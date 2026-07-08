---
template_type: system_performance_degraded
category: System Health
---

# Email Template: system_performance_degraded

## Subject
⚠️ Leistungseinbruch erkannt - {{ affected_area }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Leistungseinbruch
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Langsame Antwortzeiten erkannt
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Ihre Spwig-Installation erlebt einen Leistungseinbruch.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Leistungsproblem:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Betroffenes Bereich:</strong> {{ affected_area }}<br/>
              <strong>Aktuelle Antwortzeit:</strong> <span style="color: #d97706; font-weight: bold;">{{ current_response_time }}ms</span><br/>
              <strong>Normale Antwortzeit:</strong> {{ normal_response_time }}ms<br/>
              <strong>Einbruch:</strong> {{ degradation_percentage }}% langsamer<br/>
              <strong>Erkannt:</strong> {{ detected_at }}
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
          Mögliche Ursachen:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ possible_causes }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Langsamste Endpoints:
        </mj-text>

        {% for endpoint in slow_endpoints %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ endpoint.path }}</strong> - {{ endpoint.avg_time }}ms ({{ endpoint.request_count }} Anfragen)
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Empfohlene Aktionen:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ recommended_actions }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ performance_dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Performance-Dashboard ansehen
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ slow_queries_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Langsame Abfragen ansehen
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Wir benachrichtigen Sie, sobald die Leistung auf normaler Ebene ist.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ LEISTUNGSABNACHMUNG

Langsame Antwortzeiten erkannt

Ihre Spwig-Installation erlebt einen Leistungseinbruch.

LEISTUNGSPROBLEM:
- Betroffenes Bereich: {{ affected_area }}
- Aktuelle Antwortzeit: {{ current_response_time }}ms
- Normale Antwortzeit: {{ normal_response_time }}ms
- Einbruch: {{ degradation_percentage }}% langsamer
- Erkannt: {{ detected_at }}

AUSWIRKUNGEN:
{{ impact_description }}

MOGLICHE URSACHEN:
{{ possible_causes }}

LANGSAMSTE ENDPOINTS:
{% for endpoint in slow_endpoints %}
{{ endpoint.path }} - {{ endpoint.avg_time }}ms ({{ endpoint.request_count }} Anfragen)
{% endfor %}

EMPFOHLENE AKTIONEN:
{{ recommended_actions }}

Performance-Dashboard ansehen: {{ performance_dashboard_url }}
Langsame Abfragen ansehen: {{ slow_queries_url }}

Wir benachrichtigen Sie, sobald die Leistung auf normaler Ebene ist.