---
template_type: affiliate_commission_rejected
category: Affiliate Program
---

# Email Template: affiliate_commission_rejected

## Subject
Aggiornamento stato commissione - Ordine #{{ order_number }}

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
          Aggiornamento stato commissione
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
          Ti volevamo informare che la commissione per l'ordine #{{ order_number }} ({{ commission_amount }}) non è stata approvata.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Questo accade di solito quando un ordine viene annullato o rimborsato prima che termini il periodo di commissione.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Se hai domande su questa commissione, contatta il nostro team di supporto.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#6c757d" color="#ffffff" href="{{ portal_url }}">
          Visualizza il pannello dell'affiliato
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          Hai domande? <a href="mailto:{{ support_email }}" style="color: #007bff;">Contatta il supporto</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Aggiornamento stato commissione - Ordine #{{ order_number }}

Ciao {{ affiliate_name }},

Ti volevamo informare che la commissione per l'ordine #{{ order_number }} ({{ commission_amount }}) non è stata approvata.

Questo accade di solito quando un ordine viene annullato o rimborsato prima che termini il periodo di commissione.

Se hai domande su questa commissione, contatta il nostro team di supporto.

Visualizza il pannello dell'affiliato: {{ portal_url }}

{{ shop_name }}
Hai domande? Contatta {{ support_email }}
