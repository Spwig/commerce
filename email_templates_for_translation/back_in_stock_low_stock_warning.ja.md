---
template_type: back_in_stock_low_stock_warning
category: Stock Notifications
---

# Email Template: back_in_stock_low_stock_warning

## Subject
⚠️ {{ product_name }} が戻りましたが在庫は限定です！- {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ 在庫限定 - お早めに！
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          {{ product_name }} が在庫に戻りました！
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          こんにちは {{ customer_name }}、
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          グッドラック！待ってた商品が在庫に戻りました。しかし急いでください - 在庫は {{ stock_remaining }} 個 {{ stock_remaining|pluralize }} だけです！
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
            <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}">
              {{ product_price }}
            </mj-text>
            {% if variant_name %}
            <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              バリエーション: {{ variant_name }}
            </mj-text>
            {% endif %}
            <mj-spacer height="10px" />
            <mj-text font-size="14px" color="#dc2626" font-weight="bold">
              ⚠️ 在庫 {{ stock_remaining }} 個だけです！
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ product_url }}" background-color="#dc2626" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          在庫がなくなる前に今すぐ購入
        </mj-button>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#991b1b" align="center">
              🔥 <strong>この商品は過去1か月で {{ times_sold_out }} 回 {{ times_sold_out|pluralize }} 売切れしました！</strong><br/>
              再び見逃さないでください - 在庫がなくなる前に今すぐ注文してください。
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          関心がなくなった場合は、<a href="{{ unsubscribe_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">この通知から購読を解除</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ 在庫限定 - お早めに！

{{ product_name }} が在庫に戻りました！

こんにちは {{ customer_name }}、

グッドラック！待ってた商品が在庫に戻りました。しかし急いでください - 在庫は {{ stock_remaining }} 個 {{ stock_remaining|pluralize }} だけです！

PRODUCT:
{{ product_name }}
{{ product_description }}
Price: {{ product_price }}
{% if variant_name %}バリエーション: {{ variant_name }}{% endif %}

⚠️ 在庫 {{ stock_remaining }} 個だけです！

在庫がなくなる前に今すぐ購入: {{ product_url }}

🔥 この商品は過去1か月で {{ times_sold_out }} 回 {{ times_sold_out|pluralize }} 売切れしました！
再び見逃さないでください - 在庫がなくなる前に今すぐ注文してください。

関心がなくなった場合は、購読を解除: {{ unsubscribe_url }}