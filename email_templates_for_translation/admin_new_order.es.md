---
template_type: admin_new_order
category: Admin Notifications
---

# Email Template: admin_new_order

## Subject
Nueva orden recibida - Número de orden #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Nueva orden recibida
        </mj-text>
        <mj-text>
          Se ha realizado una nueva orden en tu tienda.
        </mj-text>
        <mj-text>
          <strong>Número de orden:</strong> {{ order_number }}
        </mj-text>
        <mj-text>
          <strong>Cliente:</strong> {{ customer_name }}
        </mj-text>
        <mj-text>
          <strong>Total:</strong> {{ order_total }}
        </mj-text>
        <mj-button href="{{ admin_order_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          Ver en administrador
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Nueva orden recibida

Se ha realizado una nueva orden en tu tienda.

Número de orden: {{ order_number }}
Cliente: {{ customer_name }}
Total: {{ order_total }}

Ver en administrador: {{ admin_order_url }}
