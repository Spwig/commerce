"""Two-proportion significance behind A/B winner confidence."""

from django.test import SimpleTestCase

from email_marketing.services.ab_stats import is_reliable, two_proportion_confidence


class TwoProportionConfidenceTests(SimpleTestCase):
    def test_a_clear_difference_is_highly_confident(self):
        # 90% vs 50% over 100 recipients each — unmistakable.
        self.assertGreater(two_proportion_confidence(90, 100, 50, 100), 0.99)

    def test_a_tiny_difference_on_a_small_sample_is_not_confident(self):
        # 55% vs 50% over 20 each sits well below the 95% bar.
        c = two_proportion_confidence(11, 20, 10, 20)
        self.assertLess(c, 0.95)
        self.assertGreater(c, 0.0)

    def test_the_same_gap_grows_more_convincing_with_more_data(self):
        small = two_proportion_confidence(11, 20, 9, 20)
        large = two_proportion_confidence(550, 1000, 450, 1000)
        self.assertGreater(large, small)

    def test_zero_recipients_returns_zero(self):
        self.assertEqual(two_proportion_confidence(0, 0, 5, 10), 0.0)
        self.assertEqual(two_proportion_confidence(5, 10, 0, 0), 0.0)

    def test_no_variation_returns_zero(self):
        self.assertEqual(two_proportion_confidence(0, 50, 0, 50), 0.0)  # every arm all-miss
        self.assertEqual(two_proportion_confidence(50, 50, 50, 50), 0.0)  # every arm all-hit

    def test_identical_rates_return_zero(self):
        self.assertEqual(two_proportion_confidence(25, 50, 25, 50), 0.0)

    def test_result_is_always_bounded(self):
        for c in (
            two_proportion_confidence(100, 100, 0, 100),
            two_proportion_confidence(1, 1000, 999, 1000),
            two_proportion_confidence(3, 7, 2, 9),
        ):
            self.assertGreaterEqual(c, 0.0)
            self.assertLessEqual(c, 1.0)


class ReliabilityTests(SimpleTestCase):
    def test_a_healthy_sample_is_reliable(self):
        self.assertTrue(is_reliable(20, 40, 12, 40))

    def test_a_tiny_lopsided_sample_is_not_reliable(self):
        # 1/1 vs 0/39 reads as "100% confident" from the z-test — but it's noise.
        self.assertFalse(is_reliable(1, 1, 0, 39))

    def test_zero_recipients_is_not_reliable(self):
        self.assertFalse(is_reliable(0, 0, 3, 30))

    def test_rare_events_need_more_recipients(self):
        # ~1% event rate over 100 each: fewer than 5 expected events per arm.
        self.assertFalse(is_reliable(1, 100, 1, 100))
        # Healthy event counts over the same size are fine.
        self.assertTrue(is_reliable(20, 100, 30, 100))
