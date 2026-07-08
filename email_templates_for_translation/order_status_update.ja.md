---
template_type: order_status_update
category: Core E-commerce
---

# Email Template: order_status_update

## Subject
注文 #{{ order_number }} - ステータス更新: {{ new_status_display }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          注文ステータス更新
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#6b7280' }}">
          注文 #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          こんにちは {{ customer_name }}、
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          あなたの注文 <strong>#{{ order_number }}</strong> のステータスが更新されました。
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>以前のステータス:</strong> {{ old_status_display }}<br/>
              <strong>新しいステータス:</strong> {{ new_status_display }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

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
注文ステータス更新 - 注文 #{{ order_number }}

こんにちは {{ customer_name }}、

あなたの注文 #{{ order_number }} のステータスが更新されました。

以前のステータス: {{ old_status_display }}
新しいステータス: {{ new_status_display }}

{% if order_url %}注文の詳細: {{ order_url }}{% endif %}