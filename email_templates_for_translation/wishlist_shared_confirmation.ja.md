---
template_type: wishlist_shared_confirmation
category: Wishlist
---

# Email Template: wishlist_shared_confirmation

## Subject
✓ {{ shop_name }} が共有されました

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ✓ ウィッシュリストが成功裏に共有されました！
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          こんにちは、{{ customer_name }}。
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ wishlist_item_count }} 個のアイテムを含むあなたのウィッシュリストが成功裏に共有されました。以下に記載のリンクを使用して、他人が今後あなたのウィッシュリストを閲覧できるようになります。
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              共有リンク:
            </mj-text>
            <mj-text font-family="'Courier New', monospace" font-size="14px" color="{{ theme.color.primary|default:'#2563eb' }}">
              {{ share_url }}
            </mj-text>
            <mj-spacer height="15px" />
            <mj-button href="{{ share_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
              リンクをコピー
            </mj-button>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          共有内容:
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
          • ご設定されたウィッシュリスト名（ある場合）<br/>
          • {{ wishlist_item_count }} 個の商品<br/>
          • 商品名、画像、価格<br/>
          • 各商品の購入リンク
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              💡 友人や家族とプレゼントや特別な場面で共有するのに最適です！
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ wishlist_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          マイウィッシュリストを管理
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          共有を停止したい場合は、いつでもウィッシュリストの <a href="{{ wishlist_settings_url }}">設定</a> で共有リンクを無効にできます。
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ ウィッシュリストが成功裏に共有されました！

こんにちは、{{ customer_name }}。

{{ wishlist_item_count }} 個のアイテムを含むあなたのウィッシュリストが成功裏に共有されました。以下に記載のリンクを使用して、他人が今後あなたのウィッシュリストを閲覧できるようになります。

共有リンク:
{{ share_url }}

共有内容:
• ご設定されたウィッシュリスト名（ある場合）
• {{ wishlist_item_count }} 個の商品
• 商品名、画像、価格
• 各商品の購入リンク

💡 友人や家族とプレゼントや特別な場面で共有するのに最適です！

マイウィッシュリストを管理: {{ wishlist_url }}

共有を停止したい場合は、いつでもウィッシュリストの 設定 で共有リンクを無効にできます: {{ wishlist_settings_url }}