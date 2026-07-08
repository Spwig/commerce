---
template_type: refund_notification
category: Core E-commerce
---

# Email Template: refund_notification

## Subject
İade İşlemi Yapıldı - Sipariş #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          İade İşlemi Yapıldı
        </mj-text>
        <mj-text>
          Sipariş #{{ order_number }} için bir iade işlemi yapıldı.
        </mj-text>
        <mj-text>
          <strong>İade Tutarı:</strong> {{ refund_amount }}
        </mj-text>
        <mj-text>
          İade, hesabınıza {{ refund_days }} iş günü içinde yansıtılacaktır.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
İade İşlemi Yapıldı

Sipariş #{{ order_number }} için bir iade işlemi yapıldı.

İade Tutarı: {{ refund_amount }}

İade, hesabınıza {{ refund_days }} iş günü içinde yansıtılacaktır.