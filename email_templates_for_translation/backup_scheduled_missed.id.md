---
template_type: backup_scheduled_missed
category: Backups
---

# Email Template: backup_scheduled_missed

## Subject
⚠️ Backup Terjadwal Tidak Berjalan - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Backup Terjadwal Tidak Berjalan
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Backup terjadwal untuk {{ shop_name }} tidak berjalan seperti yang diharapkan. Data Anda mungkin tidak sepenuhnya terlindungi.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detail Jadwal Backup:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Waktu Terjadwal:</strong> {{ scheduled_time }}<br/>
              <strong>Jenis Backup:</strong> {{ backup_type }}<br/>
              <strong>Backup Terakhir yang Berhasil:</strong> {{ last_successful_backup }}<br/>
              <strong>Waktu Sejak Backup Terakhir:</strong> {{ time_since_last }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Kemungkinan Penyebab:
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          • Server sedang offline atau tidak dapat dijangkau<br/>
          • Layanan tugas terjadwal tidak berjalan<br/>
          • Hak akses tidak cukup<br/>
          • Ruang penyimpanan penuh<br/>
          • Masalah koneksi database
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Jalankan Backup Secara Manual
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ admin_logs_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Lihat Log Sistem
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ BACKUP TERJADWAL TIDAK BERJALAN

Hi {{ admin_name }},

Backup terjadwal untuk {{ shop_name }} tidak berjalan seperti yang diharapkan. Data Anda mungkin tidak sepenuhnya terlindungi.

DETAIL JADWAL BACKUP:
- Waktu Terjadwal: {{ scheduled_time }}
- Jenis Backup: {{ backup_type }}
- Backup Terakhir yang Berhasil: {{ last_successful_backup }}
- Waktu Sejak Backup Terakhir: {{ time_since_last }}

KEMUNGKINAN PENYEBAB:
• Server sedang offline atau tidak dapat dijangkau
• Layanan tugas terjadwal tidak berjalan
• Hak akses tidak cukup
• Ruang penyimpanan penuh
• Masalah koneksi database

Jalankan backup secara manual: {{ admin_backup_url }}
Lihat log sistem: {{ admin_logs_url }}