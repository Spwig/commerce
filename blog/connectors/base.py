"""
Base Social Connector Interface.

All social connector packages must inherit from BaseSocialConnector
and implement the required methods.

"""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from blog.models import SocialConnectorAccount

logger = logging.getLogger(__name__)


class ConnectorCapability(Enum):
    """Capabilities that a social connector can support."""

    POST_TEXT = "post_text"
    POST_IMAGE = "post_image"
    POST_VIDEO = "post_video"
    POST_LINK = "post_link"
    SCHEDULE_POST = "schedule_post"
    DELETE_POST = "delete_post"
    GET_ANALYTICS = "get_analytics"
    REFRESH_TOKEN = "refresh_token"


@dataclass
class PostResult:
    """Result of a social media post operation."""

    success: bool
    post_id: str | None = None
    post_url: str | None = None
    error_message: str | None = None
    error_code: str | None = None
    platform_data: dict | None = None


@dataclass
class ConnectorInfo:
    """Metadata about a social connector."""

    provider_key: str
    display_name: str
    description: str
    icon: str  # Path to icon file relative to package
    oauth_scopes: list[str]
    capabilities: list[ConnectorCapability]
    max_text_length: int
    supports_hashtags: bool
    supports_mentions: bool
    rate_limit_posts_per_hour: int = 10


class BaseSocialConnector(ABC):
    """
    Base class for social media connectors.

    All social connector packages must inherit from this class and
    implement the abstract methods.

    Example usage:
        class FacebookPageConnector(BaseSocialConnector):
            def get_info(self) -> ConnectorInfo:
                return ConnectorInfo(
                    provider_key='facebook_page',
                    display_name='Facebook Page',
                    ...
                )

            def post(self, account, text, link=None, image_url=None, video_url=None) -> PostResult:
                # Post to Facebook
                ...
    """

    @abstractmethod
    def get_info(self) -> ConnectorInfo:
        """
        Return metadata about this connector.

        Returns:
            ConnectorInfo with details about the connector
        """
        pass

    @abstractmethod
    def get_oauth_url(self, redirect_uri: str, state: str) -> str:
        """
        Generate OAuth authorization URL.

        Args:
            redirect_uri: URL to redirect after authorization
            state: State parameter for CSRF protection

        Returns:
            URL to redirect user to for OAuth authorization
        """
        pass

    @abstractmethod
    def handle_oauth_callback(self, code: str, redirect_uri: str) -> dict[str, Any]:
        """
        Handle OAuth callback and exchange code for tokens.

        Args:
            code: Authorization code from OAuth provider
            redirect_uri: Same redirect_uri used in get_oauth_url

        Returns:
            Dict with:
                - access_token: OAuth access token
                - refresh_token: OAuth refresh token (if available)
                - expires_in: Token expiration in seconds
                - account_id: Platform account ID
                - account_name: Platform account name
                - account_url: URL to the account on the platform
                - avatar_url: URL to account avatar/profile picture
        """
        pass

    @abstractmethod
    def post(
        self,
        account: "SocialConnectorAccount",
        text: str,
        link: str | None = None,
        image_url: str | None = None,
        video_url: str | None = None,
        scheduled_time: str | None = None,
    ) -> PostResult:
        """
        Post content to the social platform.

        Args:
            account: SocialConnectorAccount instance with credentials
            text: Post text content
            link: Optional link to include
            image_url: Optional image URL to attach
            video_url: Optional video URL to attach
            scheduled_time: Optional ISO datetime for scheduled post

        Returns:
            PostResult with success/failure details
        """
        pass

    def delete_post(self, account: "SocialConnectorAccount", post_id: str) -> bool:
        """
        Delete a previously created post.

        Args:
            account: SocialConnectorAccount instance
            post_id: Platform-specific post ID

        Returns:
            True if deleted successfully
        """
        raise NotImplementedError("delete_post not supported by this connector")

    def refresh_token(self, account: "SocialConnectorAccount") -> dict[str, Any]:
        """
        Refresh OAuth access token.

        Args:
            account: SocialConnectorAccount instance with refresh token

        Returns:
            Dict with new access_token, expires_in, and optionally new refresh_token
        """
        raise NotImplementedError("refresh_token not supported by this connector")

    def get_analytics(self, account: "SocialConnectorAccount", post_id: str) -> dict[str, Any]:
        """
        Get analytics for a specific post.

        Args:
            account: SocialConnectorAccount instance
            post_id: Platform-specific post ID

        Returns:
            Dict with analytics data (likes, shares, comments, reach, etc.)
        """
        raise NotImplementedError("get_analytics not supported by this connector")

    def validate_credentials(self, account: "SocialConnectorAccount") -> bool:
        """
        Validate that account credentials are still valid.

        Args:
            account: SocialConnectorAccount instance

        Returns:
            True if credentials are valid
        """
        # Default implementation - attempt a simple API call
        try:
            credentials = account.get_credentials()
            return bool(credentials.get("access_token"))
        except Exception:
            return False

    def format_text(self, text: str, hashtags: list[str] = None, mentions: list[str] = None) -> str:
        """
        Format text with hashtags and mentions for the platform.

        Args:
            text: Base text content
            hashtags: List of hashtags (without #)
            mentions: List of usernames to mention (without @)

        Returns:
            Formatted text ready for posting
        """
        info = self.get_info()
        formatted = text

        if hashtags and info.supports_hashtags:
            hashtag_str = " ".join(f"#{tag}" for tag in hashtags)
            formatted = f"{formatted}\n\n{hashtag_str}"

        if mentions and info.supports_mentions:
            mention_str = " ".join(f"@{user}" for user in mentions)
            formatted = f"{mention_str} {formatted}"

        # Truncate if needed
        if len(formatted) > info.max_text_length:
            formatted = formatted[: info.max_text_length - 3] + "..."

        return formatted


class SocialConnectorRegistry:
    """
    Registry for available social connectors.

    Connectors are loaded dynamically from installed component packages.
    """

    _connectors: dict[str, BaseSocialConnector] = {}

    @classmethod
    def register(cls, connector: BaseSocialConnector):
        """Register a social connector."""
        info = connector.get_info()
        cls._connectors[info.provider_key] = connector
        logger.info(f"Registered social connector: {info.provider_key} ({info.display_name})")

    @classmethod
    def unregister(cls, provider_key: str):
        """Unregister a social connector."""
        if provider_key in cls._connectors:
            del cls._connectors[provider_key]
            logger.info(f"Unregistered social connector: {provider_key}")

    @classmethod
    def get(cls, provider_key: str) -> BaseSocialConnector | None:
        """Get a connector by provider key."""
        return cls._connectors.get(provider_key)

    @classmethod
    def get_all(cls) -> dict[str, BaseSocialConnector]:
        """Get all registered connectors."""
        return cls._connectors.copy()

    @classmethod
    def get_available_providers(cls) -> list[ConnectorInfo]:
        """Get info about all available connectors."""
        return [connector.get_info() for connector in cls._connectors.values()]

    @classmethod
    def load_from_components(cls):
        """
        Load connectors from installed component packages.

        Scans the component registry for social connector components
        and loads their connector classes via components_data/.
        """
        try:
            from component_updates.integration_paths import (
                INTEGRATIONS_DIR,
                import_component_module,
            )
            from component_updates.models import ComponentRegistry

            # Find installed social connector components
            connectors = ComponentRegistry.objects.filter(
                component_type="social_connector", is_enabled=True
            )

            for component in connectors:
                try:
                    # Load from components_data via file-path-based import
                    provider_dir = INTEGRATIONS_DIR / "social_connector" / component.component_key
                    current_path = provider_dir / "current"
                    if not current_path.exists():
                        logger.warning(
                            f"No current version for social connector {component.component_key}"
                        )
                        continue

                    module_name = f"social_connector_{component.component_key}"
                    module = import_component_module(current_path, "connector", module_name)

                    # Get the connector class (should be named <Name>Connector)
                    connector_class = getattr(module, "Connector", None)
                    if connector_class:
                        connector = connector_class()
                        cls.register(connector)

                except Exception as e:
                    logger.error(f"Failed to load social connector {component.component_key}: {e}")

        except Exception as e:
            logger.error(f"Failed to load social connectors from components: {e}")
