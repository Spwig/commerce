---
template_type: component_update_failed
category: Component Updates
---

# Email Template: component_update_failed

## Subject
❌ Actualización fallida: {{ component_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ❌ Actualización fallida
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Error de instalación
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          La actualización de {{ component_name }} a la versión {{ target_version }} falló en la instalación.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detalles del fallo:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Componente:</strong> {{ component_name }}<br/>
              <strong>Versión objetivo:</strong> {{ target_version }}<br/>
              <strong>Falló en:</strong> {{ failed_at }}<br/>
              <strong>Código de error:</strong> {{ error_code }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Mensaje de error:
        </mj-text>

        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" font-family="monospace" color="#991b1b" line-height="1.6">
              {{ error_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if error_log %}
        <mj-spacer height="20px" />
        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>Registro de errores completo:</strong><br/>
          <code style="font-size: 12px; color: #6b7280;">{{ error_log|truncatewords:50 }}</code>
        </mj-text>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ¿Qué hacer:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Verificar los requisitos del sistema y dependencias<br/>
          2. Revisar el registro de errores para detalles<br/>
          3. Intentar instalar de nuevo, o contactar soporte<br/>
          4. Su tienda sigue funcionando en {{ current_version }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ retry_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Reintentar instalación
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Contactar soporte
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❌ ACTUALIZACIÓN FALLIDA

Error de instalación

La actualización de {{ component_name }} a la versión {{ target_version }} falló en la instalación.

DETALLES DEL FALLO:
- Componente: {{ component_name }}
- Versión objetivo: {{ target_version }}
- Falló en: {{ failed_at }}
- Código de error: {{ error_code }}

MENSAJE DE ERROR:
{{ error_message }}

{% if error_log %}
REGISTRO DE ERRORES COMPLETO:
{{ error_log|truncatewords:50 }}
{% endif %}

¿QUÉ HACER:
1. Verificar los requisitos del sistema y dependencias
2. Revisar el registro de errores para detalles
3. Intentar instalar de nuevo, o contactar soporte
4. Su tienda sigue funcionando en {{ current_version }}

Reintentar instalación: {{ retry_url }}
Contactar soporte: {{ support_url }}

