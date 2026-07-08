---
template_type: backup_restore_failed
category: Backups
---

# Email Template: backup_restore_failed

## Subject
🚨 KRITIS: Pemulihan Backup Gagal - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef2f2">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#dc2626" align="center">
          🚨 KRITIS: Pemulihan Backup Gagal
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#1f2937' }}" font-weight="bold">
          Hi {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Operasi pemulihan backup kritis telah gagal. Toko Anda mungkin berada dalam keadaan tidak konsisten dan memerlukan perhatian segera.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              Detail Pemulihan:
            </mj-text>
            <mj-text color="#7f1d1d">
              <strong>File Backup:</strong> {{ backup_filename }}<br/>
              <strong>Dibuka:</strong> {{ restore_started_at }}<br/>
              <strong>Gagal:</strong> {{ restore_failed_at }}<br/>
              <strong>Lama:</strong> {{ restore_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Detail Kesalahan:
        </mj-text>

        <mj-section background-color="#f9fafb" border-radius="4px" padding="15px">
          <mj-column>
            <mj-text font-family="'Courier New', monospace" font-size="13px" color="#dc2626">
              {{ error_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#92400e">
              🚨 TINDAKAN SEGERA DIBUTUHKAN:
            </mj-text>
            <mj-text color="#92400e">
              1. <strong>JANGAN</strong> membuat perubahan apa pun pada toko<br/>
              2. Periksa koneksi dan integritas database<br/>
              3. Periksa log kesalahan untuk melihat stack trace rinci<br/>
              4. Hubungi segera dukungan teknis<br/>
              5. Pertimbangkan untuk kembali ke keadaan terakhir yang diketahui baik
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Lihat Log Pemulihan
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ support_url }}" background-color="#92400e" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          Hubungi Dukungan Darurat
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 KRITIS: PEMULIHAN BACKUP GAGAL

Hi {{ admin_name }},

Operasi pemulihan backup kritis telah gagal. Toko Anda mungkin berada dalam keadaan tidak konsisten dan memerlukan perhatian segera.

DETAIL PEMULIHAN:
- File Backup: {{ backup_filename }}
- Dibuka: {{ restore_started_at }}
- Gagal: {{ restore_failed_at }}
- Lama: {{ restore_duration }}

DETAIL KESALAHAN:
{{ error_message }}

🚨 TINDAKAN SEGERA DIBUTUHKAN:
1. JANGAN membuat perubahan apa pun pada toko
2. Periksa koneksi dan integritas database
3. Periksa log kesalahan untuk melihat stack trace rinci
4. Hubungi segera dukungan teknis
5. Pertimbangkan untuk kembali ke keadaan terakhir yang diketahui baik

Lihat log pemulihan: {{ admin_backup_url }}
Hubungi dukungan darurat: {{ support_url }}