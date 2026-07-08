---
template_type: backup_weekly_report
category: Backups
---

# Email Template: backup_weekly_report

## Subject
Ringkasan Cadangan Mingguan - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Ringkasan Cadangan Mingguan
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          {{ week_start }} - {{ week_end }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Statistik Cadangan:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Total Cadangan:</strong> {{ total_backups }}<br/>
              <strong>Berhasil:</strong> <span style="color: #059669;">{{ successful_backups }}</span><br/>
              <strong>Gagal:</strong> <span style="color: #dc2626;">{{ failed_backups }}</span><br/>
              <strong>Rata-rata Ukuran:</strong> {{ average_size }}<br/>
              <strong>Total Penyimpanan yang Digunakan:</strong> {{ total_storage }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        {% if failed_backups > 0 %}
        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              ⚠️ Masalah Terdeteksi:
            </mj-text>
            <mj-text color="#7f1d1d">
              {{ failed_backups }} cadangan gagal minggu ini. Silakan periksa dan lakukan tindakan korektif.
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="20px" />
        {% endif %}

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Cadangan Terbaru:
        </mj-text>

        {% for backup in recent_backups %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="4px" padding="12px" margin-bottom="8px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
              <strong>{{ backup.date }}</strong> - {{ backup.type }}
            </mj-text>
            <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              Ukuran: {{ backup.size }} | Durasi: {{ backup.duration }} |
              {% if backup.status == 'success' %}
              <span style="color: #059669;">✓ Sukses</span>
              {% else %}
              <span style="color: #dc2626;">✗ Gagal</span>
              {% endif %}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          Lihat Semua Cadangan
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
RINGKASAN CADANGAN MINGGUAN
{{ week_start }} - {{ week_end }}

STATISTIK CADANGAN:
- Total Cadangan: {{ total_backups }}
- Berhasil: {{ successful_backups }}
- Gagal: {{ failed_backups }}
- Rata-rata Ukuran: {{ average_size }}
- Total Penyimpanan yang Digunakan: {{ total_storage }}

{% if failed_backups > 0 %}
⚠️ MASALAH TERDETEKSI:
{{ failed_backups }} cadangan gagal minggu ini. Silakan periksa dan lakukan tindakan korektif.
{% endif %}

CADANGAN TERBARU:
{% for backup in recent_backups %}
- {{ backup.date }} - {{ backup.type }}
  Ukuran: {{ backup.size }} | Durasi: {{ backup.duration }} | Status: {{ backup.status }}
{% endfor %}

Lihat semua cadangan: {{ admin_backup_url }}