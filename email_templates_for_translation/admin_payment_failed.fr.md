---
template_type: admin_payment_failed
category: Admin Notifications
---

# Email Template: admin_payment_failed

## Subject
Paiement échoué - Commande n°{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.error|default:'#ef4444' }}">
          Paiement échoué
        </mj-text>
        <mj-text>
          Un tentative de paiement a échoué pour la commande n°{{ order_number }}.
        </mj-text>
        <mj-text>
          <strong>Client:</strong> {{ customer_name }}
        </mj-text>
        <mj-text>
          <strong>Montant:</strong> {{ order_total }}
        </mj-text>
        <mj-text>
          <strong>Erreur:</strong> {{ error_message }}
        </mj-text>
        <mj-button href="{{ admin_order_url }}" background-color="{{ theme.color.error|default:'#ef4444' }}">
          Voir dans l'administration
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Paiement échoué

Un tentative de paiement a échoué pour la commande n°{{ order_number }}.

Client: {{ customer_name }}
Montant: {{ order_total }}
Erreur: {{ error_message }}

Voir dans l'administration: {{ admin_order_url }}