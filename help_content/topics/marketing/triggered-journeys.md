---
slug: triggered-journeys
title_i18n_key: Triggered Journeys
category: marketing-seo
component: email_marketing
keywords:
  - triggered journey
  - email automation
  - drip campaign
  - welcome series
  - welcome email
  - automated email sequence
  - customer signup email
  - order placed email
  - first order email
  - journey step
  - journey enrollment
  - campaign studio
  - once per subscriber
  - re-enrollment cooldown
  - journey a/b test
  - split test journey step
  - test journey emails
  - abandoned cart email
  - cart abandonment
  - cart recovery email
  - win-back email
  - lapsed customer email
  - re-engagement email
  - post-delivery review request
  - order delivered email
  - back in stock email
  - back in stock journey
  - abandoned cart block
  - featured product block
  - journey report
  - enrollment funnel
  - attributed revenue
  - revenue per enrollee
  - revenue by step
url_patterns:
  - /admin/email_marketing/journey/
  - /admin/email_marketing/journeyenrollment/
  - /admin/campaigns/journeys/[0-9a-f-]+/report/
related:
  - recurring-campaigns
  - journey-builder
  - ab-testing
  - stock-notifications
  - campaign-reports
published: true
---

<!-- screenshots-needed:
- url: /admin/campaigns/journeys/{journey_id}/report/
  filename: journey-report.webp
  description: The Journey report page for a journey with meaningful enrollment history — the enrollment funnel cards (Enrolled/Active now/Completed/Exited) and Attributed revenue card both showing non-zero numbers, plus the "Revenue by step" table (Step/Revenue/Orders/Sent/Opens/Clicks) with at least one plain step and one A/B step, both showing real Sent/Opens/Clicks counts.
  save-to: core/static/core/admin/img/help/triggered-journeys/
  viewport: 1440x900
-->

Campaign Studio's **Journeys** are automated, multi-step email sequences that start on their own whenever a customer does something specific — signs up, places an order, leaves items in their cart, goes quiet for a while, or has an order delivered. Instead of remembering to send a welcome email, a cart-recovery nudge, or a review request by hand, you build the sequence once and Spwig runs it for every customer who qualifies, for as long as the journey stays active.

## Three ways to send email

Campaign Studio now covers three distinct sending patterns:

| Type | Behaviour |
|------|-----------|
| **Broadcast** | Sent once — immediately or at a single scheduled date and time. Use for a one-off announcement or sale. |
| **Recurring** | A template that sends on a repeating schedule (see [Recurring Campaigns](/help/recurring-campaigns)). |
| **Journey** | A multi-step sequence that starts automatically for one customer when a lifecycle event happens, then drips out its steps over hours or days. |

A journey doesn't have its own "send" button and no schedule to configure — it reacts to events instead of a clock.

## Triggers

Every journey listens for exactly one event, set as the journey's **Trigger**:

| Trigger | Fires when |
|---------|-----------|
| **Customer signs up** | A new customer account is created. |
| **Order is placed** | Any order is placed, by a new or returning customer. |
| **First order is placed** | Specifically a customer's very first order. |
| **Cart abandoned** | A shopper adds something to their cart, then goes idle without checking out. |
| **Customer lapsed (win-back)** | A customer hasn't placed an order in a while. |
| **Order delivered** | An order's status changes to Delivered. |
| **Product back in stock** | A product a customer asked to be notified about becomes available again. |

## The recovery and re-engagement triggers, in detail

**Order delivered** and **Product back in stock** fire immediately, the same way **Order is placed** does. **Cart abandoned** and **Customer lapsed (win-back)** work differently: rather than reacting to a single moment, Spwig periodically checks for shoppers and customers who match, so there can be a short delay between a cart going idle (or a customer lapsing) and enrollment.

**Cart abandoned** — enrolls a shopper who added something to their cart and then went idle without completing checkout. By default that's after around an hour of inactivity; the exact idle window (and how far back Spwig will still look) is a threshold your host can tune for your store. It works for both signed-in shoppers and guests — for a guest, Spwig uses the email address captured at checkout. If the shopper comes back and completes their order, they're automatically taken out of the journey, so a completed purchase never gets a "did you forget something?" email. Add an **Abandoned Cart** content block to the recovery email to show exactly what was left behind, with live prices, images, and a link back to the cart — or use a **Featured Product** block to spotlight one item instead.

**Customer lapsed (win-back)** — enrolls a customer who hasn't placed an order in a while, to give them a reason to come back. By default that's 90 days without a purchase (also a host-tunable threshold). A customer is only re-entered into a win-back journey at most once per that window, so someone who stays lapsed doesn't get re-enrolled again right away.

**Order delivered** — enrolls a customer once their order's status changes to **Delivered**, which is a natural moment to ask for a review a few days later. It fires once per order, on the transition into Delivered — later edits to an already-delivered order don't fire it again. Note that the order list's **Mark selected orders as Delivered** bulk action updates orders directly and does not fire this trigger (or the delivery confirmation email); update orders one at a time, or via the Spwig mobile app, for it to fire.

**Product back in stock** — when a product a customer asked to be notified about comes back in stock, Spwig checks whether you have an active journey listening for this trigger. If you do, the customer is enrolled in that journey instead of the plain one-off alert — so you can add a delay, a **Featured Product** block showing the restocked item, or a follow-up email. If no back-in-stock journey is active, customers still get the standard one-off notification email exactly as before, so turning a journey on for this trigger is entirely optional.

## Building a journey

Navigate to **Campaign Studio > Journeys** and click **Add Journey**.

1. Give the journey a **Name** — this is for your reference only; customers never see it.
2. Choose the **Trigger** event.
3. Optionally set **Only for segment** to a Segment — when set, only subscribers who belong to that segment are ever enrolled. Leave it blank to enroll every eligible subscriber.
4. Set **Once per subscriber** and **Re-enrollment cooldown (days)** — see [Guarding against over-enrollment](#guarding-against-over-enrollment) below.
5. Set **Status** to **Active** to turn the journey on. Leave it as **Draft** while you're still designing it, or set it to **Paused** to stop new enrollments without losing your setup.
6. Click **Save** — Spwig takes you straight into the [Journey Builder](/help/journey-builder), the visual canvas where you design the actual sequence: which emails send, how long to wait between them, and whether different subscribers should follow different paths.

A simple three-step welcome series, once designed on the canvas, might look like:

| Step | Waits | Sends |
|------|-------|-------|
| 1 | Immediately | Welcome Email |
| 2 | 3 days later | Getting Started Tips |
| 3 | 7 days after that | First Order Discount |

The emails themselves are ordinary Campaigns you design in the same visual builder you'd use for a Broadcast — subject line, content blocks, everything. There's no need to schedule or send one yourself; leave it as **Draft** and just pick it from the step's dropdown in the builder. The journey sends it for you, once per subscriber who reaches that step.

See [Journey Builder](/help/journey-builder) for the full guide to designing steps on the canvas, branching a journey with a **Yes/No** condition, and starting from a ready-made template instead of a blank canvas.

## A/B testing a step

Any **Send email** step can be turned into an A/B test, so a journey automatically discovers — and then keeps using — the email that performs best. Because a journey runs continuously (subscribers arrive over time), Spwig doesn't test a fixed batch and stop; instead it **splits enrollees evenly across the variants as they flow in, watches how each performs, and once one is a clear statistical winner it locks that variant in for every future enrollee.** Subscribers already partway through keep the version they were first sent.

Open a Send email step in the [Journey Builder](/help/journey-builder) and set **Step type**:

- **Single email** — the normal behaviour: everyone gets the one email you choose.
- **A/B: different emails** — pick **two to four** emails (different designs, offers, or layouts); each enrollee gets one.
- **A/B: different subject lines** — pick one email and enter **two to four** subject lines; each enrollee gets that email with a different subject.

Then choose **Pick the winner by** — **Open rate** (usually best for a subject test) or **Click rate** — and you're done. Set the journey **Active** and enrollees start being split across the variants.

The step's panel shows a **live scoreboard** as data comes in — each variant's recipients, open rate, and click rate, plus how confident Spwig is in the leader ("Leading at 92% confidence"). A winner is only locked once Spwig is at least **95% confident** *and* there's enough data to trust it, so a low-traffic journey won't jump to conclusions. Once locked, the step reads **"Winner locked: Variant B"** and every new enrollee gets that variant; on the canvas the card shows **"A/B · N emails"** while testing, then **"A/B winner: B"** once decided.

A few things to know:

- **Give it traffic.** Confidence depends on volume — a step only a handful of people reach may sit at "Not enough data yet" for a while. A/B testing shines on journeys with steady enrollment.
- **Editing the variants or the winner metric starts a fresh test** — a previously locked winner is cleared so the new set-up earns its own result.
- An A/B step with fewer than two variants **blocks the journey from going Active** until you complete it (or switch it back to a single email).

See [A/B Testing](ab-testing) for more on how Spwig reads confidence and significance.

## How enrollment works

When the trigger event happens for a customer, Spwig checks every active journey listening for that event and, for each one the customer is eligible for, **enrolls** them at the flow's starting point. From there, Spwig moves the subscriber forward through whatever you designed on the canvas — waiting out each **Wait** step, sending each **Send email** step's email, and following the correct **Yes**/**No** path at any **Branch** — until they reach an **Exit** step, at which point the journey is marked **Completed** for that subscriber.

**Consent is always respected.** A subscriber who hasn't opted into marketing email, or who has since unsubscribed, is simply skipped — the journey doesn't stop for other subscribers, and mid-journey opt-outs stop that subscriber's remaining sends automatically. You never need to filter your journeys by consent status yourself.

## Guarding against over-enrollment

Two settings on the journey control how often a subscriber can go through it:

| Setting | What it does | Typical use |
|---------|--------------|-------------|
| **Once per subscriber** *(on by default)* | Each subscriber is enrolled at most once, ever, no matter how many times the trigger event happens again for them. | A welcome series — a customer should only ever receive it once. |
| **Re-enrollment cooldown (days)** | When **Once per subscriber** is off, sets a minimum number of days that must pass since a subscriber's last enrollment before they can be enrolled again. Set to `0` for no cooldown. | An order-triggered series that should run again for a new order, but not re-fire for every order placed the same week. |

Turn **Once per subscriber** off for a journey you want to run per order (like a post-purchase thank-you), and pair it with a cooldown so a customer who orders twice in the same day only gets enrolled once. A subscriber already actively working through a journey is never enrolled into a second, overlapping run of that same journey regardless of these settings.

## Monitoring journeys

The **Campaign Studio > Journeys** list shows each journey's **Trigger**, **Status**, the number of **Emails** it sends, and running **Enrolled** / **Completed** totals, so you can see at a glance whether a journey is actually reaching people.

![The Journeys list showing two active journeys with enrollment and completion counts](/static/core/admin/img/help/triggered-journeys/journey-list.webp)

To see individual subscribers rather than totals, open the **Journey Enrollments** list at `/admin/email_marketing/journeyenrollment/`. Each row shows one subscriber's progress through one journey: which **Journey** they're in, their **Current step**, **Status** (Active, Completed, or Cancelled), and when their **Next step** is due. Use the filters to narrow it down to one journey or one status — for example, filtering to **Active** shows everyone currently mid-sequence.

![The Journey Enrollments list showing subscriber progress across two journeys](/static/core/admin/img/help/triggered-journeys/journey-enrollments.webp)

## Journey report

Every journey has its own **Report** page, opened by clicking the **Report** button on the journey's card in **Campaign Studio > Journeys**, or on the journey's own settings page. It's a single-page summary of how far enrollees get through the sequence and, where your emails contain tracked links, how much revenue the journey has driven.

![The Journey report page showing the enrollment funnel, attributed revenue card, and revenue-by-step table](/static/core/admin/img/help/triggered-journeys/journey-report.webp)

### Enrollment funnel

Four cards show where enrollees currently stand:

| Card | What it shows |
|------|---------------|
| **Enrolled** | The total number of subscribers who have ever entered this journey. |
| **Active now** | Enrollees currently partway through the sequence, waiting on or working through their next step. |
| **Completed** | Enrollees who reached the journey's **Exit** step. |
| **Exited** | Enrollees taken out of the journey before completing it — for example, a shopper who finished checkout mid-way through a cart-abandonment sequence, or a subscriber who unsubscribed. |

If the journey has no enrollments yet, all four cards read zero and a note reminds you that metrics appear once customers start entering the journey.

### Attributed revenue

The **Attributed revenue** card works the same way as a [campaign report's](campaign-reports) — Spwig traces orders back to clicks on links in the journey's emails, the same click-through, consent-gated attribution described in [Attributed revenue](campaign-reports#attributed-revenue) on that page. The same caveats apply here: attribution is click-through only (an open alone never attributes revenue), it follows your store's active attribution model and lookback window, it respects analytics consent, and it isn't retroactive — a journey only shows revenue from emails sent after attribution tracking was switched on for your store.

The card's sub-line breaks the total down into:

- **Orders** — how many orders are credited to this journey, across every step's emails combined.
- **AOV** — the average order value across those orders.
- **Revenue per enrollee** — attributed revenue divided by total **Enrolled**. A journey doesn't have a single "spend" the way a campaign does — it runs continuously rather than costing something once — so there's no ROAS figure here. **Revenue per enrollee** is the closest equivalent: a steady, comparable measure of how efficiently the journey turns an enrollment into a sale, that you can track over time or compare against another journey.

### Revenue by step

When the journey has at least one **Send email** step, a **Revenue by step** table breaks the total down further, one row per step, so you can see which email in the sequence is actually earning its keep:

| Column | What it shows |
|--------|---------------|
| **Step** | The step's email, with an **A/B** badge if that step is running an [A/B test](ab-testing). |
| **Revenue** | Attributed revenue from orders traced back to that step's email. |
| **Orders** | The number of orders behind that revenue figure. |
| **Sent** | How many times this step's email has gone out. |
| **Opens** / **Clicks** | How many of those sends were opened, and how many were clicked. Spwig tracks opens and clicks for every step's sends, plain and A/B alike. |

Use this table to spot a weak link in an otherwise healthy journey — for example, a welcome series where the first email drives most of the revenue and a later step contributes little might be a candidate for a stronger offer or a rewrite, rather than assuming the whole sequence needs a rethink.

## Tips

- The fastest way to start a cart-abandonment, win-back, post-delivery review, or back-in-stock journey is a starter template — when you save a new journey with one of these triggers, the [Journey Builder](/help/journey-builder)'s **Templates** picker offers a ready-made flow (**Abandoned cart recovery**, **Win-back lapsed customers**, **Post-delivery review request**, or **Back-in-stock alert**) you can adjust rather than build from scratch.
- Start every journey as **Draft** while you build its steps, then flip **Status** to **Active** once you've checked the emails and delays — nothing enrolls until it's Active.
- Keep **Once per subscriber** on for anything tied to a one-time milestone (signup, first order); turn it off with a sensible cooldown for anything that should repeat, like a post-purchase series.
- Use **Only for segment** to run a different welcome series for a specific audience — e.g. a VIP segment gets a richer sequence than everyone else.
- Set the first step's wait to `0` if you want the first email to go out immediately after the trigger fires, rather than waiting.
- Check the **Journey Enrollments** list after activating a new journey to confirm subscribers are actually being enrolled and advancing through their steps as expected.
- Pausing a journey (**Status: Paused**) stops new enrollments but doesn't cancel subscribers already partway through — they keep receiving their remaining steps.
