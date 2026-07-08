---
template_type: payment_confirmation
category: Core E-commerce
---

# Email Template: payment_confirmation

## Subject
Pagamento confermato - Ordine #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Pagamento confermato
        </mj-text>
        <mj-text>
          Il pagamento per l'ordine #{{ order_number }} è stato elaborato con successo.
        </mj-text>
        <mj-text>
          <strong>Importo pagato:</strong> {{ amount_paid }}
        </mj-text>
        <mj-text>
          <strong>Metodo di pagamento:</strong> {{ payment_method }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Pagamento confermato

Il pagamento per l'ordine #{{ order_number }} è stato elaborato con successo.

Importo pagato: {{ amount_paid }}
Metodo di pagamento: {{ payment_method }}
