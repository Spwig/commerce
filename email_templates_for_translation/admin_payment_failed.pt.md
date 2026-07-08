---
template_type: admin_payment_failed
category: Admin Notifications
---

# Email Template: admin_payment_failed

## Subject
Pagamento Falhou - Pedido #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.error|default:'#ef4444' }}">
          Payment Failed
        </mj-text>
        <mj-text>
          A payment attempt has failed for order #{{ order_number }}.
        </mj-text>
        <mj-text>
          <strong>Customer:</strong> {{ customer_name }}
        </mj-text>
        <mj-text>
          <strong>Amount:</strong> {{ order_total }}
        </mj-text>
        <mj-text>
          <strong>Error:</strong> {{ error_message }}
        </mj-text>
        <mj-button href="{{ admin_order_url }}" background-color="{{ theme.color.error|default:'#ef4444' }}">
          View in Admin
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Payment Failed

A payment attempt has failed for order #{{ order_number }}.

Customer: {{ customer_name }}
Amount: {{ order_total }}
Error: {{ error_message }}

View in admin: {{ admin_order_url }}