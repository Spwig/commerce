"""
Tier-2 config-breadth lifecycle tests.

Where Tier-1 (`tests/invariants/`) proves the transaction is correct, Tier-2
proves it stays correct across the merchant's configuration surface — the four
checkout templates, the gateway scenarios, guest vs authenticated, and the
voucher/gift-card/shipping combinations. Not release-blocking (marked
``tier2``, not ``invariant``); breadth coverage that catches a config-specific
regression a single golden path would miss.
"""
