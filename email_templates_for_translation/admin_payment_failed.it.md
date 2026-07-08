---
template_type: admin_payment_failed
category: Admin Notifications
---

# Email Template: admin_payment_failed

## Subject
Pagamento fallito - Ordine #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.error|default:'#ef4444' }}">
          Pagamento fallito
        </mj-text>
        <mj-text>
          Un tentativo di pagamento è fallito per l'ordine #{{ order_number }}.
        </mj-text>
        <mj-text>
          <strong>Cliente:</strong> {{ customer_name }}
        </mj-text>
        <mj-text>
          <strong>Importo:</strong> {{ order_total }}
        </mj-text>
        <mj-text>
          <strong>Errore:</strong> {{ error_message }}
        </mj-text>
        <mj-button href="{{ admin_order_url }}" background-color="{{ theme.color.error|default:'#ef4444' }}">
          Visualizza nell'amministrazione
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Pagamento fallito

Un tentativo di pagamento è fallito per l'ordine #{{ order_number }}.

Cliente: {{ customer_name }}
Importo: {{ order_total }}
Errore: {{ error_message }}

Visualizza nell'amministrazione: {{ admin_order_url }}