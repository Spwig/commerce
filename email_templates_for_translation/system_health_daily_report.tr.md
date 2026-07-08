---
template_type: system_health_daily_report
category: System Health
---

# Email Template: system_health_daily_report

## Subject
📊 Günlük Sistem Sağlığı Raporu - {{ report_date }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 Günlük Sistem Sağlığı Raporu
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Sistem Sağlığı Özeti
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ report_date }} tarihli günlük sağlık raporu.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Genel Durum: {{ overall_status }}
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
          Sistem Metrikleri:
        </mj-text>

        {% for metric in metrics %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ metric.name }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Current:</strong> {{ metric.current_value }}<br/>
              <strong>Average (24h):</strong> {{ metric.average }}<br/>
              <strong>Peak:</strong> {{ metric.peak }}<br/>
              <strong>Status:</strong> <span style="color: {{ metric.status_color }};">{{ metric.status }}</span>
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        {% if warnings_count > 0 or critical_count > 0 %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Uyarılar (24h):
        </mj-text>
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Kritik:</strong> <span style="color: #dc2626;">{{ critical_count }}</span><br/>
              <strong>Uyarılar:</strong> <span style="color: #d97706;">{{ warnings_count }}</span><br/>
              <strong>Çözüldü:</strong> <span style="color: #059669;">{{ resolved_count }}</span>
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Performans Özeti:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Çalışma Süresi:</strong> {{ uptime_percentage }}%<br/>
              <strong>Ortalama Yanıt Süresi:</strong> {{ avg_response_time }}ms<br/>
              <strong>Yavaş İstekler:</strong> {{ slow_requests_count }}<br/>
              <strong>Hatalar (500):</strong> {{ errors_500_count }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if recommendations %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Öneriler:
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
          Raporu Görüntüle
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 GÜNLÜK SİSTEM SAĞLIĞI RAPORU

Sistem Sağlığı Özeti

{{ report_date }} tarihli günlük sağlık raporu.

GENEL DURUM: {{ overall_status }}
{{ status_message }}

SİSTEM METRİKLERİ:
{% for metric in metrics %}
{{ metric.name }}:
- Mevcut: {{ metric.current_value }}
- Ortalama (24h): {{ metric.average }}
- Zirve: {{ metric.peak }}
- Durum: {{ metric.status }}

{% endfor %}

{% if warnings_count > 0 or critical_count > 0 %}
Uyarılar (24h):
- Kritik: {{ critical_count }}
- Uyarılar: {{ warnings_count }}
- Çözüldü: {{ resolved_count }}
{% endif %}

PERFORMANS ÖZETİ:
- Çalışma Süresi: {{ uptime_percentage }}%
- Ortalama Yanıt Süresi: {{ avg_response_time }}ms
- Yavaş İstekler: {{ slow_requests_count }}
- Hatalar (500): {{ errors_500_count }}

{% if recommendations %}
ÖNERİLER:
{{ recommendations }}
{% endif %}

Tam raporu görüntüle: {{ full_report_url }}