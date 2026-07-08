---
template_type: order_cancelled
category: Core E-commerce
---

# Email Template: order_cancelled

## Subject
ご注文 #{{ order_number }} がキャンセルされました

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          注文がキャンセルされました
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          こんにちは {{ customer_name }}、
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          ご注文 <strong>#{{ order_number }}</strong> がキャンセルされました。
        </mj-text>

        {% if cancellation_reason %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>理由:</strong> {{ cancellation_reason }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          支払いが行われた場合、元の支払い方法に基づいて返金が処理されます。
        </mj-text>

        <mj-spacer height="30px" />

        {% if order_url %}
        <mj-button href="{{ order_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          注文の詳細を表示
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
注文がキャンセルされました

こんにちは {{ customer_name }},

ご注文 #{{ order_number }} がキャンセルされました。

{% if cancellation_reason %}理由: {{ cancellation_reason }}{% endif %}

支払いが行われた場合、元の支払い方法に基づいて返金が処理されます。

{% if order_url %}注文の詳細: {{ order_url }}{% endif %}

このキャンセルについてご質問はありますか？
メール: {{ support_email }}
電話: {{ support_phone }}