---
template_type: shipping_confirmation
category: Core E-commerce
---

# Email Template: shipping_confirmation

## Subject
ご注文が発送されました - 注文番号 #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          ご注文が発送されました！
        </mj-text>
        <mj-text>
          よろしいニュースです！注文番号 #{{ order_number }} は発送されました。
        </mj-text>
        <mj-text>
          <strong>追跡番号：</strong>{{ tracking_number }}
        </mj-text>
        <mj-text>
          <strong>配送業者：</strong>{{ carrier }}
        </mj-text>
        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          配送状況を追跡する
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
ご注文が発送されました！

よろしいニュースです！注文番号 #{{ order_number }} は発送されました。

追跡番号：{{ tracking_number }}
配送業者：{{ carrier }}

配送状況を追跡する：{{ tracking_url }}

