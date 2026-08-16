"""
Rotate, pre-publish, or retire the merchant's agentic signing keys.

This is the operator surface for the key lifecycle (`AgentKey` is intentionally
kept out of the admin — it holds encrypted private material). Typical use::

    # Two-phase rollover: stage the new key, let verifiers cache it, then switch.
    ./manage.py agentic_rotate_keys --prepublish
    ./manage.py agentic_rotate_keys                # promote staged, retire old

    # One-shot rotation of just the AP2 mandate key, 3-day overlap:
    ./manage.py agentic_rotate_keys --purpose ap2_mandate --overlap-days 3

    # Retire one specific key immediately (e.g. suspected compromise):
    ./manage.py agentic_rotate_keys --retire <kid>
"""

from django.core.management.base import BaseCommand, CommandError

from agentic.models import AgentKey
from agentic.services import key_service

_PURPOSES = (AgentKey.PURPOSE_TRANSPORT, AgentKey.PURPOSE_AP2)


class Command(BaseCommand):
    help = "Rotate, pre-publish, or retire the store's agentic signing keys."

    def add_arguments(self, parser):
        parser.add_argument(
            "--purpose",
            choices=(*_PURPOSES, "all"),
            default="all",
            help="Which key purpose to act on (default: all).",
        )
        parser.add_argument(
            "--overlap-days",
            type=int,
            default=key_service.DEFAULT_OVERLAP_DAYS,
            help="Days a rotated-out key stays published so recent signatures verify.",
        )
        parser.add_argument(
            "--prepublish",
            action="store_true",
            help="Stage a new rotating key (published, not yet signing) instead of rotating now.",
        )
        parser.add_argument(
            "--retire",
            metavar="KID",
            default=None,
            help="Retire one specific key by kid (overrides --purpose/--prepublish).",
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Allow --retire to remove the last active key of a purpose (stops signing).",
        )

    def handle(self, *args, **options):
        overlap = options["overlap_days"]
        if overlap < 0:
            raise CommandError("--overlap-days must be >= 0")

        if options["retire"]:
            kid = options["retire"]
            self._guard_last_active(kid, force=options["force"])
            try:
                key = key_service.retire_signing_key(kid, overlap_days=overlap)
            except ValueError as exc:
                raise CommandError(str(exc)) from exc
            self.stdout.write(
                self.style.SUCCESS(
                    f"Retired {key.purpose} key {key.kid[:12]}… (overlap {overlap}d)."
                )
            )
            self._warn_if_no_active(key.purpose)
            return

        purposes = _PURPOSES if options["purpose"] == "all" else (options["purpose"],)

        for purpose in purposes:
            if options["prepublish"]:
                key = key_service.prepublish_signing_key(purpose)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Pre-published {purpose} key {key.kid[:12]}… (rotating; publish then rotate)."
                    )
                )
                continue

            result = key_service.rotate_signing_key(purpose, overlap_days=overlap)
            verb = "Promoted staged" if result["promoted"] else "Minted new"
            self.stdout.write(
                self.style.SUCCESS(
                    f"{verb} {purpose} key {result['new_kid'][:12]}…; "
                    f"retired {len(result['retired_kids'])} (overlap {overlap}d)."
                )
            )

    def _guard_last_active(self, kid, *, force):
        # Retiring the only active key of a purpose silently stops signing (AP2
        # mandate issuance no-ops, transport can't sign) with no runtime error —
        # a foot-gun on a mistyped kid. Refuse unless the operator forces it;
        # rotation is the safe way to replace a key.
        key = AgentKey.objects.filter(kid=kid).first()
        if key is None or key.status != AgentKey.STATUS_ACTIVE or force:
            return
        others = (
            AgentKey.objects.filter(purpose=key.purpose, status=AgentKey.STATUS_ACTIVE)
            .exclude(kid=kid)
            .exists()
        )
        if not others:
            raise CommandError(
                f"{kid[:12]}… is the only active {key.purpose} key; retiring it stops signing. "
                f"Use `--purpose {key.purpose}` to rotate (mints a replacement), or pass --force."
            )

    def _warn_if_no_active(self, purpose):
        if not AgentKey.objects.filter(purpose=purpose, status=AgentKey.STATUS_ACTIVE).exists():
            self.stdout.write(
                self.style.WARNING(
                    f"No active {purpose} key remains. "
                    f"Run `agentic_rotate_keys --purpose {purpose}` to mint one."
                )
            )
