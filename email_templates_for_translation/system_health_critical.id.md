---
template_type: system_health_critical
category: System Health
---

# Email Template: system_health_critical

## Subject
🚨 PERINGATAN KRITIS: {{ metric_name }} - {{ current_value }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#991b1b" align="center">
          🚨 PERINGATAN SISTEM KRITIS
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Perhatian Segera Diperlukan
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Sebuah masalah kesehatan sistem kritis telah terdeteksi pada instalasi Spwig Anda.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b" font-size="16px">
              🚨 Masalah Kritis
            </mj-text>
            <mj-text color="#991b1b">
              <strong>Metric:</strong> {{ metric_name }}<br/>
              <strong>Nilai Saat Ini:</strong> <span style="font-size: 18px; font-weight: bold;">{{ current_value }}</span><br/>
              <strong>Threshold Kritis:</strong> {{ critical_threshold }}<br/>
              <strong>Diketahui Pada:</strong> {{ detected_at }}<br/>
              <strong>Keparahan:</strong> KRITIS
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Dampak:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ impact_description }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Tindakan Segera Diperlukan:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ recommended_actions }}
        </mj-text>

        {% if trend_data %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Tren:
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
              ⚠️ Peringatan Penurunan Layanan
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              Masalah ini dapat menyebabkan gangguan layanan atau penurunan kinerja. Selesaikan segera untuk mencegah dampak terhadap pelanggan.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ dashboard_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Lihat Dashboard Sistem
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ logs_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Lihat Log Sistem
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 PERINGATAN SISTEM KRITIS

Perhatian Segera Diperlukan

Sebuah masalah kesehatan sistem kritis telah terdeteksi pada instalasi Spwig Anda.

🚨 MASALAH KRITIS:
- Metric: {{ metric_name }}
- Nilai Saat Ini: {{ current_value }}
- Threshold Kritis: {{ critical_threshold }}
- Diketahui Pada: {{ detected_at }}
- Keparahan: KRITIS

DAMPACK:
{{ impact_description }}

TINDAKAN SEGERA DIPERLUKAN:
{{ recommended_actions }}

{% if trend_data %}
TREN:
{{ trend_data }}
{% endif %}

⚠️ PERINGATAN PENURUNAN LAYANAN:
Masalah ini dapat menyebabkan gangguan layanan atau penurunan kinerja. Selesaikan segera untuk mencegah dampak terhadap pelanggan.

Lihat dashboard sistem: {{ dashboard_url }}
Lihat log sistem: {{ logs_url }}