---
template_type: license_maintenance_renewal
category: License
---

# Email Template: license_maintenance_renewal

## Subject
Mantenimiento renovado - Orden #{{ order_number }}

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
    <mj-section background-color="{{ theme.color.success|default:'#10b981' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Mantenimiento renovado!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Orden #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Hola {{ customer_name }},
        </mj-text>
        <mj-text>
          Tu suscripción de mantenimiento de Spwig se ha renovado con éxito. Continuarás recibiendo actualizaciones de la plataforma, parches de seguridad y nuevas funciones.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Renewal Summary -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Resumen de renovación
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Clave de licencia: {{ license_key }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Mantenimiento válido hasta: {{ renewal_expires_at }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Número de orden: {{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What's Included -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Qué incluye
        </mj-text>
        <mj-text font-size="14px">
          Tu mantenimiento activo te da acceso a:
        </mj-text>
        <mj-text font-size="14px" padding-top="5px">
          - Actualizaciones y mejoras de características de la plataforma
        </mj-text>
        <mj-text font-size="14px">
          - Parches de seguridad y correcciones de errores
        </mj-text>
        <mj-text font-size="14px">
          - Nuevas versiones de componentes a través del servidor de actualización
        </mj-text>
        <mj-text font-size="14px">
          - Soporte técnico
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Next Steps -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          No se requiere ninguna acción por tu parte. Las actualizaciones seguirán estando disponibles a través del sistema de actualización de componentes de tu panel de administración.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Mantenimiento renovado!

Orden #{{ order_number }}

Hola {{ customer_name }},

Tu suscripción de mantenimiento de Spwig se ha renovado con éxito. Continuarás recibiendo actualizaciones de la plataforma, parches de seguridad y nuevas funciones.

Resumen de renovación:
- Clave de licencia: {{ license_key }}
- Mantenimiento válido hasta: {{ renewal_expires_at }}
- Número de orden: {{ order_number }}

Qué incluye:
- Actualizaciones y mejoras de características de la plataforma
- Parches de seguridad y correcciones de errores
- Nuevas versiones de componentes a través del servidor de actualización
- Soporte técnico

No se requiere ninguna acción por tu parte. Las actualizaciones seguirán estando disponibles a través del sistema de actualización de componentes de tu panel de administración.

¿Necesitas ayuda? Contacta a {{ support_email }}