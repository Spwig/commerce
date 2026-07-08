---
template_type: admin_report_revenue_forecast
category: Admin Reports
---

# Email Template: admin_report_revenue_forecast

## Subject
📈 Umsatzvorhersage - {{ forecast_period }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📈 Umsatzvorhersage
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Projektierter Leistungsverlauf
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Vorhersagezeitraum:</strong> {{ forecast_period }}<br/>
              <strong>Projektierter Umsatz:</strong> <span style="font-size: 20px; color: #059669;">{{ projected_revenue }}</span><br/>
              <strong>Aktueller Trend:</strong> {{ trend_direction }}<br/>
              <strong>Sicherheit:</strong> {{ confidence_level }}%
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Analyse:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ analysis }}
        </mj-text>

        {% if recommendations %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Empfehlungen:
        </mj-text>
        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              {{ recommendations }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ full_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Detaillierte Vorhersage ansehen
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📈 UMSATZVORHERSAGE

Projektierter Leistungsverlauf

VORHERSAGE:
- Vorhersagezeitraum: {{ forecast_period }}
- Projektierter Umsatz: {{ projected_revenue }}
- Aktueller Trend: {{ trend_direction }}
- Sicherheit: {{ confidence_level }}%

ANALYSE:
{{ analysis }}

{% if recommendations %}
EMPFEHLUNGEN:
{{ recommendations }}
{% endif %}

Detaillierte Vorhersage ansehen: {{ full_report_url }}