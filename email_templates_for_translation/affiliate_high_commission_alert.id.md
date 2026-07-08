---
template_type: affiliate_high_commission_alert
category: Affiliate Program
---

# Email Template: affiliate_high_commission_alert

## Subject
⚠️ Aktivitas Komisi Tidak Biasa Terdeteksi - {{ affiliate_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Peringatan Komisi Tinggi
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Aktivitas Tidak Biasa Terdeteksi
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Komisi yang tidak biasa tinggi telah diperoleh oleh afiliasi {{ affiliate_name }}. Ini memerlukan tinjauan untuk pencegahan penipuan.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detail Peringatan:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Afiliasi:</strong> {{ affiliate_name }} ({{ affiliate_id }})<br/>
              <strong>Jumlah Komisi:</strong> <span style="font-weight: bold; color: #dc2626;">{{ commission_amount }}</span><br/>
              <strong>Nilai Pesanan:</strong> {{ order_value }}<br/>
              <strong>ID Pesanan:</strong> {{ order_number }}<br/>
              <strong>Terdeteksi:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Mengapa Hal Ini Ditandai:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ flag_reason }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Tindakan yang Direkomendasikan:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Tinjau detail pesanan untuk keabsahan<br/>
          • Periksa riwayat rujukan afiliasi<br/>
          • Verifikasi pelanggan tidak terkait dengan penunjuk<br/>
          • Setujui atau tolak komisi di panel administrasi
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ review_commission_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Tinjau Komisi
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ affiliate_details_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Lihat Detail Afiliasi
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Komisi ini menunggu tinjauan dan tidak akan dibayar sampai disetujui.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ PERINGATAN KOMISI TINGGI

Aktivitas Tidak Biasa Terdeteksi

Komisi yang tidak biasa tinggi telah diperoleh oleh afiliasi {{ affiliate_name }}. Ini memerlukan tinjauan untuk pencegahan penipuan.

DETAIL PERINGATAN:
- Afiliasi: {{ affiliate_name }} ({{ affiliate_id }})
- Jumlah Komisi: {{ commission_amount }}
- Nilai Pesanan: {{ order_value }}
- ID Pesanan: {{ order_number }}
- Terdeteksi: {{ detected_at }}

MENGAPA HAL INI DITANDAI:
{{ flag_reason }}

TINDAKAN YANG DIREKOMENDASIKAN:
• Tinjau detail pesanan untuk keabsahan
• Periksa riwayat rujukan afiliasi
• Verifikasi pelanggan tidak terkait dengan penunjuk
• Setujui atau tolak komisi di panel administrasi

Tinjau komisi: {{ review_commission_url }}
Lihat detail afiliasi: {{ affiliate_details_url }}

Komisi ini menunggu tinjauan dan tidak akan dibayar sampai disetujui.