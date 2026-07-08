---
template_type: shipping_tracking_milestone
category: Shipping
---

# Email Template: shipping_tracking_milestone

## Subject
ご注文番号 #{{ order_number }} は {{ milestone_status }} - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          配送状況: {{ milestone_status }}
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          こんにちは {{ customer_name }}、
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          良いニュースです！ご注文は、ご届けに至る旅の中で重要なマイルストーンに達しました。
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
              📦 {{ milestone_status }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
              {{ milestone_description }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              注文の詳細:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>注文番号:</strong> {{ order_number }}<br/>
              <strong>追跡番号:</strong> {{ tracking_number }}<br/>
              <strong>配送業者:</strong> {{ carrier_name }}<br/>
              <strong>現在の場所:</strong> {{ current_location }}<br/>
              <strong>予想到着日:</strong> {{ estimated_delivery }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          パッケージの追跡
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          配送に関するご質問は、<a href="{{ support_url }}">サポートにお問い合わせください</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
配送状況: {{ milestone_status }}

こんにちは {{ customer_name }}、

良いニュースです！ご注文は、ご届けに至る旅の中で重要なマイルストーンに達しました。

📦 {{ milestone_status }}
{{ milestone_description }}

注文の詳細:
- 注文番号: {{ order_number }}
- 追跡番号: {{ tracking_number }}
- 配送業者: {{ carrier_name }}
- 現在の場所: {{ current_location }}
- 予想到着日: {{ estimated_delivery }}

パッケージの追跡: {{ tracking_url }}

配送に関するご質問は、サポートにお問い合わせください: {{ support_url }}
