---
template_type: affiliate_account_approved
category: Affiliate Program
---

# Email Template: affiliate_account_approved

## Subject
🎉 ¡Bienvenido al Programa de Afiliados de {{ shop_name }}!

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
          🎉 ¡Solicitud Aprobada!
        </mj-text>
        <mj-text font-size="18px" color="#6c757d" align="center">
          Bienvenido a nuestro programa de afiliados
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Success Banner -->
    <mj-section background-color="#28a745" padding="40px 20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#ffffff" align="center">
          ¡Ahora Eres Afiliado!
        </mj-text>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-top="10px">
          Comienza a ganar comisiones hoy mismo
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
          ¡Felicidades! Su solicitud para unirse al programa de afiliados de {{ shop_name }} ha sido aprobada.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Ahora puede comenzar a promocionar nuestros productos y ganar comisiones en cada venta que genere.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- How it Works -->
    <mj-section background-color="#f8f9fa" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="#212529" align="center" padding-bottom="10px">
          Cómo Funciona
        </mj-text>
        <mj-text font-size="14px" color="#6c757d">
          1. Obten tus enlaces únicos de afiliado desde el panel de control<br/>
          2. Comparte estos enlaces con tu audiencia<br/>
          3. Gana comisiones cuando la gente compre a través de tus enlaces<br/>
          4. Recibe pagos según tu horario de pago
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          Acceder al Panel de Afiliados
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
🎉 ¡Bienvenido al Programa de Afiliados de {{ shop_name }}!

Hola {{ affiliate_name }},

¡Felicidades! Su solicitud para unirse al programa de afiliados de {{ shop_name }} ha sido aprobada.

Ahora puede comenzar a promocionar nuestros productos y ganar comisiones en cada venta que genere.

Cómo Funciona:
1. Obten tus enlaces únicos de afiliado desde el panel de control
2. Comparte estos enlaces con tu audiencia
3. Gana comisiones cuando la gente compre a través de tus enlaces
4. Recibe pagos según tu horario de pago

Accede a tu panel: {{ portal_url }}

{{ shop_name }}
¿Tienes preguntas? Contáctanos a {{ support_email }}