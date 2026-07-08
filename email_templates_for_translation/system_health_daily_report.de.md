---
template_type: system_health_daily_report
category: System Health
---

# Email Template: system_health_daily_report

## Subject
📊 Täglicher Systemgesundheitsbericht - {{ report_date }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 Täglicher Systemgesundheitsbericht
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Systemgesundheitszusammenfassung
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Täglicher Gesundheitsbericht für {{ report_date }}.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Gesamter Status: {{ overall_status }}
        </mj-text>

        <mj-section background-color="{{ status_color }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#ffffff" font-weight="bold" align="center">
              {{ status_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Systemmetriken:
        </mj-text>

        {% for metric in metrics %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ metric.name }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Aktuell:</strong> {{ metric.current_value }}<br/>
              <strong>Durchschnitt (24h):</strong> {{ metric.average }}<br/>
              <strong>Höchstwert:</strong> {{ metric.peak }}<br/>
              <strong>Status:</strong> <span style="color: {{ metric.status_color }};">{{ metric.status }}</span>
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        {% if warnings_count > 0 or critical_count > 0 %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Warnmeldungen (24h):
        </mj-text>
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Kritisch:</strong> <span style="color: #dc2626;">{{ critical_count }}</span><br/>
              <strong>Warnmeldungen:</strong> <span style="color: #d97706;">{{ warnings_count }}</span><br/>
              <strong>Behebt:</strong> <span style="color: #059669;">{{ resolved_count }}</span>
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Leistungsbericht:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Laufzeit:</strong> {{ uptime_percentage }}%<br/>
              <strong>Durchschnittliche Antwortzeit:</strong> {{ avg_response_time }}ms<br/>
              <strong>Langsame Anfragen:</strong> {{ slow_requests_count }}<br/>
              <strong>Fehler (500):</strong> {{ errors_500_count }}
            </mj-text>
          </mj-column>
        </mj-section>

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
          Bericht einsehen
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 TÄGLICHER SYSTEMGESUNDHEITSBERICHT

Systemgesundheitszusammenfassung

Täglicher Gesundheitsbericht für {{ report_date }}.

GESAMTER STATUS: {{ overall_status }}
{{ status_message }}

SYSTEMMETRIKEN:
{% for metric in metrics %}
{{ metric.name }}:
- Aktuell: {{ metric.current_value }}
- Durchschnitt (24h): {{ metric.average }}
- Höchstwert: {{ metric.peak }}
- Status: {{ metric.status }}

{% endfor %}

{% if warnings_count > 0 or critical_count > 0 %}
WARNMELDUNGEN (24H):
- Kritisch: {{ critical_count }}
- Warnmeldungen: {{ warnings_count }}
- Behebt: {{ resolved_count }}
{% endif %}

LEISTUNGSBERICHT:
- Laufzeit: {{ uptime_percentage }}%
- Durchschnittliche Antwortzeit: {{ avg_response_time }}ms
- Langsame Anfragen: {{ slow_requests_count }}
- Fehler (500): {{ errors_500_count }}

{% if recommendations %}
EMPFEHLUNGEN:
{{ recommendations }}
{% endif %}

Vollständigen Bericht ansehen: {{ full_report_url }}