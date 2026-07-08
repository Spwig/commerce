---
template_type: payment_confirmation
category: Core E-commerce
---

# Email Template: payment_confirmation

## Subject
Paiement confirmé - Commande n°{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Paiement confirmé
        </mj-text>
        <mj-text>
          Votre paiement pour la commande n°{{ order_number }} a été traité avec succès.
        </mj-text>
        <mj-text>
          <strong>Montant payé :</strong> {{ amount_paid }}
        </mj-text>
        <mj-text>
          <strong>Méthode de paiement :</strong> {{ payment_method }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Paiement confirmé

Votre paiement pour la commande n°{{ order_number }} a été traité avec succès.

Montant payé : {{ amount_paid }}
Méthode de paiement : {{ payment_method }}