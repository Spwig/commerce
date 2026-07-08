---
template_type: refund_notification
category: Core E-commerce
---

# Email Template: refund_notification

## Subject
Remboursement traité - Commande n°{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Remboursement traité
        </mj-text>
        <mj-text>
          Un remboursement a été traité pour la commande n°{{ order_number }}.
        </mj-text>
        <mj-text>
          <strong>Montant du remboursement :</strong> {{ refund_amount }}
        </mj-text>
        <mj-text>
          Le remboursement apparaîtra sur votre compte dans {{ refund_days }} jours ouvrés.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Remboursement traité

Un remboursement a été traité pour la commande n°{{ order_number }}.

Montant du remboursement : {{ refund_amount }}

Le remboursement apparaîtra sur votre compte dans {{ refund_days }} jours ouvrés.