---
template_type: system_health_critical
category: System Health
---

# Email Template: system_health_critical

## Subject
🚨 ALERTA CRÍTICO: {{ metric_name }} - {{ current_value }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#991b1b" align="center">
          🚨 ALERTA DE SISTEMA CRÍTICO
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Atenção Imediata Necessária
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Foi detectado um problema crítico na saúde do sistema da sua instalação Spwig.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b" font-size="16px">
              🚨 Problema Crítico
            </mj-text>
            <mj-text color="#991b1b">
              <strong>Métrica:</strong> {{ metric_name }}<br/>
              <strong>Valor Atual:</strong> <span style="font-size: 18px; font-weight: bold;">{{ current_value }}</span><br/>
              <strong>Limiar Crítico:</strong> {{ critical_threshold }}<br/>
              <strong>Detectado:</strong> {{ detected_at }}<br/>
              <strong>Severidade:</strong> CRITICAL
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
          Ações Imediatas Necessárias:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ recommended_actions }}
        </mj-text>

        {% if trend_data %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Tendência:
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
              ⚠️ Alerta de Degradacão de Serviço
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              Esse problema pode causar interrupções no serviço ou degradação do desempenho. Resolva imediatamente para evitar impacto nos clientes.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ dashboard_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Ver Painel do Sistema
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ logs_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Ver Logs do Sistema
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 ALERTA DE SISTEMA CRÍTICO

Atenção Imediata Necessária

Foi detectado um problema crítico na saúde do sistema da sua instalação Spwig.

🚨 PROBLEMA CRÍTICO:
- Métrica: {{ metric_name }}
- Valor Atual: {{ current_value }}
- Limiar Crítico: {{ critical_threshold }}
- Detectado: {{ detected_at }}
- Severidade: CRITICAL

IMPACTO:
{{ impact_description }}

AÇÕES IMEDIATAS NECESSÁRIAS:
{{ recommended_actions }}

{% if trend_data %}
TENDÊncia:
{{ trend_data }}
{% endif %}

⚠️ AVISO DE DEGRADAÇÃO DE SERVIÇO:
Esse problema pode causar interrupções no serviço ou degradação do desempenho. Resolva imediatamente para evitar impacto nos clientes.

Ver painel do sistema: {{ dashboard_url }}
Ver logs do sistema: {{ logs_url }}