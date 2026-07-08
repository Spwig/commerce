---
template_type: affiliate_payout_processing
category: Affiliate Program
---

# Email Template: affiliate_payout_processing

## Subject
Votre paiement de {{ payout_amount }} est en cours de traitement

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="#f8f9fa">
    <!-- Header -->
    <mj-section background-color="#ffffff" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="#212529" align="center">
          💸 Traitement du paiement
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Payout Display -->
    <mj-section background-color="#17a2b8" padding="40px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-bottom="10px">
          Traitement de votre paiement
        </mj-text>
        <mj-text font-size="48px" font-weight="bold" color="#ffffff" align="center" line-height="1">
          {{ payout_amount }}
        </mj-text>
        <mj-text font-size="14px" color="rgba(255, 255, 255, 0.9)" align="center" padding-top="10px">
          ID de paiement : {{ payout_id }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          Bonjour {{ affiliate_name }},
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Bonne nouvelle ! Votre paiement de {{ payout_amount }} est maintenant en cours de traitement.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Les fonds devraient arriver sur votre compte dans les 3 à 5 jours ouvrés. Vous recevrez un autre e-mail lorsque le paiement sera terminé.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Payout Details -->
    <mj-section background-color="#f8f9fa" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          <strong>ID de paiement :</strong> {{ payout_id }}<br/>
          <strong>Montant :</strong> {{ payout_amount }}<br/>
          <strong>Méthode de paiement :</strong> {{ payout_method }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          Voir l'historique des paiements
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          Questions ? <a href="mailto:{{ support_email }}" style="color: #007bff;">Contacter le support</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Votre {{ payout_amount }} paiement est en cours de traitement

Bonjour {{ affiliate_name }},

Bonne nouvelle ! Votre paiement de {{ payout_amount }} est maintenant en cours de traitement.

Détails du paiement :
- ID de paiement : {{ payout_id }}
- Montant : {{ payout_amount }}
- Méthode de paiement : {{ payout_method }}

Les fonds devraient arriver sur votre compte dans les 3 à 5 jours ouvrés. Vous recevrez un autre e-mail lorsque le paiement sera terminé.

Voir l'historique des paiements : {{ portal_url }}

{{ shop_name }}
Questions ? Contacter {{ support_email }}