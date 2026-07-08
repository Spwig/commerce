---
template_type: payment_confirmation
category: Core E-commerce
---

# Email Template: payment_confirmation

## Subject
Ödeme Onaylandı - Sipariş #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Ödeme Onaylandı
        </mj-text>
        <mj-text>
          Sipariş #{{ order_number }} için ödemeniz başarıyla işlendi.
        </mj-text>
        <mj-text>
          <strong>Ödenen Tutar:</strong> {{ amount_paid }}
        </mj-text>
        <mj-text>
          <strong>Ödeme Yöntemi:</strong> {{ payment_method }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Ödeme Onaylandı

Sipariş #{{ order_number }} için ödemeniz başarıyla işlendi.

Ödenen Tutar: {{ amount_paid }}
Ödeme Yöntemi: {{ payment_method }}