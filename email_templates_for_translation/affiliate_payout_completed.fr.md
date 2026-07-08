---
template_type: affiliate_payout_completed
category: Affiliate Program
---

# Email Template: affiliate_payout_completed

## Subject
✓ Paiement effectué : {{ payout_amount }}

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
          🎉 Paiement Terminé !
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Payout Display -->
    <mj-section background-color="#28a745" padding="40px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-bottom="10px">
          ✓ Paiement réussi
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
          Votre paiement de {{ payout_amount }} a été effectué avec succès !
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Les fonds ont été envoyés à votre méthode de paiement. Selon votre banque ou votre processeur de paiement, cela peut prendre 1 à 2 jours ouvrables pour apparaître sur votre compte.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Merci d'avoir promu {{ shop_name }}. Continuez ainsi !
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          Voir les détails du paiement
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
✓ Paiement effectué : {{ payout_amount }}

Bonjour {{ affiliate_name }},

Votre paiement de {{ payout_amount }} a été effectué avec succès !

Détails du paiement :
- ID de paiement : {{ payout_id }}
- Montant : {{ payout_amount }}
- Méthode de paiement : {{ payout_method }}

Les fonds ont été envoyés à votre méthode de paiement. Selon votre banque ou votre processeur de paiement, cela peut prendre 1 à 2 jours ouvrables pour apparaître sur votre compte.

Merci d'avoir promu {{ shop_name }}. Continuez ainsi !

Voir les détails du paiement : {{ portal_url }}

{{ shop_name }}
Questions ? Contacter {{ support_email }}