---
template_type: wishlist_shared_confirmation
category: Wishlist
---

# Email Template: wishlist_shared_confirmation

## Subject
✓ 您的願望清單已分享 - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ✓ 億願望清單已成功分享！
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          您的願望清單包含 {{ wishlist_item_count }} 項產品已成功分享。其他人現在可以使用以下鏈接查看您的願望清單。
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              分享連結：
            </mj-text>
            <mj-text font-family="'Courier New', monospace" font-size="14px" color="{{ theme.color.primary|default:'#2563eb' }}">
              {{ share_url }}
            </mj-text>
            <mj-spacer height="15px" />
            <mj-button href="{{ share_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
              複製連結
            </mj-button>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          已分享的內容：
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
          • 您的願望清單名稱（如果設置了）<br/>
          • {{ wishlist_item_count }} 產品{{ wishlist_item_count|pluralize }}<br/>
          • 產品名稱、圖片和價格<br/>
          • 每個項目的購買連結
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              💡 為了禮物和特殊場合，與朋友和家人分享的完美選擇！
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ wishlist_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          管理我的願望清單
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          想要停止分享？您可以在願望清單設定中隨時禁用分享連結：<a href="{{ wishlist_settings_url }}">願望清單設定</a>。
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ 億願望清單已成功分享！

Hi {{ customer_name }},

您的願望清單包含 {{ wishlist_item_count }} 項產品已成功分享。其他人現在可以使用以下鏈接查看您的願望清單。

分享連結：
{{ share_url }}

已分享的內容：
• 您的願望清單名稱（如果設置了）
• {{ wishlist_item_count }} 產品{{ wishlist_item_count|pluralize }}
• 產品名稱、圖片和價格
• 每個項目的購買連結

💡 為了禮物和特殊場合，與朋友和家人分享的完美選擇！

管理我的願望清單：{{ wishlist_url }}

想要停止分享？您可以在願望清單設定中隨時禁用分享連結：{{ wishlist_settings_url }}