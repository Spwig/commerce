---
template_type: blog_subscription_confirmed
category: Blog
---

# Email Template: blog_subscription_confirmed

## Subject
Confirme su suscripción a {{ blog_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Confirme su suscripción
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hola {{ subscriber_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Gracias por suscribirse a {{ blog_name }}! Para completar su suscripción y comenzar a recibir actualizaciones, confirme su dirección de correo electrónico.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ confirmation_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Confirmar suscripción
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              ¿No puede hacer clic en el botón? Copie y pegue este enlace en su navegador:
              <br/>
              <span style="color: {{ theme.color.primary|default:'#2563eb' }}; font-family: 'Courier New', monospace;">
                {{ confirmation_url }}
              </span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>¿Por qué confirmar?</strong><br/>
          La confirmación por correo electrónico nos ayuda a asegurarnos de que desea recibir actualizaciones y evita el spam. Su privacidad y bandeja de entrada son importantes para nosotros.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          ¿No se suscribió? Puede ignorar este correo electrónico de forma segura.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
CONFIRME SU SUSCRIPCIÓN

Hola {{ subscriber_name }},

Gracias por suscribirse a {{ blog_name }}! Para completar su suscripción y comenzar a recibir actualizaciones, confirme su dirección de correo electrónico.

Confirmar suscripción: {{ confirmation_url }}

¿Por qué confirmar?
La confirmación por correo electrónico nos ayuda a asegurarnos de que desea recibir actualizaciones y evita el spam. Su privacidad y bandeja de entrada son importantes para nosotros.

¿No se suscribió? Puede ignorar este correo electrónico de forma segura.