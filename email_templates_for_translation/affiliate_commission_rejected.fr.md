---
template_type: affiliate_commission_rejected
category: Affiliate Program
---

# Email Template: affiliate_commission_rejected

## Subject
Mise à jour du statut de la commission - Commande n°{{ order_number }}

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
          Mise à jour du statut de la commission
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
          Nous souhaitons vous informer que la commission pour la commande n°{{ order_number }} ({{ commission_amount }}) n’a pas été approuvée.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Cela se produit généralement lorsque commande est annulée ou remboursée avant la fin de la période de commission.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Si vous avez des questions concernant cette commission, veuillez contacter notre équipe de support.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#6c757d" color="#ffffff" href="{{ portal_url }}">
          Voir le tableau de bord Affilié
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          Questions? <a href="mailto:{{ support_email }}" style="color: #007bff;">Contacter le support</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Mise à jour du statut de la commission - Commande n°{{ order_number }}

Bonjour {{ affiliate_name }},

Nous souhaitons vous informer que la commission pour la commande n°{{ order_number }} ({{ commission_amount }}) n’a pas été approuvée.

Cela se produit généralement lorsque commande est annulée ou remboursée avant la fin de la période de commission.

Si vous avez des questions concernant cette commission, veuillez contacter notre équipe de support.

Voir votre tableau de bord : {{ portal_url }}

{{ shop_name }}
Questions ? Contacter {{ support_email }}