"""
R1 coverage: the shared ``core/utils/codes.py`` generator.

R1 consolidated five independent code generators into one module. Three of the
five used ``random`` (Mersenne Twister — predictable from observed output), and
one had no uniqueness check at all. Every code produced here is a bearer
credential: whoever knows the string can spend the value behind it.

The format assertions matter as much as the entropy ones. Gift card codes get
printed on cards and emailed; a format regression would invalidate codes already
in customers' hands.

Plan: docs/.claude_code/plans/wondrous-moseying-wolf.md (R1 / P1.1)
"""

import re
import string
from unittest.mock import patch

import pytest

pytestmark = [
    pytest.mark.integration,
    pytest.mark.r1,
]


def _never_taken(code):
    """``exists`` callback for cases where uniqueness is not under test."""
    return False


def _money(amount, currency="USD"):
    from decimal import Decimal

    from djmoney.money import Money

    return Money(Decimal(amount), currency)


# ============================================================
# generate_unique_code — shape parameters
# ============================================================


class TestGenerateUniqueCodeShape:
    def test_default_is_a_single_eight_character_group(self):
        from core.utils.codes import generate_unique_code

        code = generate_unique_code(exists=_never_taken)

        assert re.fullmatch(r"[A-Z0-9]{8}", code), code

    def test_length_controls_characters_per_group(self):
        from core.utils.codes import generate_unique_code

        code = generate_unique_code(exists=_never_taken, length=12)

        assert len(code) == 12
        assert re.fullmatch(r"[A-Z0-9]{12}", code), code

    def test_groups_are_joined_by_the_separator(self):
        from core.utils.codes import generate_unique_code

        code = generate_unique_code(exists=_never_taken, length=4, groups=3)

        assert re.fullmatch(r"[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}", code), code

    def test_prefix_leads_the_code(self):
        from core.utils.codes import generate_unique_code

        code = generate_unique_code(exists=_never_taken, prefix="GC", length=4, groups=3)

        assert re.fullmatch(r"GC-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}", code), code

    def test_custom_separator_is_honoured(self):
        from core.utils.codes import generate_unique_code

        code = generate_unique_code(
            exists=_never_taken, prefix="REF", length=3, groups=2, separator="_"
        )

        assert re.fullmatch(r"REF_[A-Z0-9]{3}_[A-Z0-9]{3}", code), code

    def test_no_prefix_means_no_leading_separator(self):
        from core.utils.codes import generate_unique_code

        code = generate_unique_code(exists=_never_taken, length=4, groups=2)

        assert not code.startswith("-"), code
        assert code.count("-") == 1

    def test_alphabet_restricts_the_character_set(self):
        from core.utils.codes import generate_unique_code

        code = generate_unique_code(exists=_never_taken, length=20, alphabet="AB")

        assert set(code) <= {"A", "B"}, code

    def test_groups_below_one_is_rejected(self):
        from core.utils.codes import generate_unique_code

        with pytest.raises(ValueError, match="groups must be >= 1"):
            generate_unique_code(exists=_never_taken, groups=0)

    def test_length_below_one_is_rejected(self):
        from core.utils.codes import random_string

        with pytest.raises(ValueError, match="length must be >= 1"):
            random_string(0)


# ============================================================
# generate_unique_code — collision handling
# ============================================================


class TestGenerateUniqueCodeCollisions:
    def test_retries_past_a_taken_code(self):
        from core.utils import codes as codes_module

        sequence = iter(["TAKEN001", "TAKEN002", "FREE0003"])
        with patch.object(
            codes_module, "random_string", side_effect=lambda length, alphabet=None: next(sequence)
        ):
            code = codes_module.generate_unique_code(exists=lambda c: c.startswith("TAKEN"))

        assert code == "FREE0003", (
            "The generator must keep trying until `exists` reports the code free."
        )

    def test_raises_when_every_attempt_collides(self):
        from core.utils.codes import CodeGenerationError, generate_unique_code

        with pytest.raises(CodeGenerationError):
            generate_unique_code(exists=lambda c: True)

    def test_exhaustion_error_mentions_the_shape(self):
        """The message has to be diagnosable — it means something is badly wrong."""
        from core.utils.codes import CodeGenerationError, generate_unique_code

        with pytest.raises(CodeGenerationError) as excinfo:
            generate_unique_code(exists=lambda c: True, prefix="GC", length=4, groups=3)

        message = str(excinfo.value)
        assert "GC" in message
        assert "10" in message  # MAX_ATTEMPTS

    def test_max_attempts_is_respected(self):
        from core.utils.codes import CodeGenerationError, generate_unique_code

        calls = []

        def always_taken(code):
            calls.append(code)
            return True

        with pytest.raises(CodeGenerationError):
            generate_unique_code(exists=always_taken, max_attempts=3)

        assert len(calls) == 3

    def test_does_not_fall_back_to_a_differently_shaped_code(self):
        """
        The old gift card generator fell back to ``f"{prefix}-{uuid4().hex[:12]}"``
        after 10 collisions, silently producing a code in a different format.
        """
        from core.utils.codes import CodeGenerationError, generate_unique_code

        with pytest.raises(CodeGenerationError):
            generate_unique_code(exists=lambda c: True, prefix="GC", length=4, groups=3)


# ============================================================
# Alphabet
# ============================================================


class TestUnambiguousAlphabet:
    @pytest.mark.parametrize("char", ["0", "O", "1", "I"])
    def test_excludes_the_confusable_characters(self, char):
        from core.utils.codes import UNAMBIGUOUS_ALPHABET

        assert char not in UNAMBIGUOUS_ALPHABET, (
            f"{char!r} is trivially mis-read when a customer types a code off a "
            f"printed card or an email."
        )

    def test_contains_every_other_uppercase_alphanumeric(self):
        from core.utils.codes import UNAMBIGUOUS_ALPHABET

        expected = {c for c in (string.ascii_uppercase + string.digits) if c not in "0O1I"}
        assert set(UNAMBIGUOUS_ALPHABET) == expected
        assert len(UNAMBIGUOUS_ALPHABET) == 32

    def test_alphanumeric_alphabet_is_the_full_set(self):
        from core.utils.codes import ALPHANUMERIC_ALPHABET

        assert set(ALPHANUMERIC_ALPHABET) == set(string.ascii_uppercase + string.digits)
        assert len(ALPHANUMERIC_ALPHABET) == 36


# ============================================================
# Entropy source
# ============================================================


class TestUsesSecretsNotRandom:
    """
    Mirrors the assertion style at
    tests/integration/test_voucher_gift_card_system.py:947 — patch ``random``
    to explode, then generate. A bearer credential drawn from the Mersenne
    Twister is predictable from a handful of observed outputs.
    """

    def test_random_string_does_not_call_random_choice(self):
        from core.utils.codes import random_string

        with patch("random.choice", side_effect=AssertionError("random.choice must not be used")):
            code = random_string(10)

        assert len(code) == 10

    def test_random_string_does_not_call_random_choices(self):
        from core.utils.codes import random_string

        with patch(
            "random.choices",
            side_effect=AssertionError("random.choices must not be used"),
        ):
            code = random_string(10)

        assert len(code) == 10

    def test_generate_unique_code_does_not_call_random_choice(self):
        from core.utils.codes import generate_unique_code

        with patch("random.choice", side_effect=AssertionError("random.choice must not be used")):
            code = generate_unique_code(exists=_never_taken, length=4, groups=3, prefix="GC")

        assert code.startswith("GC-")

    def test_random_string_uses_secrets_choice(self):
        """Positive control: assert the secrets path is the one actually taken."""
        from core.utils.codes import random_string

        with patch("core.utils.codes.secrets.choice", return_value="Z") as mock_choice:
            code = random_string(6)

        assert code == "ZZZZZZ"
        assert mock_choice.call_count == 6

    def test_generated_codes_are_not_repeated(self):
        from core.utils.codes import generate_unique_code

        codes = {generate_unique_code(exists=_never_taken) for _ in range(500)}

        assert len(codes) == 500


# ============================================================
# Existing formats must not regress
# ============================================================


@pytest.mark.django_db
class TestGiftCardCodeFormat:
    """
    ``GC-XXXX-XXXX-XXXX``. These codes are printed on cards and sent by email —
    changing the shape invalidates codes already in customers' hands.
    """

    def test_matches_the_documented_format(self):
        from catalog.models import GiftCard

        code = GiftCard.generate_code()

        assert re.fullmatch(r"GC-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}", code), (
            f"Gift card code {code!r} does not match GC-XXXX-XXXX-XXXX."
        )

    def test_total_length_is_stable(self):
        from catalog.models import GiftCard

        assert len(GiftCard.generate_code()) == 17

    def test_uses_the_unambiguous_alphabet(self):
        from catalog.models import GiftCard

        # Sample enough codes that an excluded character would almost certainly
        # appear if the alphabet were wrong (32-character set vs 36).
        sampled = "".join("".join(GiftCard.generate_code().split("-")[1:]) for _ in range(200))
        assert len(sampled) == 200 * 12
        for char in "0O1I":
            assert char not in sampled, (
                f"{char!r} appeared in a gift card code — the generator is no "
                f"longer using UNAMBIGUOUS_ALPHABET."
            )

    def test_honours_a_custom_prefix(self):
        from catalog.models import GiftCard

        code = GiftCard.generate_code(prefix="XG")

        assert code.startswith("XG-")

    def test_codes_are_unique(self):
        from catalog.models import GiftCard

        codes = {GiftCard.generate_code() for _ in range(200)}

        assert len(codes) == 200

    def test_does_not_use_random(self):
        from catalog.models import GiftCard

        with patch("random.choice", side_effect=AssertionError("random.choice must not be used")):
            code = GiftCard.generate_code()

        assert code.startswith("GC-")

    def test_skips_a_code_already_in_the_database(self, django_site):
        """The uniqueness callback must actually query GiftCard."""
        from catalog.models import GiftCard
        from core.utils import codes as codes_module
        from tests.factories import ProductFactory

        sequence = iter(["AAAA", "BBBB", "CCCC", "DDDD", "EEEE", "FFFF"])
        product = ProductFactory()
        GiftCard.objects.create(
            code="GC-AAAA-BBBB-CCCC",
            product=product,
            initial_value=_money("50.00"),
        )

        with patch.object(
            codes_module,
            "random_string",
            side_effect=lambda length, alphabet=None: next(sequence),
        ):
            code = GiftCard.generate_code()

        assert code == "GC-DDDD-EEEE-FFFF"


@pytest.mark.django_db
class TestVoucherCodeFormat:
    """``VoucherCode.generate_unique_code()`` — 8 characters, no separators."""

    def test_is_eight_alphanumeric_characters(self):
        from vouchers.models import VoucherCode

        code = VoucherCode().generate_unique_code()

        assert re.fullmatch(r"[A-Z0-9]{8}", code), (
            f"Voucher code {code!r} is no longer 8 plain alphanumerics."
        )

    def test_length_argument_is_honoured(self):
        from vouchers.models import VoucherCode

        assert len(VoucherCode().generate_unique_code(length=12)) == 12

    def test_has_no_separator(self):
        from vouchers.models import VoucherCode

        code = VoucherCode().generate_unique_code()

        assert "-" not in code

    def test_does_not_use_random(self):
        from vouchers.models import VoucherCode

        with patch("random.choice", side_effect=AssertionError("random.choice must not be used")):
            code = VoucherCode().generate_unique_code()

        assert len(code) == 8

    def test_codes_are_unique(self):
        from vouchers.models import VoucherCode

        codes = {VoucherCode().generate_unique_code() for _ in range(200)}

        assert len(codes) == 200
