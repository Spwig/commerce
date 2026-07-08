---
template_type: system_health_warning
category: System Health
---

# Email Template: system_health_warning

## Subject
⚠️ Avviso di salute del sistema: {{ metric_name }} - {{ current_value }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Avviso di salute del sistema
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Threshold di Avviso Superato
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Un parametro di salute del sistema ha superato il threshold di avviso sulla vostra installazione Spwig.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Dettagli dell'Avviso:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Metrica:</strong> {{ metric_name }}<br/>
              <strong>Valore Attuale:</strong> <span style="color: #d97706; font-weight: bold;">{{ current_value }}</span><br/>
              <strong>Threshold di Avviso:</strong> {{ warning_threshold }}<br/>
              <strong>Threshold Critico:</strong> {{ critical_threshold }}<br/>
              <strong>Rilevato:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Impatto Potenziale:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ impact_description }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Azioni Consigliate:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ recommended_actions }}
        </mj-text>

        {% if trend_data %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Analisi della tendenza:
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
              💡 Azione Richiesta: Sebbene non critico al momento, risolvere questo avviso ora può prevenire problemi futuri di servizio.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Visualizza il Dashboard del Sistema
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ metrics_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Visualizza le Metriche Dettagliate
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ AVVISO DI SALUTE DEL SISTEMA

Threshold di Avviso Superato

Un parametro di salute del sistema ha superato il threshold di avviso sulla vostra installazione Spwig.

DETTAGLI DELL'AVVISO:
- Metrica: {{ metric_name }}
- Valore Attuale: {{ current_value }}
- Threshold di Avviso: {{ warning_threshold }}
- Threshold Critico: {{ critical_threshold }}
- Rilevato: {{ detected_at }}

IMPACTO POTENZIALE:
{{ impact_description }}

AZIONI CONSIGLIATE:
{{ recommended_actions }}

{% if trend_data %}
ANALISI DELLA TENDENZA:
{{ trend_data }}
{% endif %}

💡 AZIONE RICHIESTA: Sebbene non critico al momento, risolvere questo avviso ora può prevenire problemi futuri di servizio.

Visualizza il Dashboard del Sistema: {{ dashboard_url }}
Visualizza le Metriche Dettagliate: {{ metrics_url }}