---
template_type: delivery_confirmation
category: Core E-commerce
---

# Email Template: delivery_confirmation

## Subject
配達済み - 注文番号 #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          配達済み
        </mj-text>
        <mj-text>
          注文番号 #{{ order_number }} が届けられました！
        </mj-text>
        <mj-text>
          ご購入をお楽しみください。ご質問やご不安があれば、どうぞお気軽にお問い合わせください。
        </mj-text>
        <mj-button href="{{ order_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          注文を確認する
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
配達済み

注文番号 #{{ order_number }} が届けられました！

ご購入をお楽しみください。ご質問やご不安があれば、どうぞお気軽にお問い合わせください。

注文を確認する: {{ order_url }}