---
template_type: system_health_warning
category: System Health
---

# Email Template: system_health_warning

## Subject
⚠️ Peringatan Kesehatan Sistem: {{ metric_name }} - {{ current_value }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Peringatan Kesehatan Sistem
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Batas Peringatan Telah Terlampaui
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Sebuah metrik kesehatan sistem telah melampaui batas peringatan pada instalasi Spwig Anda.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detail Peringatan:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Metric:</strong> {{ metric_name }}<br/>
              <strong>Nilai Saat Ini:</strong> <span style="color: #d97706; font-weight: bold;">{{ current_value }}</span><br/>
              <strong>Batas Peringatan:</strong> {{ warning_threshold }}<br/>
              <strong>Batas Kritis:</strong> {{ critical_threshold }}<br/>
              <strong>Detected:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Dampak Potensial:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ impact_description }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Tindakan yang Direkomendasikan:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ recommended_actions }}
        </mj-text>

        {% if trend_data %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Analisis Tren:
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
              💡 Tindakan Diperlukan: Meskipun belum kritis, mengatasi peringatan ini sekarang dapat mencegah masalah layanan di masa depan.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Lihat Dashboard Sistem
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ metrics_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Lihat Metrik Detail
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ PERINGATAN KESEHATAN SISTEM

Batas Peringatan Telah Terlampaui

Sebuah metrik kesehatan sistem telah melampaui batas peringatan pada instalasi Spwig Anda.

DETAIL PERINGATAN:
- Metric: {{ metric_name }}
- Nilai Saat Ini: {{ current_value }}
- Batas Peringatan: {{ warning_threshold }}
- Batas Kritis: {{ critical_threshold }}
- Detected: {{ detected_at }}

DAMPAK POTENSIAL:
{{ impact_description }}

TINDAKAN YANG DIREKOMENDASIKAN:
{{ recommended_actions }}

{% if trend_data %}
ANALISIS TREN:
{{ trend_data }}
{% endif %}

💡 TINDAKAN DIPERLUKAN: Meskipun belum kritis, mengatasi peringatan ini sekarang dapat mencegah masalah layanan di masa depan.

Lihat dashboard sistem: {{ dashboard_url }}
Lihat metrik detail: {{ metrics_url }}

