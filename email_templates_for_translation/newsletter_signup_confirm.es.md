---
template_type: newsletter_signup_confirm
category: Newsletter
---

# Email Template: newsletter_signup_confirm

## Subject
Confirma tu suscripción a {{ store_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Confirma tu suscripción
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          ¡Gracias por suscribirte para recibir noticias de {{ store_name }}! Por favor, confirma tu dirección de correo electrónico para comenzar a recibir nuestras novedades y ofertas.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ confirmation_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Confirmar suscripción
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              ¿No puedes hacer clic en el botón? Copia y pega este enlace en tu navegador:<br/>
              <span style="color: {{ theme.color.primary|default:'#2563eb' }}; font-family: 'Courier New', monospace;">{{ confirmation_url }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>¿Por qué confirmar?</strong><br/>
          Confirmar tu correo electrónico nos ayuda a asegurarnos de que realmente deseas recibir nuestras novedades y mantiene tu bandeja de entrada libre de spam.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          ¿No te suscribiste? Puedes ignorar este correo con seguridad.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Confirma tu suscripción a {{ store_name }}

¡Gracias por suscribirte para recibir noticias de {{ store_name }}! Por favor, confirma tu dirección de correo electrónico para comenzar a recibir nuestras novedades y ofertas:

{{ confirmation_url }}

Confirmar tu correo electrónico nos ayuda a asegurarnos de que realmente deseas recibir nuestras novedades y mantiene tu bandeja de entrada libre de spam.

¿No te suscribiste? Puedes ignorar este correo con seguridad.