---
template_type: translation_job_failed
category: Translation Service
---

# Email Template: translation_job_failed

## Subject
❌ Trabajo de traducción fallido: {{ content_type }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ❌ Trabajo de Traducción Fallido
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Error de Traducción
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Su trabajo de traducción por lotes encontró un error y no pudo completarse.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detalles del Trabajo:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>ID del Trabajo:</strong> {{ job_id }}<br/>
              <strong>Tipo de Contenido:</strong> {{ content_type }}<br/>
              <strong>Idiomas de Destino:</strong> {{ target_languages }}<br/>
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

        {% if partial_completion %}
        <mj-spacer height="30px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              Completado Parcialmente
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ items_completed }} de {{ total_items }} elementos se tradujeron correctamente antes de que ocurriera el error.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Causas Comunes:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Problemas de conexión con la API del servicio de traducción<br/>
          • Créditos de traducción insuficientes<br/>
          • Contenido de origen inválido o corrupto<br/>
          • Pareja de idioma no admitida
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Acciones Recomendadas:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Verifique la configuración del servicio de traducción<br/>
          2. Verifique que estén disponibles los créditos de traducción<br/>
          3. Revise el mensaje de error para identificar problemas específicos<br/>
          4. Vuelva a intentar el trabajo de traducción
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ retry_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Volver a Intentar la Traducción
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ settings_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Verificar Configuración
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Si el problema persiste, póngase en contacto con el soporte con el código de error {{ error_code }}.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❌ TRABAJO DE TRADUCCIÓN FALLIDO

Error de traducción

Su trabajo de traducción por lotes encontró un error y no pudo completarse.

DETALLES DEL TRABAJO:
- ID del trabajo: {{ job_id }}
- Tipo de contenido: {{ content_type }}
- Idiomas de destino: {{ target_languages }}
- Falló en: {{ failed_at }}
- Código de error: {{ error_code }}

MENSAJE DE ERROR:
{{ error_message }}

{% if partial_completion %}
COMPLETADO PARCIALMENTE:
{{ items_completed }} de {{ total_items }} elementos se tradujeron correctamente antes de que ocurriera el error.
{% endif %}

CAUSAS COMUNES:
• Problemas de conexión con la API del servicio de traducción
• Créditos de traducción insuficientes
• Contenido de origen inválido o corrupto
• Pareja de idioma no admitida

ACCIONES RECOMENDADAS:
1. Verifique la configuración del servicio de traducción
2. Verifique que estén disponibles los créditos de traducción
3. Revise el mensaje de error para identificar problemas específicos
4. Vuelva a intentar el trabajo de traducción

Volver a intentar la traducción: {{ retry_url }}
Verificar configuración: {{ settings_url }}

Si el problema persiste, póngase en contacto con el soporte con el código de error {{ error_code }}.