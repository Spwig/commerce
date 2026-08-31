# Email delivery & throughput

How Spwig turns a queued email into a sent one, and how transactional mail (order
confirmations, password resets) is kept ahead of marketing (campaigns, journeys) on
a shared SMTP account. Audience: operators and contributors. All knobs are Django
settings, overridable by environment variable.

## The pipeline

Every outgoing email is an `EmailOutbox` row. It is created `queued` (in live mode)
and delivered by one of these paths — all of which funnel through
`EmailSendingService.send_email`, whose **atomic claim** (`queued → sending` in one
UPDATE) guarantees a message is never sent twice:

- **Transactional fast lane.** `send_template_email` (order/account/etc. email)
  registers an on-commit dispatch of the `email_system.send_outbox_email` Celery
  task, so the message is delivered within seconds of the transaction committing,
  off the web request. A broker hiccup can't break the request — the sweep recovers.
- **Marketing drainer.** `email_marketing.drain_campaign_outbox` (beat, 60s) sends a
  throttled batch of campaign `CampaignSend` rows.
- **Safety-net sweep.** `email_system.drain_pending_outbox` (beat, 90s) delivers any
  stranded `queued` row (a lost dispatch) and reclaims rows stuck in `sending` (a
  worker that died mid-send). It is also the *only* sender for journey-step emails.
- **Retry.** `email_system.retry_failed_emails` (beat, 5m) re-sends `failed` rows
  once their backoff has elapsed, so a transient SMTP error doesn't permanently lose
  a transactional email.

## Delivery modes (`SiteSettings.email_delivery_mode`)

- `live` — deliver normally.
- `paused` — new **and already-queued** mail is held (`held`); nothing sends. Acts as
  a kill switch even mid-blast. Release by switching back to `live`.
- `log_only` — mail is recorded (`logged`) but never sent.

## Transactional-first throughput

Priority band lives on `EmailOutbox.priority` (lower = higher): transactional is
stamped `PRIORITY_TRANSACTIONAL` (2), marketing `PRIORITY_MARKETING` (8). Only
marketing-band rows are throttled; everything else always sends.

The **per-account SMTP budget** (`email_system.services.send_budget`, Redis) enforces
it: within a per-minute window, marketing may send only while the total is under
`ceiling − reserve`; transactional always sends and is counted, so a transactional
burst makes marketing yield *more*. This guarantees ≥ `reserve` sends/minute of
headroom for transactional. It is **off by default** — the platform can't guess a
merchant's SMTP limit.

| Setting | Default | Meaning |
|---|---|---|
| `EMAIL_ACCOUNT_SEND_RATE_PER_MINUTE` | `0` (off) | The account's safe sends/minute. Set **below** your provider's hard limit — transactional is never throttled, so total can exceed this during a transactional spike. |
| `EMAIL_TRANSACTIONAL_RESERVE_PER_MINUTE` | `30` | Sends/minute always kept free for transactional. |

When the budget is exhausted, marketing sends **defer** (stay queued, retried next
tick) rather than fail. If marketing is fully starved for a tick the drainer logs a
warning.

## Operational notes

- **First deploy with a pre-existing queued backlog.** The sweep only delivers rows
  queued within `EMAIL_PENDING_SWEEP_MAX_AGE_HOURS` (default 24). If an install has a
  large backlog of old `queued` rows (e.g. from before the delivery fix), set
  `EMAIL_PENDING_SWEEP_FLOOR` to the go-live instant (ISO-8601) so ancient
  confirmations / stale reset links are not mailed.
- **Rollback is config, not code.** `EMAIL_AUTO_DISPATCH=0` stops the fast lane;
  `EMAIL_PENDING_SWEEP_ENABLED=0` stops the sweep; `EMAIL_ACCOUNT_SEND_RATE_PER_MINUTE=0`
  disables throttling. All revert to prior behaviour without a deploy.

## Settings reference

| Setting | Default | Purpose |
|---|---|---|
| `EMAIL_AUTO_DISPATCH` | `True` | On-commit fast-lane dispatch for transactional mail. |
| `EMAIL_PENDING_SWEEP_ENABLED` | `True` | The safety-net sweep. |
| `EMAIL_PENDING_SWEEP_GRACE_SECONDS` | `120` | Don't sweep a row until it's this old (let the fast path win). |
| `EMAIL_PENDING_SWEEP_STUCK_SECONDS` | `600` | A `sending` row older than this is reclaimed. |
| `EMAIL_PENDING_SWEEP_MAX_AGE_HOURS` | `24` | Upper bound on how old a swept row may be. |
| `EMAIL_PENDING_SWEEP_BATCH` | `200` | Max rows dispatched per sweep tick. |
| `EMAIL_PENDING_SWEEP_FLOOR` | unset | Hard floor: never deliver rows queued before this instant. |
| `EMAIL_ACCOUNT_SEND_RATE_PER_MINUTE` | `0` | SMTP ceiling/minute (0 disables throttling). |
| `EMAIL_TRANSACTIONAL_RESERVE_PER_MINUTE` | `30` | Headroom reserved for transactional. |
| `EMAIL_RETRY_BACKOFF_MINUTES` | `15` | Minimum wait between retry attempts. |
| `EMAIL_CAMPAIGN_STUCK_SECONDS` | `600` | A `CampaignSend` stuck in `sending` is reclaimed after this. |
