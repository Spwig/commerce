---
template_type: wishlist_shared_confirmation
category: Wishlist
---

# Email Template: wishlist_shared_confirmation

## Subject
✓ Your wishlist has been shared - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ✓ Wishlist Shared Successfully!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Your wishlist with {{ wishlist_item_count }} item{{ wishlist_item_count|pluralize }} has been shared successfully. Others can now view your wishlist using the link below.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Share Link:
            </mj-text>
            <mj-text font-family="'Courier New', monospace" font-size="14px" color="{{ theme.color.primary|default:'#2563eb' }}">
              {{ share_url }}
            </mj-text>
            <mj-spacer height="15px" />
            <mj-button href="{{ share_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
              Copy Link
            </mj-button>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          What's Shared:
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
          • Your wishlist name (if set)<br/>
          • {{ wishlist_item_count }} product{{ wishlist_item_count|pluralize }}<br/>
          • Product names, images, and prices<br/>
          • Purchase links for each item
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              💡 Perfect for sharing with friends and family for gifts and special occasions!
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ wishlist_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          Manage My Wishlist
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Want to stop sharing? You can disable the share link anytime in your <a href="{{ wishlist_settings_url }}">wishlist settings</a>.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ WISHLIST SHARED SUCCESSFULLY!

Hi {{ customer_name }},

Your wishlist with {{ wishlist_item_count }} item{{ wishlist_item_count|pluralize }} has been shared successfully. Others can now view your wishlist using the link below.

SHARE LINK:
{{ share_url }}

WHAT'S SHARED:
• Your wishlist name (if set)
• {{ wishlist_item_count }} product{{ wishlist_item_count|pluralize }}
• Product names, images, and prices
• Purchase links for each item

💡 Perfect for sharing with friends and family for gifts and special occasions!

Manage my wishlist: {{ wishlist_url }}

Want to stop sharing? You can disable the share link anytime in your wishlist settings: {{ wishlist_settings_url }}

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| customer_name | Customer's first name | Sarah |
| wishlist_item_count | Number of items | 12 |
| share_url | Public wishlist URL | https://shop.com/en/wishlist/shared/abc123xyz |
| wishlist_url | Private wishlist page | https://shop.com/en/account/wishlist |
| wishlist_settings_url | Settings page | https://shop.com/en/account/wishlist/settings |
| shop_name | Store name | Amazing Shop |

## Notes

- Confirmation email after wishlist sharing
- Transactional email - always sent
- Provides shareable link
- Explains what's visible to others
- Privacy reassurance (can disable anytime)
- Use case: gift registries, wishlists for occasions
