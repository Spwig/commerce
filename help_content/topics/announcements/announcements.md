---
slug: announcements
title_i18n_key: Announcements
category: promotions
component: announcements
keywords:
  - announcements
  - announcement bar
  - banner
  - promotional banner
  - notification bar
  - store notice
  - header banner
  - modal
  - popup
  - visibility rules
url_patterns:
  - /admin/announcements/announcement/
related:
  - design-themes
  - sales-promotions
published: true
---

Announcements let you display promotional banners and notices on your storefront. They appear in your store's header announcement bar to highlight sales, important updates, or special offers. Announcements can also open a modal popup with detailed content and images when clicked. Navigate to **Marketing > Announcements** in the admin sidebar.

![Announcement list](/static/core/admin/img/help/announcements/announcement-list.webp)

## Announcement List

The announcement page shows all your announcements with:

- **Filter Tabs** — Quick filter by All, Enabled, Disabled, or Expired
- **Search** — Find announcements by title
- **Announcement Cards** — Each announcement with status, link type, modal setting, priority, and last updated time

## Creating an Announcement

1. Click **+ Add Announcement** in the top right
2. Fill in the content fields:
   - **Title** — The main text customers see in the announcement bar (supports bold, italic, and color styling)
   - **Body** — Optional detailed content shown inside the modal popup (leave blank if you are not using a modal)
3. Optionally add an image for the modal popup:
   - **Image** — Select an image from the media library
   - **Image display mode** — **Banner Image** (displayed above the body text) or **Background Image** (displayed behind the text with an overlay)
   - **Image overlay opacity** — Only for background mode: controls how opaque the darkening overlay is (0 = fully transparent, 1 = fully opaque). A value of 0.5 works well for most images.
4. Configure the link:
   - **Link Type** — What happens when customers click the announcement bar:
     - **No Link** — Announcement is informational only
     - **Product** — Links to a specific product page
     - **Category** — Links to a category page
     - **Blog Post** — Links to a blog post
     - **Page** — Links to a page builder page
     - **Custom URL** — Links to any URL
   - **Link Text** — Button label shown inside the modal (e.g., "Shop Now")
   - **Show Modal** — When enabled, clicking the announcement opens a popup with the body content and image instead of navigating directly to the link
5. Configure display settings:
   - **Is Enabled** — Toggle the announcement on or off
   - **Priority** — Controls display order when multiple announcements are active (lower number = shown first)
   - **Expires at** — When the announcement automatically stops displaying (leave blank for no expiry)
6. Optionally configure **Visibility Rules** — restrict when this announcement is shown based on advanced conditions such as customer login status, device type, or date range
7. Click **Save**

## Modal Popups

When **Show Modal** is enabled, clicking the announcement bar opens a modal popup displaying the **Body** content and any attached image. This is useful for:

- Sale announcements with details and a "Shop Now" button
- Policy notices that need more text than fits in the bar
- Promotional popups with a hero image

When **Show Modal** is disabled, clicking the announcement navigates directly to the link URL.

## Multiple Announcements

When multiple announcements are active:
- They **rotate automatically** in the announcement bar on the storefront
- **Priority** controls the display order — lower numbers appear first
- Customers can dismiss individual announcements if the header widget is configured to allow it

## Announcement in the Header

Announcements display through the **Announcement Bar widget** in the Header Builder:

1. Navigate to **Settings > Design & Theme > Header Builder**
2. Add the **Announcement Bar** widget to your header
3. Configure the widget settings:
   - **Auto-rotate speed** — Time between announcement transitions
   - **Show close button** — Whether customers can dismiss it
   - **Animation style** — Slide, fade, or static display

## Tips

- Keep the **Title** short and actionable — "Free shipping on orders over $50!" is better than a long description.
- Use the **Body** field and **Show Modal** together when you need to communicate more detail — for example, showing full sale terms or a featured product image.
- Set **Expires at** so expired promotions disappear automatically without manual cleanup.
- Use **Visibility Rules** to show announcements only to logged-in customers, or only during specific hours.
- Match announcement colors (via the title's color styling) to your store's branding for a professional look.
- Use the **Blog Post** or **Page** link types to drive traffic to supporting content about a promotion.
- Limit active announcements to 2–3 at a time to avoid overwhelming customers.
