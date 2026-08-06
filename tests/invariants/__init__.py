"""
Release-blocking commercial invariants.

Every test here is marked ``@pytest.mark.invariant`` and asserts one of the
non-negotiable properties from the lifecycle test plan (see
docs/.claude_code/plans/i-want-us-to-jaunty-babbage.md §2.3). These run FULL in
CI on every PR and on dev/main — they are never scoped out — and a red here
blocks merge.

Each test drives the *real* order-creation / settlement / refund code and
asserts on the whole transaction footprint via ``commerce_footprint``,
not just a success flag.
"""
