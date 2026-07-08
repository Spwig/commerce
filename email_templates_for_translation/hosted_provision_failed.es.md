---
template_type: hosted_provision_failed
category: License
---

# Email Template: hosted_provision_failed

## Subject
Acción requerida - Problema en la configuración de la tienda {{ store_name }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.error|default:'#dc2626' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Problema en la configuración de la tienda
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Hola {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          Nos encontramos con un problema al configurar tu tienda <strong>{{ store_name }}</strong>. Nuestro equipo ha sido notificado y está investigándolo.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Error Details -->
    <mj-section background-color="#fef2f2" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="14px" font-weight="bold" color="#991b1b" padding-bottom="10px">
          ¿Qué pasó
        </mj-text>
        <mj-text font-size="14px" color="#7f1d1d">
          {{ provision_error }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What's Next -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          ¿Qué sucede a continuación?
        </mj-text>
        <mj-text font-size="14px">
          Nuestro equipo de soporte ha sido notificado automáticamente sobre este problema. No necesitas tomar ninguna acción - nos pondremos en contacto contigo una vez que el problema esté resuelto.
        </mj-text>
        <mj-text font-size="14px" padding-top="10px">
          Si tienes alguna pregunta en el camino, no dudes en contactarnos.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Problema en la configuración de la tienda - {{ store_name }}

Hola {{ name|default:'there' }},

Nos encontramos con un problema al configurar tu tienda {{ store_name }}. Nuestro equipo ha sido notificado y está investigándolo.

¿Qué pasó:
{{ provision_error }}

¿Qué sucede a continuación?
Nuestro equipo de soporte ha sido notificado automáticamente sobre este problema. No necesitas tomar ninguna acción - nos pondremos en contacto contigo una vez que el problema esté resuelto.

Si tienes alguna pregunta en el camino, no dudes en contactarnos.

¿Necesitas ayuda? Contacta a {{ support_email }}