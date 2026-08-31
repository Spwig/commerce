---
slug: journey-builder
title_i18n_key: Journey Builder
category: marketing-seo
component: email_marketing
keywords:
  - journey builder
  - visual canvas
  - flowchart
  - drag and drop email automation
  - branch
  - wait step
  - send email step
  - journey template
  - journey export
  - journey import
  - design journey
  - campaign studio
  - automated email flow
  - activate journey
  - journey validation
  - live enrollment counts
  - abandoned cart recovery template
  - win-back template
  - post-delivery review template
  - back-in-stock template
url_patterns:
  - /admin/campaigns/journeys/
published: true
---

<!-- screenshots-needed:
- url: /admin/campaigns/journeys/  (open any journey's builder, click Templates)
  filename: journey-builder-templates.webp
  description: The template picker with all eight starters visible (Welcome series,
    First-order onboarding, Post-purchase & review, VIP vs. standard offer, Abandoned
    cart recovery, Win-back lapsed customers, Post-delivery review request,
    Back-in-stock alert) — replaces the existing four-template screenshot at the same
    path, which is now stale.
  save-to: core/static/core/admin/img/help/journey-builder/
  viewport: 1440x900
-->

The **Journey Builder** is the visual, drag-and-drop canvas where you design what a [Journey](/help/triggered-journeys) actually does — which emails go out, how long to wait between them, and whether different subscribers should follow different paths. Instead of filling in a form, you build the flow as a flowchart: connected boxes on a canvas that you can rearrange, branch, and preview at a glance.

## Opening the builder

Every journey has its own builder canvas. You can reach it two ways:

- Creating a new journey — fill in its **Name**, **Trigger**, and audience on the settings page and click **Save** — drops you straight into the builder so you can start designing immediately.
- Opening an existing journey's settings page and clicking **Design journey** at the top.

The builder is a full-screen workspace with three areas: a **palette** of step types on the left, the **canvas** in the middle, and a **step settings** panel on the right that appears when you select something.

![The Journey Builder canvas showing a welcome series with a Yes/No branch](/static/core/admin/img/help/journey-builder/journey-builder-canvas.webp)

At the top of the canvas, a header repeats the journey's **Trigger** and **audience** (or "All subscribers" if no segment is set) so you always know who you're designing for without leaving the builder. Use the **Back** button to return to the journey's settings page.

## The step types

Drag a step from the left palette onto the canvas, or click a palette item to drop it in automatically. Four step types are available:

| Step | What it does |
|------|--------------|
| **Send email** | Sends one of your campaigns to the subscriber. |
| **Wait** | Pauses for a set number of hours or days before continuing. |
| **Branch** | Splits the path in two — **Yes** or **No** — based on whether the subscriber belongs to a segment you choose. |
| **Exit** | Ends the journey for the subscriber. |

Every journey starts with a single **Entry** step, created automatically the first time you open the builder. It shows the journey's trigger and can't be deleted — it's simply where subscribers enter the flow.

## Connecting steps

Each step has a small circular **port**: one on top (input) and one or more on the bottom (output). To connect two steps, drag from one step's bottom port to another step's top port — a curved line appears linking them.

A **Branch** step has two output ports instead of one: a green **Yes** and a red **No**. Connect each to wherever that path should lead — they can rejoin later at the same step (as in the example above, where both paths lead back to the same **Exit**) or go their separate ways entirely.

To rearrange the layout, drag a step by its body to reposition it — connected lines follow automatically. Drag an empty part of the canvas background to pan around, and use your scroll wheel to zoom in or out. If you lose track of the flow, click **Fit** in the toolbar to re-center and zoom to fit everything on screen.

## Configuring a step

Click any step to open its settings in the right-hand panel:

| Step | Setting |
|------|---------|
| **Send email** | Pick the **Email to send** from a dropdown of your campaigns. |
| **Wait** | Set **Wait for** — a number plus **hours** or **days**. |
| **Branch** | Choose **If subscriber is in segment** — the segment that decides Yes vs. No. |
| **Exit** | No settings — it's just an endpoint. |

![The right-hand panel configuring a Branch step, with the canvas dimmed behind it](/static/core/admin/img/help/journey-builder/journey-builder-branch-config.webp)

Changes save automatically as soon as you pick a value — there's no separate **Save** button on the canvas. Every step except **Entry** has a **Delete step** button at the bottom of its settings panel.

The emails you pick for **Send email** steps are ordinary campaigns you design in Campaign Studio's regular visual builder — subject line, content blocks, everything. Leave them as **Draft** and just choose them from the dropdown here; the journey sends them for you, you never click Send on them yourself.

## Starting from a template

Building a flow from a blank canvas isn't always necessary — click **Templates** in the toolbar (or **Browse templates** on an empty canvas) to open a picker with eight ready-made starters:

| Template | What it builds |
|----------|-----------------|
| **Welcome series** | Greet new subscribers, share what you're about, then a first-order nudge. |
| **First-order onboarding** | Turn a first-time buyer into a repeat customer with a gentle onboarding sequence. |
| **Post-purchase & review** | Say thanks after any order, then ask for a review once it's arrived. |
| **VIP vs. standard offer** | After an order, branches on your VIP segment to send the right follow-up offer to each group. |
| **Abandoned cart recovery** | Remind a shopper who left items behind, then a follow-up nudge a day later. |
| **Win-back lapsed customers** | Re-engage a customer who hasn't bought in a while with a reason to return. |
| **Post-delivery review request** | Ask for a review a few days after an order is marked Delivered. |
| **Back-in-stock alert** | Tell a waiting shopper the moment a product they wanted is available again. |

Each template is pre-wired to the matching trigger — for example, applying **Win-back lapsed customers** to a new journey also expects that journey's **Trigger** to be **Customer lapsed (win-back)**. See [Triggered journeys](/help/triggered-journeys) for what fires each of these trigger events and how the recovery-focused ones behave (idle windows, guest checkout, once-per-order review requests, and how a back-in-stock journey takes over from the plain one-off alert).

![The template picker showing the ready-made starter journeys](/static/core/admin/img/help/journey-builder/journey-builder-templates.webp)

Applying a template **replaces the current flow** on the canvas, so use it at the start of designing a journey rather than partway through. Spwig re-links each step to a real email or segment wherever the names match something you already have; anywhere it can't find a match, the header reports how many steps still need an email or segment chosen so you know exactly what to finish before going live.

## Sharing journeys

Two toolbar buttons let you move a journey's design between steps or between stores:

- **Export** downloads the journey as a `.journey.json` file — a portable description of the flow's shape (its steps, waits, branches, and Yes/No paths) plus the *names* of the emails and segments each step uses. It doesn't include the email designs themselves or any subscriber data.
- **Import** loads a `.journey.json` file into the current journey, replacing what's on the canvas.

This is useful for backing up a flow you're proud of, handing a proven welcome series to another Spwig store, or rebuilding a journey after cloning your store to a new install. As with templates, Spwig re-links emails and segments by name where a match exists on the target store, and flags anything it couldn't match so you can finish the setup.

## Activating your journey

When the flow is ready, use the status control at the top-right of the builder. A pill shows the journey's current status — **Draft**, **Active**, or **Paused** — next to an **Activate** button.

Clicking **Activate** **checks the flow first**. If anything would stop it working, activation is blocked and a banner lists the problems — for example a **Send email** step with no email chosen, a **Branch** with no segment or no Yes/No path, an email or segment that has since been deleted, or a loop that would run forever. Each problem is clickable: selecting it jumps to the offending step, which is outlined in red until you fix it. Warnings (such as an unreachable step or a **Wait** with no delay set) are listed too but don't block activation.

![Activation blocked, with the problem listed in a banner and the offending step outlined in red](/static/core/admin/img/help/journey-builder/journey-builder-activate-blocked.webp)

Once the flow passes, the pill switches to **Active** and the journey begins enrolling subscribers whenever its trigger fires. The button becomes **Pause**, which stops new enrolments — subscribers already partway through keep receiving their remaining steps. See [Triggered journeys](/help/triggered-journeys) for how enrolment, cooldowns, and status interact.

## Seeing who's in the journey

Once a journey is live, each step shows a small **count badge** in its corner: the number of subscribers sitting at that step right now. It's a quick way to see where people are flowing and where they're building up — a large number on a **Wait** step is expected, whereas a pile-up just before a particular email might be worth a look. The counts refresh whenever you return to the builder tab.

![The canvas with live count badges on the steps and the Activate button in the toolbar](/static/core/admin/img/help/journey-builder/journey-builder-live-counts.webp)

## Tips

- Design the flow while it's still a **Draft** — nothing enrolls anyone until you **Activate** it. Activating from the builder runs a quick check first and won't let a broken flow go live, so there's no risk of a half-built journey enrolling subscribers.
- Start from a **Template** even if you plan to heavily customize it — it's faster to edit an existing flow than to build one node by node, and it demonstrates the branch pattern if you haven't used one before.
- After applying a template or importing a file, check the header for an unmatched-steps note and fill in any **Send email** or **Branch** steps it couldn't match before activating.
- Click **Fit** whenever a flow gets wide (branches especially) — it's the fastest way to see the whole shape again after zooming or panning.
- Keep step names easy to scan by keeping each **Wait** step immediately before the email it delays, rather than clustering several waits together.
- **Export** a working journey before making major changes to it — it's a quick way to keep a fallback copy you can re-import if you don't like the result.
