---
template_type: affiliate_commission_reversed
category: Affiliate Program
---

# Email Template: affiliate_commission_reversed

## Subject
Comisión revertida - Orden #{{ order_number }}

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
          Comisión revertida
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
          La comisión de la orden #{{ order_number }} ({{ commission_amount }}) ha sido revertida debido a un reembolso del cliente.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Cuando los clientes solicitan reembolsos, cualquier comisión asociada se revierte automáticamente para garantizar una contabilidad precisa.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Esto es parte normal del proceso de afiliado. Continúe promoviendo {{ shop_name }} para ganar nuevas comisiones.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          Ver Panel de Afiliado
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          ¿Tiene preguntas? <a href="mailto:{{ support_email }}" style="color: #007bff;">Contactar soporte</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Comisión revertida - Orden #{{ order_number }}

Hola {{ affiliate_name }},

La comisión de la orden #{{ order_number }} ({{ commission_amount }}) ha sido revertida debido a un reembolso del cliente.

Cuando los clientes solicitan reembolsos, cualquier comisión asociada se revierte automáticamente para garantizar una contabilidad precisa.

Esto es parte normal del proceso de afiliado. Continúe promoviendo {{ shop_name }} para ganar nuevas comisiones.

Ver su panel: {{ portal_url }}

{{ shop_name }}
¿Tiene preguntas? Contacte {{ support_email }}