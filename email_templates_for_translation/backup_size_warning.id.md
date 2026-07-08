---
template_type: backup_size_warning
category: Backups
---

# Email Template: backup_size_warning

## Subject
⚠️ Peringatan Ukuran Backup - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Peringatan Ukuran Backup
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Backup terbaru Anda untuk {{ shop_name }} telah melebihi ambang batas ukuran yang disarankan. Ini mungkin menunjukkan kebutuhan penyimpanan data yang semakin meningkat.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Informasi Backup:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Current Size:</strong> {{ backup_size }}<br/>
              <strong>Ambang Batas Peringatan:</strong> {{ size_threshold }}<br/>
              <strong>Pertumbuhan Sejak Minggu Lalu:</strong> {{ size_increase }}<br/>
              <strong>Tanggal Backup:</strong> {{ backup_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Tindakan yang Direkomendasikan:
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          1. Periksa kebijakan retensi backup<br/>
          2. Pertimbangkan mengarsipkan backup lama<br/>
          3. Periksa file besar yang tidak diperlukan di perpustakaan media<br/>
          4. Evaluasi kebutuhan kapasitas penyimpanan<br/>
          5. Pantau tren pertumbuhan backup
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          Kelola Backup
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ PERINGATAN UKURAN BACKUP

Hi {{ admin_name }},

Backup terbaru Anda untuk {{ shop_name }} telah melebihi ambang batas ukuran yang disarankan. Ini mungkin menunjukkan kebutuhan penyimpanan data yang semakin meningkat.

INFORMASI BACKUP:
- Current Size: {{ backup_size }}
- Warning Threshold: {{ size_threshold }}
- Growth Since Last Week: {{ size_increase }}
- Backup Date: {{ backup_date }}

RECOMMENDED ACTIONS:
1. Periksa kebijakan retensi backup
2. Pertimbangkan mengarsipkan backup lama
3. Periksa file besar yang tidak diperlukan di perpustakaan media
4. Evaluasi kebutuhan kapasitas penyimpanan
5. Pantau tren pertumbuhan backup

Kelola backup: {{ admin_backup_url }}