---
template_type: affiliate_commission_reversed
category: Affiliate Program
---

# Email Template: affiliate_commission_reversed

## Subject
Commission annulée - Commande n°{{ order_number }}

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
          Commission annulée
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
          La commission pour la commande n°{{ order_number }} ({{ commission_amount }}) a été annulée en raison d'un remboursement client.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Lorsque les clients demandent des remboursements, toutes les commissions associées sont automatiquement annulées pour garantir une comptabilité précise.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Cela fait partie normale du processus d'affiliate. Continuez à promouvoir {{ shop_name }} pour gagner de nouvelles commissions !
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          Voir le tableau de bord des affiliés
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
Commission annulée - Commande n°{{ order_number }}

Bonjour {{ affiliate_name }},

La commission pour la commande n°{{ order_number }} ({{ commission_amount }}) a été annulée en raison d'un remboursement client.

Lorsque les clients demandent des remboursements, toutes les commissions associées sont automatiquement annulées pour garantir une comptabilité précise.

Cela fait partie normale du processus d'affiliate. Continuez à promouvoir {{ shop_name }} pour gagner de nouvelles commissions !

Voir votre tableau de bord : {{ portal_url }}

{{ shop_name }}
Questions ? Contacter {{ support_email }}