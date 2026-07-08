---
template_type: admin_new_order
category: Admin Notifications
---

# Email Template: admin_new_order

## Subject
Nova encomenda recebida - Encomenda #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Nova encomenda recebida
        </mj-text>
        <mj-text>
          Uma nova encomenda foi colocada na sua loja.
        </mj-text>
        <mj-text>
          <strong>Número da encomenda:</strong> {{ order_number }}
        </mj-text>
        <mj-text>
          <strong>Cliente:</strong> {{ customer_name }}
        </mj-text>
        <mj-text>
          <strong>Total:</strong> {{ order_total }}
        </mj-text>
        <mj-button href="{{ admin_order_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          Ver no administrador
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Nova encomenda recebida

Uma nova encomenda foi colocada na sua loja.

Número da encomenda: {{ order_number }}
Cliente: {{ customer_name }}
Total: {{ order_total }}

Ver no administrador: {{ admin_order_url }}