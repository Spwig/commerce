---
template_type: order_shipped
category: Core E-commerce
---

# Email Template: order_shipped

## Subject
注文 #{{ order_number }} が発送されました！

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          📦 注文が発送されました！
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          配送中です！
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          こんにちは {{ customer_name }}、
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          良いニュースです！あなたの注文は発送され、あなたのところへ配送されています。
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              配送詳細:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>注文 #:</strong> {{ order_number }}<br/>
              <strong>追跡 #:</strong> {{ tracking_number }}<br/>
              <strong>運送会社:</strong> {{ carrier_name }}<br/>
              <strong>予想到着日:</strong> {{ estimated_delivery }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          パッケージを追跡する
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📦 注文が発送されました！

配送中です！

こんにちは {{ customer_name }}、

良いニュースです！あなたの注文は発送され、あなたのところへ配送されています。

配送詳細:
- 注文 #: {{ order_number }}
- 追跡 #: {{ tracking_number }}
- 運送会社: {{ carrier_name }}
- 予想到着日: {{ estimated_delivery }}

パッケージを追跡する: {{ tracking_url }}