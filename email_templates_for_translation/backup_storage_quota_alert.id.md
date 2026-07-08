---
template_type: backup_storage_quota_alert
category: Backups
---

# Email Template: backup_storage_quota_alert

## Subject
🚨 Kuota Penyimpanan Backup Kritis - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef2f2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#dc2626" align="center">
          🚨 Kuota Penyimpanan Kritis
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>URGENT:</strong> Penyimpanan backup Anda saat ini sangat rendah. Backup masa depan mungkin gagal jika ruang penyimpanan tidak bebas.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              Status Penyimpanan:
            </mj-text>
            <mj-text color="#7f1d1d">
              <strong>Used:</strong> {{ storage_used }} of {{ storage_total }}<br/>
              <strong>Utilization:</strong> {{ storage_percentage }}%<br/>
              <strong>Available:</strong> {{ storage_available }}<br/>
              <strong>Status:</strong> <span style="color: #dc2626; font-weight: bold;">{{ storage_status }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#92400e">
              Tindakan Segera Diperlukan:
            </mj-text>
            <mj-text color="#92400e">
              1. Hapus backup lama yang tidak diperlukan lagi<br/>
              2. Arsipkan backup ke penyimpanan eksternal<br/>
              3. Tingkatkan kuota/ kapasitas penyimpanan<br/>
              4. Tinjau kebijakan retensi backup<br/>
              5. Pantau penyimpanan setiap hari hingga selesai
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Kelola Penyimpanan Sekarang
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 KUOTA PENYIMPANAN KRITIS

Hi {{ admin_name }},

URGENT: Penyimpanan backup Anda saat ini sangat rendah. Backup masa depan mungkin gagal jika ruang penyimpanan tidak bebas.

STATUS PENYIMPANAN:
- Used: {{ storage_used }} of {{ storage_total }}
- Utilization: {{ storage_percentage }}%
- Available: {{ storage_available }}
- Status: {{ storage_status }}

TINDAKAN SEGERA DIPERLUKAN:
1. Hapus backup lama yang tidak diperlukan lagi
2. Arsipkan backup ke penyimpanan eksternal
3. Tingkatkan kuota/ kapasitas penyimpanan
4. Tinjau kebijakan retensi backup
5. Pantau penyimpanan setiap hari hingga selesai

Kelola penyimpanan sekarang: {{ admin_backup_url }}