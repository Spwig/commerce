---
template_type: component_deprecated_warning
category: Component Updates
---

# Email Template: component_deprecated_warning

## Subject
⚠️ {{ component_name }} dejará de estar disponible el {{ deprecation_date }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Notificación de desuso
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          El componente dejará de estar disponible
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ component_name }} dejará de estar disponible y ya no se recomienda su uso. Por favor, planifique la migración a una solución alternativa.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Cronograma de desuso:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Componente:</strong> {{ component_name }}<br/>
              <strong>Versión actual:</strong> {{ current_version }}<br/>
              <strong>Fecha de desuso:</strong> {{ deprecation_date }}<br/>
              <strong>Fin de soporte:</strong> {{ end_of_support_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Razón del desuso:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ deprecation_reason }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ¿Qué significa esto?:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • El componente seguirá funcionando hasta {{ end_of_support_date }}<br/>
          • No se agregarán nuevas funciones<br/>
          • Se proporcionarán actualizaciones de seguridad hasta el fin de soporte<br/>
          • Después de {{ end_of_support_date }}, el componente ya no recibirá actualizaciones
        </mj-text>

        {% if recommended_alternative %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Alternativa recomendada:
        </mj-text>
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#065f46" font-weight="bold">
              {{ alternative_name }}
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              {{ alternative_description }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        {% if migration_guide %}
        <mj-spacer height="20px" />
        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          <a href="{{ migration_guide }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Ver guía de migración</a>
        </mj-text>
        {% endif %}

        <mj-spacer height="30px" />

        {% if alternative_url %}
        <mj-button href="{{ alternative_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Ver alternativa
        </mj-button>
        <mj-spacer height="10px" />
        {% endif %}

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Contactar soporte
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ NOTIFICACIÓN DE DESUSO

El componente dejará de estar disponible

{{ component_name }} dejará de estar disponible y ya no se recomienda su uso. Por favor, planifique la migración a una solución alternativa.

CRONOGRAMA DE DESUSO:
- Componente: {{ component_name }}
- Versión actual: {{ current_version }}
- Fecha de desuso: {{ deprecation_date }}
- Fin de soporte: {{ end_of_support_date }}

RAZÓN DEL DESUSO:
{{ deprecation_reason }}

¿QUÉ SIGNIFICA ESTO?:
• El componente seguirá funcionando hasta {{ end_of_support_date }}
• No se agregarán nuevas funciones
• Se proporcionarán actualizaciones de seguridad hasta el fin de soporte
• Después de {{ end_of_support_date }}, el componente ya no recibirá actualizaciones

{% if recommended_alternative %}
ALTERNATIVA RECOMENDADA:
{{ alternative_name }}
{{ alternative_description }}
{% endif %}

{% if migration_guide %}Ver guía de migración: {{ migration_guide }}{% endif %}
{% if alternative_url %}Ver alternativa: {{ alternative_url }}{% endif %}
Contactar soporte: {{ support_url }}
