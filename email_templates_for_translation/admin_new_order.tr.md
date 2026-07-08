---
template_type: admin_new_order
category: Admin Notifications
---

# Email Template: admin_new_order

## Subject
Yeni Sipariş Alındı - Sipariş #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Yeni Sipariş Alındı
        </mj-text>
        <mj-text>
          Mağazanıza yeni bir sipariş verildi.
        </mj-text>
        <mj-text>
          <strong>Sipariş Numarası:</strong> {{ order_number }}
        </mj-text>
        <mj-text>
          <strong>Müşteri:</strong> {{ customer_name }}
        </mj-text>
        <mj-text>
          <strong>Toplam:</strong> {{ order_total }}
        </mj-text>
        <mj-button href="{{ admin_order_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          Yönetici Panelinde Görüntüle
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Yeni Sipariş Alındı

Mağazanıza yeni bir sipariş verildi.

Sipariş Numarası: {{ order_number }}
Müşteri: {{ customer_name }}
Toplam: {{ order_total }}

Yönetici Panelinde Görüntüle: {{ admin_order_url }}