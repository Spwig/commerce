---
template_type: admin_report_abandoned_carts_summary
category: Admin Reports
---

# Email Template: admin_report_abandoned_carts_summary

## Subject
📊 Laporan Keranjang Ditinggalkan - {{ abandoned_count }} keranjang ({{ abandoned_value }})

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 Laporan Keranjang Ditinggalkan
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Ringkasan Pengabaian Keranjang
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Masa Periode:</strong> {{ report_period }}<br/>
              <strong>Keranjang Ditinggalkan:</strong> {{ abandoned_count }}<br/>
              <strong>Nilai Ditinggalkan:</strong> <span style="font-size: 18px; color: #dc2626;">{{ abandoned_value }}</span><br/>
              <strong>Tingkat Pengabaian:</strong> {{ abandonment_rate }}%<br/>
              <strong>Tingkat Pemulihan:</strong> {{ recovery_rate }}%
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Alasan Teratas (jika dilacak):
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ top_reasons }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ full_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Lihat Detail
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 LAPORAN KERANJANG DITINGGALKAN

Ringkasan Pengabaian Keranjang

METRIK:
- Periode: {{ report_period }}
- Keranjang Ditinggalkan: {{ abandoned_count }}
- Nilai Ditinggalkan: {{ abandoned_value }}
- Tingkat Pengabaian: {{ abandonment_rate }}%
- Tingkat Pemulihan: {{ recovery_rate }}%

ALASAN TERATAS:
{{ top_reasons }}

Lihat detail: {{ full_report_url }}