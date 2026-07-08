---
template_type: affiliate_commission_approved
category: Affiliate Program
---

# Email Template: affiliate_commission_approved

## Subject
Comisión aprobada: {{ commission_amount }}

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
          ✓ Comisión aprobada!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Approval Display -->
    <mj-section background-color="#007bff" padding="40px 20px">
      <mj-column>
        <mj-text font-size="48px" font-weight="bold" color="#ffffff" align="center" line-height="1">
          {{ commission_amount }}
        </mj-text>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-top="10px">
          Aprobada para pago
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
          Su comisión de {{ commission_amount }} de la orden #{{ order_number }} ha sido aprobada y se incluirá en su próximo pago.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Los pagos se procesan según su horario de pago. Recibirá otro correo electrónico cuando se procese el pago.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          Ver Comisiones
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          ¿Tiene preguntas? <a href="mailto:{{ support_email }}" style="color: #007bff;">Contáctenos</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Comisión aprobada: {{ commission_amount }}

Hola {{ affiliate_name }},

Su comisión de {{ commission_amount }} de la orden #{{ order_number }} ha sido aprobada y se incluirá en su próximo pago.

Los pagos se procesan según su horario de pago. Recibirá otro correo electrónico cuando se procese el pago.

Ver comisiones: {{ portal_url }}

{{ shop_name }}
¿Tiene preguntas? Contáctenos en {{ support_email }}