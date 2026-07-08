---
template_type: system_health_daily_report
category: System Health
---

# Email Template: system_health_daily_report

## Subject
📊 Rapporto quotidiano sullo stato del sistema - {{ report_date }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 Rapporto quotidiano sullo stato del sistema
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Riepilogo stato del sistema
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Rapporto quotidiano sullo stato del sistema per {{ report_date }}.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Stato generale: {{ overall_status }}
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
          Metriche del sistema:
        </mj-text>

        {% for metric in metrics %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ metric.name }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Corrente:</strong> {{ metric.current_value }}<br/>
              <strong>Media (24h):</strong> {{ metric.average }}<br/>
              <strong>Picco:</strong> {{ metric.peak }}<br/>
              <strong>Stato:</strong> <span style="color: {{ metric.status_color }};">{{ metric.status }}</span>
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        {% if warnings_count > 0 or critical_count > 0 %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Allerte (24h):
        </mj-text>
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Critiche:</strong> <span style="color: #dc2626;">{{ critical_count }}</span><br/>
              <strong>Avvisi:</strong> <span style="color: #d97706;">{{ warnings_count }}</span><br/>
              <strong>Risolte:</strong> <span style="color: #059669;">{{ resolved_count }}</span>
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Riepilogo prestazioni:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Tempo di funzionamento:</strong> {{ uptime_percentage }}%<br/>
              <strong>Tempo medio di risposta:</strong> {{ avg_response_time }}ms<br/>
              <strong>Richieste lente:</strong> {{ slow_requests_count }}<br/>
              <strong>Errori (500):</strong> {{ errors_500_count }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if recommendations %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Consigli:
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
          Visualizza il rapporto completo
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 RAPPORTO QUOTIDIANO SULLO STATO DEL SISTEMA

Riepilogo stato del sistema

Rapporto quotidiano sullo stato del sistema per {{ report_date }}.

STATO GENERALE: {{ overall_status }}
{{ status_message }}

METRICHE DEL SISTEMA:
{% for metric in metrics %}
{{ metric.name }}:
- Corrente: {{ metric.current_value }}
- Media (24h): {{ metric.average }}
- Picco: {{ metric.peak }}
- Stato: {{ metric.status }}

{% endfor %}

{% if warnings_count > 0 or critical_count > 0 %}
ALLERTE (24H):
- Critiche: {{ critical_count }}
- Avvisi: {{ warnings_count }}
- Risolte: {{ resolved_count }}
{% endif %}

RIEPILOGO PRESTAZIONI:
- Tempo di funzionamento: {{ uptime_percentage }}%
- Tempo medio di risposta: {{ avg_response_time }}ms
- Richieste lente: {{ slow_requests_count }}
- Errori (500): {{ errors_500_count }}

{% if recommendations %}
CONSIGLI:
{{ recommendations }}
{% endif %}

Visualizza il rapporto completo: {{ full_report_url }}