---
template_type: order_note_notification
category: Core E-commerce
---

# Email Template: order_note_notification

## Subject
注文 #{{ order_number }} に関するお知らせ

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ご注文に関するお知らせ
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          こんにちは {{ customer_name }}、
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ staff_name }} がご注文 <strong>#{{ order_number }}</strong> にコメントを追加しました:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              {{ note_content }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        {% if order_url %}
        <mj-button href="{{ order_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          注文を確認する
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
ご注文に関するお知らせ

こんにちは {{ customer_name }}、

{{ staff_name }} がご注文 #{{ order_number }} にコメントを追加しました:
---
{{ note_content }}
---

{% if order_url %}注文を確認する: {{ order_url }}{% endif %}

お手伝いが必要ですか？
メール: {{ support_email }}
電話: {{ support_phone }}