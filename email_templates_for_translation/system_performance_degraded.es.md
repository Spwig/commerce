---
template_type: system_performance_degraded
category: System Health
---

# Email Template: system_performance_degraded

## Subject
⚠️ Detección de Degradación de Rendimiento - {{ affected_area }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Degradación de Rendimiento
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Tiempos de Respuesta Lento Detectados
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Su instalación de Spwig está experimentando degradación de rendimiento.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Problema de Rendimiento:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Área Afectada:</strong> {{ affected_area }}<br/>
              <strong>Tiempo de Respuesta Actual:</strong> <span style="color: #d97706; font-weight: bold;">{{ current_response_time }}ms</span><br/>
              <strong>Tiempo de Respuesta Normal:</strong> {{ normal_response_time }}ms<br/>
              <strong>Degradación:</strong> {{ degradation_percentage }}% más lento<br/>
              <strong>Detectado:</strong> {{ detected_at }}
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
          Posibles Causas:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ possible_causes }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Endpoint Más Lento:
        </mj-text>

        {% for endpoint in slow_endpoints %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ endpoint.path }}</strong> - {{ endpoint.avg_time }}ms ({{ endpoint.request_count }} solicitudes)
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Acciones Recomendadas:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ recommended_actions }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ performance_dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Ver Panel de Rendimiento
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ slow_queries_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Ver Consultas Lentas
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Lo notificaremos cuando el rendimiento regrese a lo normal.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ DEGRADACIÓN DE RENDIMIENTO

Tiempos de Respuesta Lento Detectados

Su instalación de Spwig está experimentando degradación de rendimiento.

PROBLEMA DE RENDIMIENTO:
- Área Afectada: {{ affected_area }}
- Tiempo de Respuesta Actual: {{ current_response_time }}ms
- Tiempo de Respuesta Normal: {{ normal_response_time }}ms
- Degradación: {{ degradation_percentage }}% más lento
- Detectado: {{ detected_at }}

IMPACTO:
{{ impact_description }}

POSIBLES CAUSAS:
{{ possible_causes }}

ENDPOINTS MÁS LENTOS:
{% for endpoint in slow_endpoints %}
{{ endpoint.path }} - {{ endpoint.avg_time }}ms ({{ endpoint.request_count }} solicitudes)
{% endfor %}

ACCIONES RECOMENDADAS:
{{ recommended_actions }}

Ver panel de rendimiento: {{ performance_dashboard_url }}
Ver consultas lentas: {{ slow_queries_url }}

Lo notificaremos cuando el rendimiento regrese a lo normal.