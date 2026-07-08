---
template_type: admin_payment_failed
category: Admin Notifications
---

# Email Template: admin_payment_failed

## Subject
Ödeme Başarısız - Sipariş #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.error|default:'#ef4444' }}">
          Ödeme Başarısız
        </mj-text>
        <mj-text>
          Sipariş #{{ order_number }} için bir ödeme denemesi başarısız oldu.
        </mj-text>
        <mj-text>
          <strong>Müşteri:</strong> {{ customer_name }}
        </mj-text>
        <mj-text>
          <strong>Tutar:</strong> {{ order_total }}
        </mj-text>
        <mj-text>
          <strong>Hata:</strong> {{ error_message }}
        </mj-text>
        <mj-button href="{{ admin_order_url }}" background-color="{{ theme.color.error|default:'#ef4444' }}">
          Yönetici Panelinde Görüntüle
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Ödeme Başarısız

Sipariş #{{ order_number }} için bir ödeme denemesi başarısız oldu.

Müşteri: {{ customer_name }}
Tutar: {{ order_total }}
Hata: {{ error_message }}

Yönetici panelinde görüntüle: {{ admin_order_url }}