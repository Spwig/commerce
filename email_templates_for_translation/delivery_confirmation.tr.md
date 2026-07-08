---
template_type: delivery_confirmation
category: Core E-commerce
---

# Email Template: delivery_confirmation

## Subject
Sipariş Teslim Edildi - Sipariş #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Sipariş Teslim Edildi
        </mj-text>
        <mj-text>
          Siparişiniz #{{ order_number }} teslim edildi!
        </mj-text>
        <mj-text>
          Alışverişi keyifli bulmanızı umuyoruz. Herhangi bir sorunuz veya endişeniz varsa, lütfen bize başvurmaktan çekinmeyin.
        </mj-text>
        <mj-button href="{{ order_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          Siparişi Görüntüle
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Sipariş Teslim Edildi

Siparişiniz #{{ order_number }} teslim edildi!

Alışverişi keyifli bulmanızı umuyoruz. Herhangi bir sorunuz veya endişeniz varsa, lütfen bize başvurmaktan çekinmeyin.

Siparişi Görüntüle: {{ order_url }}

