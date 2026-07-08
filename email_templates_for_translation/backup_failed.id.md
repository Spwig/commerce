---
template_type: backup_failed
category: Backups
---

# Email Template: backup_failed

## Subject
🚨 DARURAT: Backup Gagal - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef2f2">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#dc2626" align="center">
          ⚠️ Backup Gagal
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#1f2937' }}">
          Hai {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Operasi backup kritis untuk toko {{ shop_name }} Anda gagal. Tindakan segera diperlukan untuk memastikan perlindungan data.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              Detail Backup:
            </mj-text>
            <mj-text color="#7f1d1d">
              <strong>Tipe Backup:</strong> {{ backup_type }}<br/>
              <strong>Dibuat:</strong> {{ backup_started_at }}<br/>
              <strong>Gagal:</strong> {{ backup_failed_at }}<br/>
              <strong>Lama:</strong> {{ backup_duration }}
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

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Tindakan yang Direkomendasikan:
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          1. Periksa ruang disk yang tersedia di server Anda<br/>
          2. Verifikasi koneksi database<br/>
          3. Periksa log kesalahan untuk melihat stack trace yang rinci<br/>
          4. Ulangi backup secara manual atau tunggu hingga jadwal berikutnya<br/>
          5. Hubungi dukungan jika masalah ini masih berlanjut
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Lihat Log Backup
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ retry_backup_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          Ulangi Backup Sekarang
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>Backup Terakhir yang Berhasil:</strong> {{ last_successful_backup }}<br/>
          <strong>Backup Berikutnya yang Dijadwalkan:</strong> {{ next_scheduled_backup }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 DARURAT: BACKUP GAGAL

Hai {{ admin_name }},

Operasi backup kritis untuk toko {{ shop_name }} Anda gagal. Tindakan segera diperlukan untuk memastikan perlindungan data.

DETAIL BACKUP:
- Tipe Backup: {{ backup_type }}
- Dibuat: {{ backup_started_at }}
- Gagal: {{ backup_failed_at }}
- Lama: {{ backup_duration }}

DETAIL KESALAHAN:
{{ error_message }}

TINDAKAN YANG DIREKOMENDASIKAN:
1. Periksa ruang disk yang tersedia di server Anda
2. Verifikasi koneksi database
3. Periksa log kesalahan untuk melihat stack trace yang rinci
4. Ulangi backup secara manual atau tunggu hingga jadwal berikutnya
5. Hubungi dukungan jika masalah ini masih berlanjut

Lihat log backup: {{ admin_backup_url }}
Ulangi backup sekarang: {{ retry_backup_url }}

Backup Terakhir yang Berhasil: {{ last_successful_backup }}
Backup Berikutnya yang Dijadwalkan: {{ next_scheduled_backup }}

---
Ini adalah peringatan sistem kritis untuk administrator {{ shop_name }}.