"""
Base class for social connector provider components.
All social connectors must inherit from this class.

Pattern follows exchange_rates/providers/base.py architecture.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any


class SocialConnectorBase(ABC):
    """
    Abstract base class for social media connectors.

    Connectors (like Facebook, Instagram, LinkedIn, etc.) extend this class
    to provide standardized social media posting services including:
    - OAuth authentication flow
    - Post creation with text and media
    - Post status checking
    - Token refresh
    - Webhook handling

    Attributes:
        provider_key (str): Unique identifier for the provider (e.g., 'facebook_page')
        provider_name (str): Human-readable name (e.g., 'Facebook Page')
        capabilities (dict): Dictionary of supported features
        credential_schema (dict): JSON schema for required credentials
    """

    # Must be set by subclass
    provider_key: str = None  # e.g., 'facebook_page'
    provider_name: str = None  # e.g., 'Facebook Page'

    def __init__(self, credentials: dict[str, Any], config: dict[str, Any] | None = None):
        """
        Initialize connector with credentials and configuration.

        Args:
            credentials: Dictionary of decrypted OAuth credentials
            config: Optional configuration dictionary

        Raises:
            ValueError: If credentials are invalid or missing
        """
        if not self.provider_key:
            raise ValueError("provider_key must be set by subclass")
        if not self.provider_name:
            raise ValueError("provider_name must be set by subclass")

        self.credentials = credentials
        self.config = config or {}

        # Validate credentials against schema
        self.validate_credentials(credentials)

    @property
    @abstractmethod
    def capabilities(self) -> dict[str, bool]:
        """
        Return dictionary of connector capabilities.

        Example:
            {
                'text_posts': True,          # Can post text-only content
                'image_posts': True,         # Can post images
                'video_posts': False,        # Can post videos
                'carousel_posts': True,      # Can post multiple images
                'stories': False,            # Can post stories
                'reels': False,              # Can post reels/shorts
                'scheduling': True,          # Supports scheduled posts
                'link_preview': True,        # Shows link previews
                'hashtags': True,            # Supports hashtags
                'mentions': True,            # Supports @mentions
                'analytics': False,          # Can fetch post analytics
                'comments': False,           # Can fetch/post comments
                'token_refresh': True,       # Supports token refresh
            }

        Returns:
            Dictionary mapping capability names to boolean values
        """
        pass

    @property
    @abstractmethod
    def credential_schema(self) -> dict[str, Any]:
        """
        Return JSON schema describing required credentials.

        Used to generate dynamic credential entry forms and validate inputs.
        Credentials are encrypted before storage.

        Example:
            {
                'access_token': {
                    'type': 'text',
                    'label': 'Access Token',
                    'required': True,
                    'secret': True,
                    'help_text': 'OAuth access token from authentication'
                },
                'refresh_token': {
                    'type': 'text',
                    'label': 'Refresh Token',
                    'required': False,
                    'secret': True,
                    'help_text': 'Token used to refresh access token'
                },
                'page_id': {
                    'type': 'text',
                    'label': 'Page ID',
                    'required': True,
                    'help_text': 'The ID of the page to post to'
                }
            }

        Returns:
            JSON schema dictionary
        """
        pass

    @property
    @abstractmethod
    def oauth_config(self) -> dict[str, Any]:
        """
        Return OAuth configuration for this provider.

        Example:
            {
                'authorize_url': 'https://www.facebook.com/v18.0/dialog/oauth',
                'token_url': 'https://graph.facebook.com/v18.0/oauth/access_token',
                'scope': ['pages_manage_posts', 'pages_read_engagement'],
                'client_id_setting': 'FACEBOOK_APP_ID',
                'client_secret_setting': 'FACEBOOK_APP_SECRET',
            }

        Returns:
            OAuth configuration dictionary
        """
        pass

    @abstractmethod
    def validate_credentials(self, credentials: dict[str, Any]) -> None:
        """
        Validate credentials against schema and business logic.

        Args:
            credentials: Dictionary of credential values

        Raises:
            ValueError: If credentials are invalid or missing required fields
        """
        pass

    @abstractmethod
    def redact_credentials(self, credentials: dict[str, Any]) -> dict[str, Any]:
        """
        Redact sensitive credential values for logging.

        Args:
            credentials: Original credentials dictionary

        Returns:
            Dictionary with sensitive values masked (e.g., 'token_***xyz')
        """
        pass

    @abstractmethod
    def test_connection(self) -> dict[str, Any]:
        """
        Test API connection and credential validity.

        Should make a simple API call to verify credentials work.

        Returns:
            Dictionary with test results:
            {
                'success': True,
                'message': 'Connection successful',
                'details': {
                    'account_name': 'My Business Page',
                    'account_id': '123456789',
                    'followers': 5000,
                    'token_expires_at': '2025-03-01T00:00:00Z'
                }
            }
        """
        pass

    @abstractmethod
    def create_post(
        self,
        message: str,
        link: str | None = None,
        image_urls: list[str] | None = None,
        image_files: list[Any] | None = None,
        scheduled_time: datetime | None = None,
        **kwargs,
    ) -> dict[str, Any]:
        """
        Create a post on the social platform.

        Args:
            message: The text content of the post
            link: Optional URL to include (for link previews)
            image_urls: Optional list of image URLs to attach
            image_files: Optional list of image file objects to upload
            scheduled_time: Optional datetime for scheduled posting
            **kwargs: Additional platform-specific options

        Returns:
            Dictionary with post result:
            {
                'success': True,
                'post_id': '123456789_987654321',
                'post_url': 'https://facebook.com/...',
                'scheduled': False,
                'message': 'Post created successfully'
            }

        Raises:
            PostError: If post creation fails
        """
        pass

    @abstractmethod
    def get_post_status(self, post_id: str) -> dict[str, Any]:
        """
        Get the status of a posted content.

        Args:
            post_id: The platform-specific post identifier

        Returns:
            Dictionary with post status:
            {
                'exists': True,
                'status': 'published',  # published, scheduled, failed, deleted
                'engagement': {
                    'likes': 100,
                    'comments': 25,
                    'shares': 10
                },
                'post_url': 'https://...'
            }
        """
        pass

    @abstractmethod
    def delete_post(self, post_id: str) -> dict[str, Any]:
        """
        Delete a post from the platform.

        Args:
            post_id: The platform-specific post identifier

        Returns:
            Dictionary with deletion result:
            {
                'success': True,
                'message': 'Post deleted successfully'
            }
        """
        pass

    @abstractmethod
    def refresh_token(self) -> dict[str, Any]:
        """
        Refresh OAuth access token using refresh token.

        Returns:
            Dictionary with new credentials:
            {
                'success': True,
                'credentials': {
                    'access_token': 'new_token_here',
                    'refresh_token': 'new_refresh_token',
                    'expires_at': '2025-06-01T00:00:00Z'
                },
                'message': 'Token refreshed successfully'
            }

        Raises:
            TokenRefreshError: If token refresh fails
        """
        pass

    def get_account_info(self) -> dict[str, Any]:
        """
        Get account information from the platform.

        Returns:
            Dictionary with account details:
            {
                'account_id': '123456789',
                'account_name': 'My Business',
                'account_url': 'https://facebook.com/mybusiness',
                'avatar_url': 'https://...',
                'followers': 5000,
                'is_verified': True
            }
        """
        # Default implementation uses test_connection
        result = self.test_connection()
        if result.get("success"):
            return result.get("details", {})
        return {}

    def format_post_content(
        self,
        title: str,
        excerpt: str,
        url: str,
        hashtags: list[str] | None = None,
        template: str | None = None,
    ) -> str:
        """
        Format blog post content for social media.

        Args:
            title: Blog post title
            excerpt: Blog post excerpt/summary
            url: URL to the blog post
            hashtags: Optional list of hashtags
            template: Optional custom template with {title}, {excerpt}, {url}, {hashtags} placeholders

        Returns:
            Formatted post content string
        """
        if template:
            hashtag_str = " ".join(f"#{tag.strip('#')}" for tag in (hashtags or []))
            return template.format(
                title=title, excerpt=excerpt, url=url, hashtags=hashtag_str
            ).strip()

        # Default format
        content_parts = []
        if title:
            content_parts.append(title)
        if excerpt:
            content_parts.append(excerpt)
        if url:
            content_parts.append(url)
        if hashtags:
            hashtag_str = " ".join(f"#{tag.strip('#')}" for tag in hashtags)
            content_parts.append(hashtag_str)

        return "\n\n".join(content_parts)

    def get_character_limit(self) -> int:
        """
        Get the character limit for posts on this platform.

        Returns:
            Maximum character count for a post
        """
        # Default limit, should be overridden by subclass
        return 280  # Twitter default

    def get_provider_info(self) -> dict:
        """
        Get provider metadata for display in admin.

        Returns:
            Dictionary with provider information
        """
        return {
            "key": self.provider_key,
            "name": self.provider_name,
            "capabilities": self.capabilities,
            "character_limit": self.get_character_limit(),
        }


# Custom Exceptions
class PostError(Exception):
    """Raised when post creation fails"""

    pass


class TokenRefreshError(Exception):
    """Raised when token refresh fails"""

    pass


class OAuthError(Exception):
    """Raised when OAuth flow fails"""

    pass


class RateLimitError(Exception):
    """Raised when API rate limit is hit"""

    pass
