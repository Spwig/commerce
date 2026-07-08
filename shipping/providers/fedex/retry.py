# -*- coding: utf-8 -*-
"""
Retry logic with exponential backoff for FedEx API calls.

This module provides utilities for retrying failed API requests with
intelligent backoff strategies to handle transient failures gracefully.
"""
import time
import logging
from functools import wraps
from typing import Callable, Type, Tuple, Optional

from .exceptions import (
    FedExServiceUnavailableError,
    FedExRateLimitError,
    FedExAPIError,
)

logger = logging.getLogger(__name__)


class RetryConfig:
    """Configuration for retry behavior."""

    def __init__(
        self,
        max_retries: int = 3,
        initial_delay: float = 1.0,
        max_delay: float = 60.0,
        exponential_base: float = 2.0,
        jitter: bool = True,
    ):
        """
        Initialize retry configuration.

        Args:
            max_retries: Maximum number of retry attempts (default: 3)
            initial_delay: Initial delay in seconds (default: 1.0)
            max_delay: Maximum delay in seconds (default: 60.0)
            exponential_base: Base for exponential backoff (default: 2.0)
            jitter: Add randomness to delay to prevent thundering herd (default: True)
        """
        self.max_retries = max_retries
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.jitter = jitter

    def get_delay(self, attempt: int) -> float:
        """
        Calculate delay for given attempt number.

        Uses exponential backoff: delay = initial_delay * (exponential_base ^ attempt)

        Args:
            attempt: Current attempt number (0-indexed)

        Returns:
            Delay in seconds
        """
        delay = self.initial_delay * (self.exponential_base ** attempt)
        delay = min(delay, self.max_delay)

        if self.jitter:
            # Add random jitter (0-50% of delay)
            import random
            jitter_amount = delay * random.uniform(0, 0.5)
            delay += jitter_amount

        return delay


# Default retry configurations for different scenarios
DEFAULT_RETRY_CONFIG = RetryConfig(
    max_retries=3,
    initial_delay=1.0,
    max_delay=60.0,
    exponential_base=2.0,
)

RATE_LIMIT_RETRY_CONFIG = RetryConfig(
    max_retries=5,
    initial_delay=2.0,
    max_delay=120.0,
    exponential_base=2.0,
)

SERVICE_UNAVAILABLE_RETRY_CONFIG = RetryConfig(
    max_retries=3,
    initial_delay=5.0,
    max_delay=60.0,
    exponential_base=2.0,
)


def should_retry(exception: Exception) -> bool:
    """
    Determine if an exception should trigger a retry.

    Args:
        exception: The exception that was raised

    Returns:
        True if should retry, False otherwise
    """
    # Always retry service unavailable errors
    if isinstance(exception, FedExServiceUnavailableError):
        return True

    # Always retry rate limit errors
    if isinstance(exception, FedExRateLimitError):
        return True

    # Retry specific HTTP errors (timeouts, 5xx errors)
    if hasattr(exception, 'response'):
        status_code = getattr(exception.response, 'status_code', None)
        if status_code in [408, 429, 500, 502, 503, 504]:
            return True

    # Don't retry other errors (authentication, validation, etc.)
    return False


def get_retry_config(exception: Exception) -> RetryConfig:
    """
    Get appropriate retry configuration based on exception type.

    Args:
        exception: The exception that was raised

    Returns:
        RetryConfig instance
    """
    if isinstance(exception, FedExRateLimitError):
        return RATE_LIMIT_RETRY_CONFIG
    elif isinstance(exception, FedExServiceUnavailableError):
        return SERVICE_UNAVAILABLE_RETRY_CONFIG
    else:
        return DEFAULT_RETRY_CONFIG


def retry_with_backoff(
    retryable_exceptions: Tuple[Type[Exception], ...] = (
        FedExServiceUnavailableError,
        FedExRateLimitError,
    ),
    config: Optional[RetryConfig] = None,
):
    """
    Decorator to retry a function with exponential backoff.

    Usage:
        @retry_with_backoff()
        def make_api_call():
            # API call that might fail
            pass

    Args:
        retryable_exceptions: Tuple of exception types to retry
        config: RetryConfig instance (defaults to DEFAULT_RETRY_CONFIG)

    Returns:
        Decorated function
    """
    if config is None:
        config = DEFAULT_RETRY_CONFIG

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0

            while True:
                try:
                    return func(*args, **kwargs)

                except retryable_exceptions as e:
                    # Check if we should retry this specific exception
                    if not should_retry(e):
                        logger.warning(
                            f"{func.__name__} failed with non-retryable error: {e}"
                        )
                        raise

                    # Check if we've exhausted retries
                    if attempt >= config.max_retries:
                        logger.error(
                            f"{func.__name__} failed after {attempt + 1} attempts"
                        )
                        raise

                    # Get retry configuration for this exception type
                    retry_config = get_retry_config(e)

                    # Calculate delay
                    delay = retry_config.get_delay(attempt)

                    # Special handling for rate limit errors with retry_after
                    if isinstance(e, FedExRateLimitError) and e.retry_after:
                        delay = max(delay, e.retry_after)

                    logger.warning(
                        f"{func.__name__} attempt {attempt + 1} failed: {e}. "
                        f"Retrying in {delay:.2f} seconds..."
                    )

                    # Wait before retrying
                    time.sleep(delay)
                    attempt += 1

                except Exception as e:
                    # Non-retryable exception, raise immediately
                    logger.error(f"{func.__name__} failed with non-retryable error: {e}")
                    raise

        return wrapper

    return decorator


class RetryHandler:
    """
    Context manager for retry logic with exponential backoff.

    Usage:
        retry_handler = RetryHandler(max_retries=3)
        for attempt in retry_handler:
            try:
                result = make_api_call()
                break
            except FedExServiceUnavailableError as e:
                retry_handler.handle_exception(e)
    """

    def __init__(self, config: Optional[RetryConfig] = None):
        """
        Initialize retry handler.

        Args:
            config: RetryConfig instance (defaults to DEFAULT_RETRY_CONFIG)
        """
        self.config = config or DEFAULT_RETRY_CONFIG
        self.attempt = 0
        self.last_exception = None

    def __iter__(self):
        """Iterate through retry attempts."""
        return self

    def __next__(self):
        """Get next retry attempt."""
        if self.attempt >= self.config.max_retries + 1:
            if self.last_exception:
                raise self.last_exception
            raise StopIteration

        attempt_num = self.attempt
        self.attempt += 1
        return attempt_num

    def handle_exception(self, exception: Exception):
        """
        Handle an exception during retry attempt.

        Args:
            exception: The exception that occurred

        Raises:
            The exception if retries exhausted or non-retryable
        """
        self.last_exception = exception

        # Check if we should retry
        if not should_retry(exception):
            logger.warning(f"Non-retryable error: {exception}")
            raise

        # Check if we've exhausted retries
        if self.attempt > self.config.max_retries:
            logger.error(f"Failed after {self.attempt} attempts")
            raise

        # Get retry configuration for this exception type
        retry_config = get_retry_config(exception)

        # Calculate delay
        delay = retry_config.get_delay(self.attempt - 1)

        # Special handling for rate limit errors
        if isinstance(exception, FedExRateLimitError) and exception.retry_after:
            delay = max(delay, exception.retry_after)

        logger.warning(
            f"Attempt {self.attempt} failed: {exception}. "
            f"Retrying in {delay:.2f} seconds..."
        )

        # Wait before next attempt
        time.sleep(delay)


# Convenience function for one-off retries
def retry_call(
    func: Callable,
    *args,
    config: Optional[RetryConfig] = None,
    **kwargs,
):
    """
    Execute a function with retry logic.

    Usage:
        result = retry_call(make_api_call, arg1, arg2, config=my_config)

    Args:
        func: Function to call
        *args: Positional arguments for func
        config: RetryConfig instance
        **kwargs: Keyword arguments for func

    Returns:
        Result of func(*args, **kwargs)
    """
    @retry_with_backoff(config=config)
    def wrapper():
        return func(*args, **kwargs)

    return wrapper()
