---
template_type: wishlist_shared_confirmation
category: Wishlist
---

# Email Template: wishlist_shared_confirmation

## Subject
✓ 您的购物清单已分享 - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ✓ 购物清单已成功分享！
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          您的购物清单包含 {{ wishlist_item_count }} 个商品，已成功分享。其他人现在可以使用下面的链接查看您的购物清单。
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              分享链接：
            </mj-text>
            <mj-text font-family="'Courier New', monospace" font-size="14px" color="{{ theme.color.primary|default:'#2563eb' }}">
              {{ share_url }}
            </mj-text>
            <mj-spacer height="15px" />
            <mj-button href="{{ share_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
              复制链接
            </mj-button>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          已分享内容：
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
          • 您的购物清单名称（如已设置）<br/>
          • {{ wishlist_item_count }} 个商品<br/>
          • 商品名称、图片和价格<br/>
          • 每个商品的购买链接
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              💡 适合与朋友和家人分享礼物和特殊场合！
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ wishlist_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          管理我的购物清单
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          想要停止分享？您随时可以在购物清单设置中禁用分享链接。 <a href="{{ wishlist_settings_url }}">购物清单设置</a>.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ 购物清单已成功分享！

Hi {{ customer_name }},

您的购物清单包含 {{ wishlist_item_count }} 个商品，已成功分享。其他人现在可以使用下面的链接查看您的购物清单。

分享链接：
{{ share_url }}

已分享内容：
• 您的购物清单名称（如已设置）
• {{ wishlist_item_count }} 个商品
• 商品名称、图片和价格
• 每个商品的购买链接

💡 适合与朋友和家人分享礼物和特殊场合！

管理我的购物清单：{{ wishlist_url }}

想要停止分享？您随时可以在购物清单设置中禁用分享链接：{{ wishlist_settings_url }}