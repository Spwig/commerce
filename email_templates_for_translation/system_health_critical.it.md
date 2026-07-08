---
template_type: system_health_critical
category: System Health
---

# Email Template: system_health_critical

## Subject
🚨 AVVISO CRITICO: {{ metric_name }} - {{ current_value }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#991b1b" align="center">
          🚨 AVVISO SISTEMA CRITICO
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Attenzione immediata richiesta
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          &Egrave; stata rilevata un problema critico di salute del sistema sulla vostra installazione Spwig.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b" font-size="16px">
              🚨 Problema Critico
            </mj-text>
            <mj-text color="#991b1b">
              <strong>Metrica:</strong> {{ metric_name }}<br/>
              <strong>Valore Attuale:</strong> <span style="font-size: 18px; font-weight: bold;">{{ current_value }}</span><br/>
              <strong>Limite Critico:</strong> {{ critical_threshold }}<br/>
              <strong>Rilevato:</strong> {{ detected_at }}<br/>
              <strong>Gravità:</strong> CRITICAL
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Impatto:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ impact_description }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Azioni Immediate Richieste:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ recommended_actions }}
        </mj-text>

        {% if trend_data %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Trend:
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
              ⚠️ AVVERTENZA DI DEGRADO DEI SERVIZI
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              Questo problema potrebbe causare interruzioni del servizio o degrado delle prestazioni. Risolvete immediatamente per prevenire un impatto sui clienti.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ dashboard_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Visualizza il pannello di controllo del sistema
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ logs_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Visualizza i log del sistema
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 AVVISO SISTEMA CRITICO

Attenzione immediata richiesta

&Egrave; stata rilevata un problema critico di salute del sistema sulla vostra installazione Spwig.

🚨 PROBLEMA CRITICO:
- Metrica: {{ metric_name }}
- Valore Attuale: {{ current_value }}
- Limite Critico: {{ critical_threshold }}
- Rilevato: {{ detected_at }}
- Gravità: CRITICAL

IMPACTO:
{{ impact_description }}

AZIONI IMMEDIATE RICHIESTE:
{{ recommended_actions }}

{% if trend_data %}
TREND:
{{ trend_data }}
{% endif %}

⚠️ AVVERTENZA DI DEGRADO DEI SERVIZI:
Questo problema potrebbe causare interruzioni del servizio o degrado delle prestazioni. Risolvete immediatamente per prevenire un impatto sui clienti.

Visualizza il pannello di controllo del sistema: {{ dashboard_url }}
Visualizza i log del sistema: {{ logs_url }}

