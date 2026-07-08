---
slug: customer-display-promo-slides
title_i18n_key: Customer Display Promo Slides
category: point-of-sale
component: pos_app
keywords:
  - promo slides
  - promotional slides
  - customer display
  - pos display
  - carousel slides
  - customer-facing display
  - idle screen
  - digital signage
  - pos advertising
  - in-store promotions
  - slide carousel
  - promotional content
  - display advertising
  - customer screen
url_patterns:
  - /admin/pos_app/promoslide/
related:
  - pos-system-overview
  - pos-store-groups
  - managing-pos-terminals
published: true
---

Promotional slides display on the customer-facing screen when the POS terminal is idle (no active transaction). Create a carousel of images showcasing seasonal promotions, new product launches, store policies, upcoming events, and loyalty program benefits. Slides can be targeted to specific stores or groups using scope assignment—run holiday promotions only in US stores, or display local event information only at relevant locations. Active slides cycle automatically every 5-10 seconds, creating engaging digital signage that keeps customers informed while waiting.

Use promotional slides to increase awareness of current promotions, educate customers about policies, and drive engagement with loyalty programs and events.

![Promo Slide List](/static/core/admin/img/help/customer-display-promo-slides/promoslide-list.webp)

## Customer Display Behavior

When a POS terminal is idle (no customer at register, no transaction in progress), the customer-facing display shows:

**Carousel Mode**:
- Cycles through all active slides
- Each slide displays for 5-10 seconds (configurable per terminal)
- Smooth fade transitions between slides
- Loops continuously until transaction starts

**During Transaction**:
- Carousel stops immediately
- Display switches to transaction view (items, running total, payment prompts)
- Carousel resumes when transaction completes and terminal returns to idle

**No Slides Configured**:
- Display shows "Welcome" message with store branding
- Static screen (no carousel)

**Technical Requirements**:
- Customer display can be a separate monitor or the same screen as cashier (POS app supports picture-in-picture mode)
- Display syncs via BroadcastChannel API (same-device communication) or WebSocket (separate-device displays)

## Scope Targeting

Like receipt templates, promo slides support scope-based targeting (highest priority to lowest):

| Priority | Scope | Example | Use Case |
|----------|-------|---------|----------|
| **1** | Store-specific | Paris Store slides | Parisian summer festival event slide |
| **2** | Group-specific | European Stores slides | GDPR privacy policy slide for EU only |
| **3** | All Stores | Global slides | "Free shipping on orders >$50" (company-wide promo) |

**How Scope Works**:
- Terminal displays slides matching its store scope (store-specific slides)
- Plus slides matching its group scope (if store is in a group)
- Plus slides with no scope assignment (global slides)
- Result: Store may show 3-5 slides (mix of scoped and global)

**Example**:
- Global slide: "New Loyalty Program - Join Today!" (no scope)
- Group slide: "Memorial Day Sale - 30% Off" (US Stores group only)
- Store slide: "Grand Opening - NYC Flagship" (NYC Store only)

**NYC Store Terminal** displays all 3 slides (store + group + global)
**London Store Terminal** displays only global slide (not in US Stores group, not NYC store)

## Image Requirements

Promo slides are full-screen images optimized for customer display monitors:

**Aspect Ratio**: 16:9 (widescreen)

**Recommended Resolution**: 1920×1080 pixels (Full HD)
- Scales cleanly to most modern displays
- File size balance (quality vs loading speed)

**Accepted Resolutions**:
- Minimum: 1280×720 (HD)
- Optimal: 1920×1080 (Full HD)
- Maximum: 3840×2160 (4K) - not recommended (large file size, slower loading)

**File Format**: JPG, PNG, or WebP
- JPG for photographs
- PNG for graphics with transparency (though backgrounds are recommended)
- WebP for smallest file size

**File Size**: <500KB per slide
- Larger files slow carousel loading
- Compress images before uploading (use Media Library optimization)

**Design Recommendations**:
- High contrast for readability at distance (customers 2-6 feet from display)
- Large text (minimum 48pt for body text, 72pt+ for headlines)
- Bold fonts (thin fonts wash out on some displays)
- Avoid small details (won't be visible from customer vantage point)
- Include call-to-action (what customer should do: "Ask cashier for details", "Sign up today")

## Creating a Promo Slide

Navigate to **POS > Promo Slides** and click **+ Add Promo Slide**:

![Promo Slide Add Form](/static/core/admin/img/help/customer-display-promo-slides/promoslide-add-form.webp)

**Image** - Upload or select from Media Library:
- Click **Browse Media Library** to select existing image
- Or upload new image meeting requirements above
- Preview shows how image will appear on display

**Title** (Optional) - Text overlay at top of slide:
- Max 60 characters (longer text truncates)
- Appears in semi-transparent dark bar at top of image
- Use for slide headline ("Summer Sale", "New Arrivals")
- Leave blank if image includes title text

**Subtitle** (Optional) - Text overlay below title:
- Max 120 characters
- Appears below title in same semi-transparent bar
- Use for supporting details ("Up to 50% off", "Free gift with purchase")
- Leave blank if image is self-contained

**Is Active** - Toggle to enable/disable slide:
- Only active slides appear in carousel
- Use to seasonal activation (turn off after promo ends)
- Deactivating preserves slide for future reactivation

**Sort Order** - Controls slide position in carousel:
- Lower numbers appear earlier in rotation
- Use multiples of 10: 10, 20, 30 (allows inserting slides between existing)
- Example: Holiday sale (sort order 10) displays before general loyalty program (sort order 20)

**Scope Assignment** (Optional):
- **Warehouse** - Select to show only at specific store
- **Store Group** - Select to show only at stores in group
- **Leave both blank** - Shows at all stores (global slide)

## Sort Order and Carousel Flow

**Example Carousel** (NYC Store terminal):
- Slide 1 (sort order 10): "Grand Opening - NYC Flagship" (store-specific)
- Slide 2 (sort order 15): "Memorial Day Sale - 30% Off" (US Stores group)
- Slide 3 (sort order 20): "New Loyalty Program - Join Today!" (global)
- Slide 4 (sort order 30): "Follow us @yourstore" (global)

Carousel loops: 1 → 2 → 3 → 4 → 1 → 2 → ...

**London Store Terminal** (not in US Stores group, different store):
- Slide 1 (sort order 20): "New Loyalty Program - Join Today!" (global)
- Slide 2 (sort order 30): "Follow us @yourstore" (global)

Carousel loops: 1 → 2 → 1 → 2 → ...

Use sort order to prioritize most important content first in rotation.

## Seasonal Activation Strategy

**Problem**: Creating/deleting slides for every seasonal promotion is tedious.

**Solution**: Create slides once, activate/deactivate seasonally:

1. **Create Slides for Major Events**:
   - "Summer Sale" (Is Active: No, created in advance)
   - "Back to School" (Is Active: No, created in advance)
   - "Black Friday" (Is Active: No, created in advance)
   - "Holiday Sale" (Is Active: No, created in advance)

2. **Activate When Relevant**:
   - June 1: Set "Summer Sale" → Is Active: Yes
   - August 15: Set "Summer Sale" → Is Active: No, set "Back to School" → Is Active: Yes
   - November 20: Set "Black Friday" → Is Active: Yes
   - December 1: Set "Black Friday" → Is Active: No, set "Holiday Sale" → Is Active: Yes

3. **Deactivate After Event**:
   - Keeps slide library organized
   - Reuse slides year-over-year (update image if needed, keep configuration)

## Use Case Examples

**Use Case 1: Seasonal Promotion**
- Image: Red background with white text "SUMMER SALE - UP TO 60% OFF"
- Title: "Summer Sale"
- Subtitle: "50-60% off select items. Ask cashier for details."
- Scope: All stores (global)
- Sort order: 10 (highest priority during summer)
- Active: June-August only

**Use Case 2: Store Policy**
- Image: Infographic showing return policy steps
- Title: "Easy Returns"
- Subtitle: "30 days with receipt. No questions asked."
- Scope: All stores (global)
- Sort order: 40 (lower priority than promotions)
- Active: Year-round

**Use Case 3: New Product Launch**
- Image: Hero product shot of new item
- Title: "NEW: Wireless Earbuds Pro"
- Subtitle: "Now available in-store and online. $199.99"
- Scope: All stores (global)
- Sort order: 5 (highest priority during launch week)
- Active: Launch week only, then deactivate

**Use Case 4: Local Event**
- Image: Local charity run poster
- Title: "Support Local"
- Subtitle: "Join us at the Community 5K on June 15!"
- Scope: Specific store (NYC Store only)
- Sort order: 8 (priority for this store)
- Active: 2 weeks before event

**Use Case 5: Loyalty Program**
- Image: Loyalty card visual with point examples
- Title: "Earn Rewards"
- Subtitle: "Join our loyalty program and earn 1 point per $1 spent"
- Scope: All stores (global)
- Sort order: 30 (evergreen content)
- Active: Year-round

## Managing Slides

**Slide List View**:
- Shows all slides with image preview, title, scope, status
- Filter by active/inactive
- Filter by scope (view all global slides, all group slides, etc.)

**Bulk Activation/Deactivation**:
- Select multiple slides in list
- Use admin action to activate or deactivate all at once
- Useful for seasonal transitions (deactivate all summer slides, activate all fall slides)

**Testing Slides**:
- After creating/updating slide, navigate to POS terminal
- Let terminal go idle (no transaction)
- Verify slide appears in carousel
- Check image quality, text overlay readability, timing

**Updating Active Slides**:
- Changes take effect on next carousel refresh (usually <30 seconds)
- No need to restart terminals

## Tips

- **Design for distance** - Customers view display from 2-6 feet away; use large text and high contrast
- **Keep message simple** - Slide displays for <10 seconds; one clear message per slide
- **Use seasonal deactivation** - Create once, toggle on/off yearly rather than recreating
- **Prioritize with sort order** - Most important promotions should have lowest sort order (appear first)
- **Test on actual hardware** - Display color calibration varies; verify slides look good on your specific monitors
- **Limit active slide count** - 3-5 active slides per store is optimal; 10+ slides means each appears infrequently
- **Include CTAs** - Tell customers what to do ("Ask cashier", "Visit website", "Scan QR code on receipt")
- **Update regularly** - Stale promotions (expired sales, past events) reduce customer trust
- **Use scope strategically** - Regional promotions (group scope) and local events (store scope) feel more relevant than constant global content
