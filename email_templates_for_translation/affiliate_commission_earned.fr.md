---
template_type: affiliate_commission_earned
category: Affiliate Program
---

# Email Template: affiliate_commission_earned

## Subject
🎉 Vous avez gagné une commission de {{ commission_amount }} !

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
          💰 Commission Earned!
        </mj-text>
        <mj-text font-size="18px" color="#6c757d" align="center">
          Great news from {{ shop_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Commission Display -->
    <mj-section background-color="#28a745" padding="40px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-bottom="10px">
          💵 Votre Commission
        </mj-text>
        <mj-text font-size="48px" font-weight="bold" color="#ffffff" align="center" line-height="1">
          {{ commission_amount }}
        </mj-text>
        <mj-text font-size="14px" color="rgba(255, 255, 255, 0.9)" align="center" padding-top="10px">
          From Order #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          Hi {{ affiliate_name }},
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Félicitations ! Vous avez gagné une commission de {{ commission_amount }} provenant de la commande #{{ order_number }}.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Continuez à promouvoir {{ shop_name }} pour gagner plus de commissions. Plus vous générez de ventes, plus vous gagnez !
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Commission Details -->
    <mj-section background-color="#f8f9fa" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          <strong>Order Number:</strong> #{{ order_number }}<br/>
          <strong>Commission Amount:</strong> {{ commission_amount }}<br/>
          <strong>Commission Rate:</strong> {{ commission_rate }}%
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          View Affiliate Dashboard
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          Questions ? <a href="mailto:{{ support_email }}" style="color: #007bff;">Contactez le support</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Vous avez gagné une commission de {{ commission_amount }} !

Bonjour {{ affiliate_name }},

Félicitations ! Vous avez gagné une commission de {{ commission_amount }} provenant de la commande #{{ order_number }}.

Détails de la commission :
- Numéro de commande : #{{ order_number }}
- Montant de la commission : {{ commission_amount }}
- Taux de commission : {{ commission_rate }}%

Continuez à promouvoir {{ shop_name }} pour gagner plus de commissions.

Voir votre tableau de bord : {{ portal_url }}

{{ shop_name }}
Questions ? Contactez {{ support_email }}