---
template_type: system_health_warning
category: System Health
---

# Email Template: system_health_warning

## Subject
⚠️ Advertencia de Salud del Sistema: {{ metric_name }} - {{ current_value }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Advertencia de Salud del Sistema
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Se ha superado el umbral de advertencia
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Una métrica de salud del sistema ha superado el umbral de advertencia en su instalación de Spwig.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detalles de la Advertencia:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Métrica:</strong> {{ metric_name }}<br/>
              <strong>Valor Actual:</strong> <span style="color: #d97706; font-weight: bold;">{{ current_value }}</span><br/>
              <strong>Umbral de Advertencia:</strong> {{ warning_threshold }}<br/>
              <strong>Umbral Crítico:</strong> {{ critical_threshold }}<br/>
              <strong>Detectado:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Impacto Potencial:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ impact_description }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Acciones Recomendadas:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ recommended_actions }}
        </mj-text>

        {% if trend_data %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Análisis de Tendencias:
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

        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              💡 Acción Requerida: Aunque no sea crítico aún, abordar esta advertencia ahora puede prevenir problemas de servicio futuros.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Ver Panel de Control del Sistema
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ metrics_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Ver Métricas Detalladas
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ ADVERTENCIA DE SALUD DEL SISTEMA

Se ha superado el umbral de advertencia

Una métrica de salud del sistema ha superado el umbral de advertencia en su instalación de Spwig.

DETALLES DE LA ADVERTENCIA:
- Métrica: {{ metric_name }}
- Valor Actual: {{ current_value }}
- Umbral de Advertencia: {{ warning_threshold }}
- Umbral Crítico: {{ critical_threshold }}
- Detectado: {{ detected_at }}

IMPACTO POTENCIAL:
{{ impact_description }}

ACCIONES RECOMENDADAS:
{{ recommended_actions }}

{% if trend_data %}
ANÁLISIS DE TENDENCIAS:
{{ trend_data }}
{% endif %}

💡 ACCIÓN REQUERIDA: Aunque no sea crítico aún, abordar esta advertencia ahora puede prevenir problemas de servicio futuros.

Ver panel de control del sistema: {{ dashboard_url }}
Ver métricas detalladas: {{ metrics_url }}