---
template_type: wishlist_price_drop
category: Wishlist
---

# Email Template: wishlist_price_drop

## Subject
🔥 価格が下がりました！{{ product_name }}は現在{{ discount_percentage }}％割引！

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          🔥 価格が下がりました！
        </mj-text>
        <mj-text font-size="18px" color="#047857" align="center">
          ワishlistの商品で{{ discount_percentage }}％割引！
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ラッキーアクセント、{{ customer_name }}！
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          ウォッチリストの商品が価格が下がりました！この機会を逃さないでください。
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column width="35%">
            <mj-image src="{{ product_image }}" alt="{{ product_name }}" border-radius="8px" />
          </mj-column>
          <mj-column width="65%">
            <mj-text font-weight="bold" font-size="18px" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ product_name }}
            </mj-text>
            <mj-spacer height="10px" />
            <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              元の価格: <span style="text-decoration: line-through;">{{ original_price }}</span>
            </mj-text>
            <mj-text font-size="24px" font-weight="bold" color="#059669">
              今: {{ new_price }}
            </mj-text>
            <mj-text font-size="16px" font-weight="bold" color="#dc2626">
              {{ savings_amount }}節約 ({{ discount_percentage }}％割引)
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ product_url }}" background-color="#059669" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          今すぐ購入して{{ discount_percentage }}％節約
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#991b1b" align="center">
              ⏰ <strong>限定時間:</strong> このセールは永遠には続きません。いつでも価格が戻る可能性があります！
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          ウォッチリストから削除: <a href="{{ remove_wishlist_url }}">こちらをクリック</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🔥 価格が下がりました！
{{ discount_percentage }}％割引でウォッチリストの商品を節約

ラッキーアクセント、{{ customer_name }}！

ウォッチリストの商品が価格が下がりました！この機会を逃さないでください。

{{ product_name }}
元の価格: {{ original_price }}
今: {{ new_price }}
{{ savings_amount }}節約 ({{ discount_percentage }}％割引)

今すぐ購入して{{ discount_percentage }}％節約: {{ product_url }}

⏰ 限定時間: このセールは永遠には続きません。いつでも価格が戻る可能性があります！

ウォッチリストから削除: {{ remove_wishlist_url }}