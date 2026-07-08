# Social Share Buttons - Merchant Guide

## Overview

Social share buttons are **automatically enabled** on your store, allowing customers to share your products on social media. Every share is tracked and customers earn loyalty badges for sharing!

## Accessing Settings

1. Log in to your admin panel
2. Go to **Social Sharing → Social Sharing Settings**
3. Configure where and how share buttons appear

## Configuration Options

### Automatic Placement

Control where social share buttons appear automatically:

- **Enable on Products** ✅ (Default: ON)
  - Share buttons appear on every product detail page
  - Customers can share products on Facebook, Twitter, LinkedIn, etc.

- **Enable on Categories** (Default: OFF)
  - Share buttons appear on category pages

- **Enable on Blog Posts** ✅ (Default: ON)
  - Share buttons appear on blog posts

- **Enable on Custom Pages** (Default: OFF)
  - Share buttons appear on your custom pages

### Placement Position

Choose where buttons appear on the page:

- **Below Content** (Default) - After product description
- **Above Content** - Before product description
- **Sidebar** - In the page sidebar
- **Floating** - Sticky buttons that follow scrolling

### Display Options

- **Show Share Counts** ✅ (Default: ON)
  - Display how many times content has been shared
  - "45 shares on Facebook", etc.

- **Track Shares** ✅ (Default: ON)
  - Track share events for analytics
  - Award loyalty badges automatically (5, 20, 50 shares)

## Supported Platforms

Your customers can share on:

- 📘 **Facebook**
- 🐦 **Twitter/X**
- 💼 **LinkedIn**
- 📌 **Pinterest**
- 💬 **WhatsApp**
- ✈️ **Telegram**
- ✉️ **Email**

## Loyalty Integration

When customers share your content, they automatically earn loyalty badges:

- **Social Butterfly** - Share 5 items (+100 points)
- **Social Advocate** - Share 20 items (+400 points)
- **Brand Ambassador** - Share 50 items (+1000 points)

No configuration needed - badges are awarded automatically!

## Advanced Configuration

### Widget Configuration

Click "Widget Configuration" to customize:

- **Widget Slug**: Which widget package to use (default: social_share_buttons)
- **Default Config**: JSON configuration for button style, size, etc.
- **Enabled Platforms**: Limit which platforms are available

Example custom config:
```json
{
  "display_style": "circular",
  "button_size": "large",
  "orientation": "vertical"
}
```

Available styles:
- `rounded` - Rounded buttons (default)
- `square` - Square buttons
- `circular` - Circular icons only
- `text` - Text links

Available sizes:
- `small`
- `medium` (default)
- `large`

## Template Integration (Advanced)

If you have custom templates, you can manually place share buttons:

```django
{% load social_share_tags %}

{# On product detail page #}
{% social_share_buttons content_type='product' object_id=product.id %}

{# With custom share text and image #}
{% social_share_buttons
    content_type='product'
    object_id=product.id
    share_title=product.name
    share_description=product.short_description
    share_image=product.main_image.url %}
```

## Analytics

View social sharing analytics in **Social Sharing** section:

- **Social Shares** - View all share events
  - Filter by platform, date, content type
  - See which customers are sharing

- **Share Counts** - View aggregated statistics
  - Total shares per product/page
  - Platform breakdown

## Best Practices

1. **Keep it Enabled on Products** - Product shares drive new customers
2. **Show Share Counts** - Social proof encourages more sharing
3. **Track Shares** - Understand what content resonates
4. **Check Analytics Monthly** - See which products get shared most
5. **Promote Loyalty Badges** - Mention badges in marketing to encourage sharing

## Troubleshooting

**Q: Share buttons not appearing?**
- Check that "Enable on Products" is turned ON in settings
- Verify the social_share_buttons widget is installed
- Check your theme supports widget placements

**Q: Share counts not updating?**
- Counts update in real-time when customers share
- Check "Track Shares" is enabled in settings

**Q: Badges not awarded?**
- Badges are only awarded to logged-in customers
- Check customer's loyalty member status
- View "Loyalty → Member Badges" to confirm

**Q: Want to change button appearance?**
- Go to Social Sharing Settings → Widget Configuration
- Add display_style, button_size, or orientation to Default Config

## Support

For technical support or questions:
- Contact your platform administrator
- Check platform documentation
- Visit https://updates.spwig.com for updates

---

**Remember**: Social sharing is powerful marketing - every share is free advertising and brings new customers to your store!
