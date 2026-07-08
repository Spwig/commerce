---
template_type: system_health_critical
category: System Health
---

# Email Template: system_health_critical

## Subject
🚨 KRITISCHER ALERT: {{ metric_name }} - {{ current_value }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#991b1b" align="center">
          🚨 KRITISCHER SYSTEMALERT
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Sofortige Aufmerksamkeit erforderlich
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Es wurde ein kritischer Gesundheitszustand des Systems auf Ihrer Spwig-Installation erkannt.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b" font-size="16px">
              🚨 Kritischer Fehler
            </mj-text>
            <mj-text color="#991b1b">
              <strong>Metric:</strong> {{ metric_name }}<br/>
              <strong>Aktueller Wert:</strong> <span style="font-size: 18px; font-weight: bold;">{{ current_value }}</span><br/>
              <strong>Kritischer Schwellenwert:</strong> {{ critical_threshold }}<br/>
              <strong>Erkannt um:</strong> {{ detected_at }}<br/>
              <strong>Schweregrad:</strong> KRITISCH
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Auswirkungen:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ impact_description }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Sofort erforderliche Maßnahmen:
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
              ⚠️ Warnung vor Leistungsverlust
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              Dieser Fehler kann zu Unterbrechungen des Dienstes oder einer Leistungseinbuße führen. Sofort beheben, um negative Auswirkungen auf Kunden zu vermeiden.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ dashboard_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          System-Dashboard ansehen
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ logs_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          System-Protokolle ansehen
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 KRITISCHER SYSTEMALERT

Sofortige Aufmerksamkeit erforderlich

Es wurde ein kritischer Gesundheitszustand des Systems auf Ihrer Spwig-Installation erkannt.

🚨 KRITISCHER FEHLER:
- Metric: {{ metric_name }}
- Aktueller Wert: {{ current_value }}
- Kritischer Schwellenwert: {{ critical_threshold }}
- Erkannt um: {{ detected_at }}
- Schweregrad: KRITISCH

AUSWIRKUNGEN:
{{ impact_description }}

SOFORT ERFAORDERLICHE MASSNAHMEN:
{{ recommended_actions }}

{% if trend_data %}
TREND:
{{ trend_data }}
{% endif %}

⚠️ WARNGESETZT VOR LEISTUNGSVERLUST:
Dieser Fehler kann zu Unterbrechungen des Dienstes oder einer Leistungseinbuße führen. Sofort beheben, um negative Auswirkungen auf Kunden zu vermeiden.

System-Dashboard ansehen: {{ dashboard_url }}
System-Protokolle ansehen: {{ logs_url }}