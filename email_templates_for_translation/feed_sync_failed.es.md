---
template_type: feed_sync_failed
category: Product Feeds
---

# Email Template: feed_sync_failed

## Subject
❌ {{ feed_name }} sincronización fallida en {{ platform_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ❌ Error en la Sincronización
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Error de Sincronización
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          No se pudo sincronizar {{ feed_name }} con {{ platform_name }}.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detalles del Fallo:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Feed:</strong> {{ feed_name }}<br/>
              <strong>Plataforma:</strong> {{ platform_name }}<br/>
              <strong>Falló en:</strong> {{ failed_at }}<br/>
              <strong>Código de Error:</strong> {{ error_code }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Mensaje de Error:
        </mj-text>

        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" font-family="monospace" color="#991b1b" line-height="1.6">
              {{ error_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Causas Comunes:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Credenciales de API inválidas o token caducado<br/>
          • Problemas de conectividad de red<br/>
          • Límites de tasa de la API de la plataforma superados<br/>
          • El formato del feed no cumple con los requisitos de la plataforma
        </mj-text>

        {% if recommended_action %}
        <mj-spacer height="30px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              Acción Recomendada
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ recommended_action }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ retry_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Volver a Intentar la Sincronización
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ admin_feed_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Verificar Configuración del Feed
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❌ ERROR DE SINCRONIZACIÓN

Error de Sincronización

No se pudo sincronizar {{ feed_name }} con {{ platform_name }}.

DETALLES DEL FALLO:
- Feed: {{ feed_name }}
- Plataforma: {{ platform_name }}
- Falló en: {{ failed_at }}
- Código de Error: {{ error_code }}

MENSAJE DE ERROR:
{{ error_message }}

CAUSAS COMUNES:
• Credenciales de API inválidas o token caducado
• Problemas de conectividad de red
• Límites de tasa de la API de la plataforma superados
• El formato del feed no cumple con los requisitos de la plataforma

{% if recommended_action %}
ACCION RECOMENDADA:
{{ recommended_action }}
{% endif %}

Reintentar sincronización: {{ retry_url }}
Verificar configuración del feed: {{ admin_feed_url }}