---
template_type: refund_notification
category: Core E-commerce
---

# Email Template: refund_notification

## Subject
Rimborso Processato - Ordine #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Rimborso Processato
        </mj-text>
        <mj-text>
          È stato processato un rimborso per l'ordine #{{ order_number }}.
        </mj-text>
        <mj-text>
          <strong>Importo del Rimborso:</strong> {{ refund_amount }}
        </mj-text>
        <mj-text>
          L'importo del rimborso apparirà nel tuo account entro {{ refund_days }} giorni lavorativi.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Rimborso Processato

È stato processato un rimborso per l'ordine #{{ order_number }}.

Importo del Rimborso: {{ refund_amount }}

L'importo del rimborso apparirà nel tuo account entro {{ refund_days }} giorni lavorativi.