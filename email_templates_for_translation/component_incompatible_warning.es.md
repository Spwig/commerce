---
template_type: component_incompatible_warning
category: Component Updates
---

# Email Template: component_incompatible_warning

## Subject
⚠️ Incompatibilidad: {{ component_name }} y {{ conflicting_component }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Advertencia de compatibilidad
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Conflicto de versiones detectado
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Se ha detectado un problema de compatibilidad entre componentes en su tienda Spwig.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detalles del conflicto:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Componente 1:</strong> {{ component_name }} v{{ component_version }}<br/>
              <strong>Componente 2:</strong> {{ conflicting_component }} v{{ conflicting_version }}<br/>
              <strong>Detectado:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Problema de compatibilidad:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ incompatibility_description }}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#991b1b" font-weight="bold">
              Impacto potencial
            </mj-text>
            <mj-text font-size="14px" color="#991b1b" line-height="1.6">
              {{ impact_description }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Acción recomendada:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ recommended_action }}
        </mj-text>

        {% if compatible_versions %}
        <mj-spacer height="30px" />
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" font-weight="bold">
              Versiones compatibles
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              {{ compatible_versions }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        {% if update_url %}
        <mj-button href="{{ update_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Resolver conflicto
        </mj-button>
        <mj-spacer height="10px" />
        {% endif %}

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Contactar soporte
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Su tienda aún está operativa, pero le recomendamos resolver este conflicto pronto.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ ADVERTENCIA DE COMPATIBILIDAD

Conflicto de versiones detectado

Se ha detectado un problema de compatibilidad entre componentes en su tienda Spwig.

DETALLES DEL CONFLICTO:
- Componente 1: {{ component_name }} v{{ component_version }}
- Componente 2: {{ conflicting_component }} v{{ conflicting_version }}
- Detectado: {{ detected_at }}

PROBLEMA DE COMPATIBILIDAD:
{{ incompatibility_description }}

IMPACTO POTENCIAL:
{{ impact_description }}

ACCIÓN RECOMENDADA:
{{ recommended_action }}

{% if compatible_versions %}VERSIONES COMPATIBLES:
{{ compatible_versions }}
{% endif %}

{% if update_url %}Resolver conflicto: {{ update_url }}{% endif %}
Contactar soporte: {{ support_url }}

Su tienda aún está operativa, pero le recomendamos resolver este conflicto pronto.