---
template_type: shipping_delayed
category: Shipping
---

# Email Template: shipping_delayed

## Subject
注文番号 #{{ order_number }} の配達の遅延に関するお知らせ

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          注文に関するお知らせ
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          こんにちは、{{ customer_name }}。
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          ご注文の配達に遅延が生じていることをお知らせします。ご不便をおかけして誠に申し訳ございません。ご理解とご協力に感謝いたします。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              注文の詳細:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>注文番号:</strong> {{ order_number }}<br/>
              <strong>当初の到着予定:</strong> {{ original_delivery_date }}<br/>
              <strong>新しい到着予定:</strong> {{ new_delivery_date }}<br/>
              <strong>追跡番号:</strong> {{ tracking_number }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          遅延の理由:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ delay_reason }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          注文の追跡
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          当社は、できるだけ早くご注文をお届けするよう尽力しております。お荷物が発送されたら、もう一度ご連絡いたします。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          ご質問はございませんか？ <a href="{{ support_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">カスタマーサポートチームにお問い合わせください</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
注文番号 #{{ order_number }} のお知らせ

こんにちは、{{ customer_name }}。

ご注文の配達に遅延が生じていることをお知らせします。ご不便をおかけして誠に申し訳ございません。ご理解とご協力に感謝いたします。

注文の詳細:
- 注文番号: {{ order_number }}
- 当初の到着予定: {{ original_delivery_date }}
- 新しい到着予定: {{ new_delivery_date }}
- 追跡番号: {{ tracking_number }}

遅延の理由:
{{ delay_reason }}

注文の追跡: {{ tracking_url }}

当社は、できるだけ早くご注文をお届けするよう尽力しております。お荷物が発送されたら、もう一度ご連絡いたします。

ご質問はございませんか？ カスタマーサポートチームにお問い合わせください: {{ support_url }}

---
このお知らせは、{{ shop_name }} での注文番号 #{{ order_number }} に関するものです。