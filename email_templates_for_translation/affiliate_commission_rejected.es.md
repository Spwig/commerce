---
template_type: affiliate_commission_rejected
category: Affiliate Program
---

# Email Template: affiliate_commission_rejected

## Subject
Actualización del estado de comisión - Pedido #{{ order_number }}

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
          Actualización del estado de comisión
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
          Queremos informarte que la comisión del pedido #{{ order_number }} ({{ commission_amount }}) no fue aprobada.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Esto suele ocurrir cuando un pedido se cancela o se devuelve antes de que finalice el período de comisión.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Si tienes preguntas sobre esta comisión, por favor contacta a nuestro equipo de soporte.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#6c757d" color="#ffffff" href="{{ portal_url }}">
          Ver Panel de Afiliado
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          ¿Tienes preguntas? <a href="mailto:{{ support_email }}" style="color: #007bff;">Contáctanos</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Actualización del estado de comisión - Pedido #{{ order_number }}

Hola {{ affiliate_name }},

Queremos informarte que la comisión del pedido #{{ order_number }} ({{ commission_amount }}) no fue aprobada.

Esto suele ocurrir cuando un pedido se cancela o se devuelve antes de que finalice el período de comisión.

Si tienes preguntas sobre esta comisión, por favor contacta a nuestro equipo de soporte.

Ver tu panel: {{ portal_url }}

{{ shop_name }}
¿Tienes preguntas? Contáctanos en {{ support_email }}

