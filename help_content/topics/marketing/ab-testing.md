---
slug: ab-testing
title_i18n_key: A/B Testing
category: marketing-seo
component: email_marketing
keywords:
  - a/b test
  - ab testing
  - split test
  - email split test
  - test subject lines
  - subject line test
  - content test
  - winning variant
  - test winner
  - open rate test
  - click rate test
  - campaign studio
  - compare email variants
  - holdout audience
  - test sample
url_patterns:
  - /admin/campaigns/[0-9a-f-]+/ab-test/
  - /admin/campaigns/ab-test/
  - /admin/campaigns/[0-9a-f-]+/builder/
  - /admin/email_marketing/campaign/
related:
  - audiences
  - recurring-campaigns
  - triggered-journeys
  - campaign-reports
published: true
---

Campaign Studio's **A/B testing** lets you try two to four **variants** — different versions of the same campaign — on a slice of your audience before committing to the full send. Change only the subject line, or design entirely different content for each variant. Spwig splits a sample of your list evenly across the variants, watches how each one performs, and automatically sends the best-performing variant to everyone who didn't see the test.

## Setting up a test

Build your campaign as normal in Campaign Studio's visual builder first — write a subject line, design your content, and choose the **Segment** you want to reach. That campaign becomes the test's **container**. Once you attach an A/B test to it, the container itself is never sent directly — its job is to hold the settings, and the audience it's set to reach is exactly the pool the test runs against.

Two places open the A/B test wizard:

- The **A/B test** button in the visual builder's toolbar.
- The **A/B test** icon on the campaign's card in **Campaign Studio > Campaigns**.

Once a test exists on a campaign, that same button takes you straight to its results instead of the wizard, and the campaign's card picks up a small **A/B** badge so you can spot it in the list at a glance.

## What to test

The wizard's first step asks what should differ between variants:

| Option | What changes | Measured by |
|--------|--------------|-------------|
| **Subject line** | Every variant sends the exact same content — only the subject line differs. The most common test. | Open rate |
| **Content** | Each variant is a separate design that you build yourself in the visual builder. | Click rate |

![The "What do you want to test?" step, with Subject line selected](/static/core/admin/img/help/ab-testing/ab-test-what-to-test.webp)

## Choosing your variants

What you enter next depends on what you picked:

- **Subject line** — type a subject for each variant (2–4). Two rows are shown to start; click **Add another subject** for a third or fourth.
- **Content** — just choose how many variants you want (2–4). Every variant starts as an exact copy of your container's current design, so you only need to change what you're testing.

Either way, Spwig labels the variants **A**, **B**, **C**, and **D** in the order you enter them — you'll see them as "Variant A", "Variant B", and so on from here.

![The Variants step with three subject lines entered for variants A, B, and C](/static/core/admin/img/help/ab-testing/ab-test-variants.webp)

For a content test, you don't design the variants in the wizard itself — after you create the test, each variant's card on the results hub gets a small pencil icon that opens it in the same visual builder you used for the container. This is only available while the test is still in **Draft**; once you start the test, the designs are locked in so what you're measuring doesn't change mid-test.

## Test settings

The wizard's last step covers how the test is run and decided:

| Setting | What it does |
|---------|--------------|
| **Test sample** | The share of your audience used for the test, split evenly across the variants: 20%, 30%, 50%, or 100%. The rest — the **holdout** — receives the winner afterward. Choosing 100% tests your entire list at once, so there's no holdout left to send a winner to. |
| **Winner decided by** | **Open rate** or **Click rate**. Defaults to open rate for a subject-line test and click rate for a content test, since that's what each is really measuring — but you can change it either way. |
| **Test window (hours)** | How long to gather opens and clicks before picking a winner, from 1 to 168 hours (a full week). |
| **Automatically send the winner to the rest of the audience** | On by default. When checked, Spwig emails the winning variant to the holdout as soon as the window ends, with no further action from you. |

A short review card at the bottom recaps your choices before you commit.

![The Settings step with sample, metric, window, and auto-send options set, plus a review card](/static/core/admin/img/help/ab-testing/ab-test-settings.webp)

## Starting the test

Click **Create test** to save the setup — this doesn't send anything yet. You land on the test's results hub in **Draft** status, showing each variant with zero recipients so far and two buttons: **Start test** and **Cancel test**.

![A freshly created test in Draft status, showing three variants ready to start](/static/core/admin/img/help/ab-testing/ab-test-draft.webp)

Click **Start test** when you're ready. Spwig splits your test sample evenly across the variants and emails each one right away — you don't need to do anything else; a background job checks in once the test window has passed and decides the winner on its own. The container campaign's own status stays **Draft** throughout all of this — that's expected, since it's the variants (and later the winner) that actually go out, never the container.

Your audience needs to be large enough that every variant gets a meaningful number of recipients. Spwig blocks starting a test if any variant would end up with zero people, but a test genuinely worth reading needs more than a bare minimum — aim for a few hundred recipients or more before relying on the result.

## While the test runs

Once started, the hub switches to **Testing** and shows "Test running — the winner is decided automatically around" the date and time the window ends. Recipient counts and live open/click rates update on every visit, alongside a bar chart comparing every variant's open rate and click rate side by side — not just whichever metric you picked to decide the winner.

![A running test showing live recipient counts, open/click rates, and a comparison chart](/static/core/admin/img/help/ab-testing/ab-test-running.webp)

You can also keep an eye on every test from the **Campaign Studio dashboard**: its *Recent A/B tests* panel lists your running and recently-decided tests — each with its confidence at a glance — and links straight to the results, alongside cards counting how many tests are running and how many were decided in the last 30 days.

## Reading the results

When the test window ends, Spwig picks the variant with the highest rate on your chosen metric, marks the test **Complete**, and — if **Automatically send the winner** was checked and there's a holdout to send to — emails that variant to everyone who wasn't part of the test. The winning variant's card is outlined and carries a **Winner** badge; the comparison chart stays in place so you can see how the variants compared.

![A completed test with the winning variant highlighted and a Winner badge](/static/core/admin/img/help/ab-testing/ab-test-complete.webp)

Keep in mind the numbers on this page are always for the test sample, not your whole list — with a 20% sample, you're reading how a fifth of your audience responded, not everyone.

## How confident is the result?

A higher open or click rate doesn't always mean a variant is genuinely better — with a small audience, one variant can come out ahead purely by chance. So alongside the winner, Spwig shows **how confident it is that the result is real**, based on the size of the gap and the number of recipients. You'll see one of three readings:

- **A clear result** — Spwig is at least 95% confident the leading variant genuinely beats the others. This is a result you can act on.
- **Too close to call** — there's a leader, but the gap is small enough that it could be chance. The percentage shown is how confident Spwig is, below the 95% mark. Consider re-running with a larger audience or a longer test window before drawing conclusions.
- **Not enough data yet** — too few recipients (or too few opens and clicks) to tell the variants apart at all. This is common on small lists; grow the audience or let the test run longer.

![A completed test showing a clear result — the winning variant carries a confidence badge and the summary reads "statistically clear"](/static/core/admin/img/help/ab-testing/ab-test-confidence.webp)

The same reading appears while a test is still running, so you can watch a result firm up — or not — before the window closes. Because confidence depends heavily on audience size, this is the practical reason to aim for a few hundred or more recipients per test: on a very small list, even a big-looking difference will usually read as "too close to call".

Note that when auto-send is on, Spwig still sends the highest-rate variant to the rest of your audience even if the result is inconclusive — the confidence reading is there to tell you how much to trust the outcome, not to hold up the send.

## Cancelling a test

**Cancel test** is available while a test is in **Draft** or **Testing**, and stops it with no winner ever sent. It's there for when you've changed your mind or made a mistake in the setup — not something to use lightly, since once a test is cancelled (or has completed normally), there's no button to set up a new one on that same campaign. If you want to run another comparison later, build a fresh campaign for it.

## Tips

- Reach for a **Subject line** test first — it's the simplest to set up and the most common reason to A/B test at all.
- Use a **Content** test when you want to compare genuinely different designs or offers, not just wording in the subject.
- Finish designing every variant of a content test — using the pencil icon on each card — before clicking **Start test**. You can't edit a variant's design once the test is running.
- Leave **Test sample** below 100% if you want Spwig to automatically email the winner to the rest of your list afterward — at 100% there's no holdout left for it to reach.
- Give the test window enough time to span your subscribers' normal reading habits (24 hours comfortably covers a full day of time zones and inboxes) rather than deciding a winner off just the first hour or two.
