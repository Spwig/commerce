---
template_type: system_health_recovered
category: System Health
---

# Email Template: system_health_recovered

## Subject
✓ {{ metric_name }} normal seviyeye döndü

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          ✓ Sorun Çözüldü
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Sistem Sağlığı Geri Döndü
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          İyimser haber! {{ metric_name }} ile ilgili sistem sağlığı sorunu çözüldü.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Geri Dönüşü Detayları:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Metric:</strong> {{ metric_name }}<br/>
              <strong>Mevcut Değer:</strong> <span style="color: #059669; font-weight: bold;">{{ current_value }}</span><br/>
              <strong>Normal Seviye:</strong> {{ normal_threshold }}<br/>
              <strong>Sorun Tespit Edildi:</strong> {{ issue_detected_at }}<br/>
              <strong>Geri Dönüş:</strong> {{ recovered_at }}<br/>
              <strong>Süre:</strong> {{ issue_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#065f46" font-weight="bold">
              ✓ Sistem Durumu: Normal
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              {{ metric_name }} normal seviyeye döndü ve kabul edilebilir parametreler içinde çalışıyor.
            </mj-text>
          </mj-column>
        </mj-section>

        {% if resolution_summary %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Çözüm Özeti:
        </mj-text>
        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ resolution_summary }}
        </mj-text>
        {% endif %}

        {% if actions_taken %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Alınan Aksiyonlar:
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
          Önleyici Tedbirler:
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
          Sistem Panelini Görüntüle
        </mj-button>

        {% if incident_report_url %}
        <mj-spacer height="10px" />
        <mj-button href="{{ incident_report_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Olay Raporunu Görüntüle
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ SORUN ÇÖZÜLDÜ

Sistem Sağlığı Geri Döndü

İyimser haber! {{ metric_name }} ile ilgili sistem sağlığı sorunu çözüldü.

GERİ DÖNÜŞÜ DETAYLARI:
- Metric: {{ metric_name }}
- Mevcut Değer: {{ current_value }}
- Normal Seviye: {{ normal_threshold }}
- Sorun Tespit Edildi: {{ issue_detected_at }}
- Geri Dönüş: {{ recovered_at }}
- Süre: {{ issue_duration }}

✓ SİSTEM DURUMU: NORMAL
{{ metric_name }} normal seviyeye döndü ve kabul edilebilir parametreler içinde çalışıyor.

{% if resolution_summary %}
ÇÖZÜM ÖZETİ:
{{ resolution_summary }}
{% endif %}

{% if actions_taken %}
ALINAN AKSİYONLAR:
{{ actions_taken }}
{% endif %}

{% if preventive_measures %}
ÖNLEYİCİ TEDBİRLER:
{{ preventive_measures }}
{% endif %}

Sistem panelini görüntüle: {{ dashboard_url }}
{% if incident_report_url %}Olay raporunu görüntüle: {{ incident_report_url }}{% endif %}