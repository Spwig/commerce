---
template_type: back_in_stock_waitlist_confirmation
category: Stock Notifications
---

# Email Template: back_in_stock_waitlist_confirmation

## Subject
✓ {{ product_name }} - {{ shop_name }} のお待ちリストに登録されました

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ✓ お待ちリストに登録されました！
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          こんにちは {{ customer_name }}、
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          ご登録ありがとうございます！この商品が再入荷した moment すぐにご連絡いたします。
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
            <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
              {{ product_description }}
            </mj-text>
            <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}">
              {{ product_price }}
            </mj-text>
            {% if variant_name %}
            <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              バリエーション: {{ variant_name }}
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              💡 <strong>期待すること:</strong><br/>
              このアイテムが再入荷した moment すぐにメールでお知らせします。在庫は限定されていますので、通知を受けた moment すぐに行動してください！
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          お待ちの間...
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          今在庫のある類似商品をご覧ください:
        </mj-text>

        {% for product in similar_products %}
        <mj-spacer height="10px" />
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="4px" padding="12px">
          <mj-column width="25%">
            <mj-image src="{{ product.image }}" alt="{{ product.name }}" border-radius="4px" />
          </mj-column>
          <mj-column width="75%">
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ product.name }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.primary|default:'#2563eb' }}">
              {{ product.price }}
            </mj-text>
            <mj-text font-size="13px">
              <a href="{{ product.url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">商品を確認する →</a>
            </mj-text>
          </mj-column>
        </mj-section>
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          気持ちが変わった場合は？<a href="{{ unsubscribe_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">このお待ちリストから解除</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ お待ちリストに登録されました！

こんにちは {{ customer_name }}、

ご登録ありがとうございます！この商品が再入荷した moment すぐにご連絡いたします。

PRODUCT:
{{ product_name }}
{{ product_description }}
Price: {{ product_price }}
{% if variant_name %}バリエーション: {{ variant_name }}{% endif %}

💡 期待すること:
このアイテムが再入荷した moment すぐにメールでお知らせします。在庫は限定されていますので、通知を受けた moment すぐに行動してください！

WHILE YOU WAIT...
今在庫のある類似商品をご覧ください:
{% for product in similar_products %}
- {{ product.name }} - {{ product.price }}
  {{ product.url }}
{% endfor %}

気持ちが変わった場合は？このお待ちリストから解除: {{ unsubscribe_url }}