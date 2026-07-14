from django.test import SimpleTestCase


class FeedServiceImportSmokeTest(SimpleTestCase):
    """Regression: product_feeds.services.__init__ re-exported ProductFeedItem
    from .formatters which did not export it, causing ImportError at first use
    of any FeedService entry point."""

    def test_feed_service_importable(self):
        from product_feeds.services import (
            BaseFeedFormatter,
            CSVFeedFormatter,
            FeedService,
            JSONFeedFormatter,
            ProductFeedItem,
            XMLFeedFormatter,
        )

        self.assertTrue(callable(FeedService))
        self.assertTrue(callable(BaseFeedFormatter))
        self.assertTrue(callable(XMLFeedFormatter))
        self.assertTrue(callable(CSVFeedFormatter))
        self.assertTrue(callable(JSONFeedFormatter))
        self.assertTrue(callable(ProductFeedItem))
