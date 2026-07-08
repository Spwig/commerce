---
template_type: system_health_critical
category: System Health
---

# Email Template: system_health_critical

## Subject
🚨 AVISO DE SISTEMA CRÍTICO: {{ metric_name }} - {{ current_value }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#991b1b" align="center">
          🚨 AVISO DE SISTEMA CRÍTICO
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Atención Inmediata Requerida
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Se ha detectado un problema grave de salud del sistema en su instalación de Spwig.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b" font-size="16px">
              🚨 Problema Crítico
            </mj-text>
            <mj-text color="#991b1b">
              <strong>Métrica:</strong> {{ metric_name }}<br/>
              <strong>Valor Actual:</strong> <span style="font-size: 18px; font-weight: bold;">{{ current_value }}</span><br/>
              <strong>Umbral Crítico:</strong> {{ critical_threshold }}<br/>
              <strong>Detectado:</strong> {{ detected_at }}<br/>
              <strong>Gravedad:</strong> CRÍTICO
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Impacto:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ impact_description }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Acciones Inmediatas Requeridas:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ recommended_actions }}
        </mj-text>

        {% if trend_data %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Tendencia:
        </mj-text>
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              {{ trend_data }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ Advertencia de Degradación del Servicio
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              Este problema puede causar interrupciones del servicio o degradación del rendimiento. Abordar inmediatamente para evitar el impacto en los clientes.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ dashboard_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Ver Panel de Control del Sistema
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ logs_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Ver Registros del Sistema
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 AVISO DE SISTEMA CRÍTICO

Atención Inmediata Requerida

Se ha detectado un problema grave de salud del sistema en su instalación de Spwig.

🚨 PROBLEMA CRÍTICO:
- Métrica: {{ metric_name }}
- Valor Actual: {{ current_value }}
- Umbral Crítico: {{ critical_threshold }}
- Detectado: {{ detected_at }}
- Gravedad: CRÍTICO

IMPACTO:
{{ impact_description }}

ACCIONES INMEDIATAS REQUERIDAS:
{{ recommended_actions }}

{% if trend_data %}
TENDENCIA:
{{ trend_data }}
{% endif %}

⚠️ ADVERTENCIA DE DEGRADACIÓN DEL SERVICIO:
Este problema puede causar interrupciones del servicio o degradación del rendimiento. Abordar inmediatamente para evitar el impacto en los clientes.

Ver panel de control del sistema: {{ dashboard_url }}
Ver registros del sistema: {{ logs_url }}
