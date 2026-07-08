---
template_type: affiliate_payout_cancelled
category: Affiliate Program
---

# Email Template: affiliate_payout_cancelled

## Subject
Pagamento annullato - {{ payout_amount }}

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
          Pagamento Annullato
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          Ciao {{ affiliate_name }},
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Il tuo pagamento di {{ payout_amount }} (ID pagamento: {{ payout_id }}) \è stato annullato.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Se hai domande su perché questo pagamento \è stato annullato, per favore contatta il nostro team di supporto.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#6c757d" color="#ffffff" href="{{ portal_url }}">
          Visualizza il Pannello dell'Affiliato
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          Domande? <a href="mailto:{{ support_email }}" style="color: #007bff;">Contatta il Supporto</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Pagamento annullato - {{ payout_amount }}

Ciao {{ affiliate_name }},

Il tuo pagamento di {{ payout_amount }} (ID pagamento: {{ payout_id }}) \è stato annullato.

Se hai domande su perché questo pagamento \è stato annullato, per favore contatta il nostro team di supporto.

Visualizza il pannello affiliati: {{ portal_url }}

{{ shop_name }}
Domande? Contatta {{ support_email }}