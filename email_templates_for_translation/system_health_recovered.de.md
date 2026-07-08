---
template_type: system_health_recovered
category: System Health
---

# Email Template: system_health_recovered

## Subject
✓ {{ metric_name }} ist wieder normal

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          ✓ Problem behoben
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Systemgesundheit wiederhergestellt
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Gute Nachrichten! Das Systemgesundheitsproblem mit {{ metric_name }} wurde behoben.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Wiederherstellungsdetails:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Metric:</strong> {{ metric_name }}<br/>
              <strong>Aktueller Wert:</strong> <span style="color: #059669; font-weight: bold;">{{ current_value }}</span><br/>
              <strong>Normaler Schwellenwert:</strong> {{ normal_threshold }}<br/>
              <strong>Problem erkannt:</strong> {{ issue_detected_at }}<br/>
              <strong>Wiederhergestellt:</strong> {{ recovered_at }}<br/>
              <strong>Dauer:</strong> {{ issue_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#065f46" font-weight="bold">
              ✓ Systemstatus: Normal
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              {{ metric_name }} ist auf normale Werte zurückgekehrt und funktioniert innerhalb akzeptabler Parameter.
            </mj-text>
          </mj-column>
        </mj-section>

        {% if resolution_summary %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Wiederherstellungszusammenfassung:
        </mj-text>
        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ resolution_summary }}
        </mj-text>
        {% endif %}

        {% if actions_taken %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Getroffene Maßnahmen:
        </mj-text>
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.6">
              {{ actions_taken }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        {% if preventive_measures %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Präventive Maßnahmen:
        </mj-text>
        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              {{ preventive_measures }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Systemdashboard ansehen
        </mj-button>

        {% if incident_report_url %}
        <mj-spacer height="10px" />
        <mj-button href="{{ incident_report_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Zwischenbericht ansehen
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ PROBLEM BEHOBEN

Systemgesundheit wiederhergestellt

Gute Nachrichten! Das Systemgesundheitsproblem mit {{ metric_name }} wurde behoben.

WIEDERHERSTELLUNGSDETAILS:
- Metric: {{ metric_name }}
- Aktueller Wert: {{ current_value }}
- Normaler Schwellenwert: {{ normal_threshold }}
- Problem erkannt: {{ issue_detected_at }}
- Wiederhergestellt: {{ recovered_at }}
- Dauer: {{ issue_duration }}

✓ SYSTEMSTATUS: NORMAL
{{ metric_name }} ist auf normale Werte zur點kgekehrt und funktioniert innerhalb akzeptabler Parameter.

{% if resolution_summary %}
WIEDERHERSTELLUNGSZUSAMMENFASSUNG:
{{ resolution_summary }}
{% endif %}

{% if actions_taken %}
GETROFFENE MAßNAHMEN:
{{ actions_taken }}
{% endif %}

{% if preventive_measures %}
PRÄVENTIVE MAßNAHMEN:
{{ preventive_measures }}
{% endif %}

Systemdashboard ansehen: {{ dashboard_url }}
{% if incident_report_url %}Zwischenbericht ansehen: {{ incident_report_url }}{% endif %}