---
template_type: affiliate_payout_cancelled
category: Affiliate Program
---

# Email Template: affiliate_payout_cancelled

## Subject
Pago cancelado - {{ payout_amount }}

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
          Pago cancelado
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          Hola {{ affiliate_name }},
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Su pago de {{ payout_amount }} (ID de pago: {{ payout_id }}) ha sido cancelado.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Si tiene preguntas sobre por qué se canceló este pago, por favor póngase en contacto con nuestro equipo de soporte.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#6c757d" color="#ffffff" href="{{ portal_url }}">
          Ver Panel del Afiliado
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          Preguntas? <a href="mailto:{{ support_email }}" style="color: #007bff;">Contáctenos</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Pago cancelado - {{ payout_amount }}

Hola {{ affiliate_name }},

Su pago de {{ payout_amount }} (ID de pago: {{ payout_id }}) ha sido cancelado.

Si tiene preguntas sobre por qué se canceló este pago, por favor póngase en contacto con nuestro equipo de soporte.

Ver su panel: {{ portal_url }}

{{ shop_name }}
Preguntas? Contáctenos {{ support_email }}