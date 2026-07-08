---
template_type: component_security_update
category: Component Updates
---

# Email Template: component_security_update

## Subject
🔒 URGENTE: Actualización de seguridad disponible para {{ component_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#991b1b" align="center">
          🔒 ACTUALIZACIÓN DE SEGURIDAD REQUERIDA
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Parche de Seguridad Crítico
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Se ha descubierto una vulnerabilidad de seguridad en {{ component_name }}. Por favor, actualice inmediatamente para proteger su tienda.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b" font-size="16px">
              ⚠️ Información de Seguridad
            </mj-text>
            <mj-text color="#991b1b">
              <strong>Componente:</strong> {{ component_name }}<br/>
              <strong>Versión Actual:</strong> {{ current_version }}<br/>
              <strong>Versión Parcheada:</strong> {{ patched_version }}<br/>
              <strong>Gravedad:</strong> {{ severity_level }}<br/>
              <strong>CVE ID:</strong> {{ cve_id }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Detalles de la Vulnerabilidad:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ vulnerability_description }}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Impacto Potencial:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ impact_description }}
        </mj-text>

        {% if mitigation_steps %}
        <mj-spacer height="30px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              Mitigación Temporal
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ mitigation_steps }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Acción Requerida: Instale la Actualización Inmediatamente
        </mj-text>

        <mj-spacer height="20px" />

        <mj-button href="{{ update_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Instalar Parche de Seguridad
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ advisory_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Leer Avisos de Seguridad
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Si necesita asistencia, contacte inmediatamente al soporte de Spwig.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🔒 ACTUALIZACIÓN DE SEGURIDAD REQUERIDA

Parche de Seguridad Crítico

Se ha descubierto una vulnerabilidad de seguridad en {{ component_name }}. Por favor, actualice inmediatamente para proteger su tienda.

⚠️ INFORMACIÓN DE SEGURIDAD:
- Componente: {{ component_name }}
- Versión Actual: {{ current_version }}
- Versión Parcheada: {{ patched_version }}
- Gravedad: {{ severity_level }}
- CVE ID: {{ cve_id }}

DETALLES DE LA VULNERABILIDAD:
{{ vulnerability_description }}

IMPACTO POTENCIAL:
{{ impact_description }}

{% if mitigation_steps %}
MITIGACIÓN TEMPORAL:
{{ mitigation_steps }}
{% endif %}

ACCION REQUERIDA: INSTALAR ACTUALIZACIÓN DE INMEDIATO

Instalar parche de seguridad: {{ update_url }}
Leer aviso de seguridad: {{ advisory_url }}

Si necesita asistencia, contacte inmediatamente al soporte de Spwig.