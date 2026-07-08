---
template_type: component_rollback_success
category: Component Updates
---

# Email Template: component_rollback_success

## Subject
✓ {{ component_name }} dikembalikan ke v{{ previous_version }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dbeafe">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          ↩️ Rollback Selesai
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Komponen Dipulihkan
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ component_name }} telah berhasil dikembalikan ke versi sebelumnya.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detail Rollback:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Komponen:</strong> {{ component_name }}<br/>
              <strong>Dikembalikan dari:</strong> v{{ failed_version }}<br/>
              <strong>Dipulihkan ke:</strong> v{{ previous_version }}<br/>
              <strong>Selesai:</strong> {{ completed_at }}<br/>
              <strong>Lama:</strong> {{ rollback_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if rollback_reason %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Alasan Rollback:
        </mj-text>
        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ rollback_reason }}
        </mj-text>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" font-weight="bold">
              ✓ Status Toko
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              Toko Anda sekarang berjalan pada versi stabil {{ previous_version }}. Semua fungsi seharusnya sudah dipulihkan.
            </mj-text>
          </mj-column>
        </mj-section>

        {% if data_restored %}
        <mj-spacer height="20px" />
        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>Pemulihan Data:</strong> {{ data_restoration_message }}
        </mj-text>
        {% endif %}

        {% if next_steps %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Langkah Selanjutnya:
        </mj-text>
        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ next_steps }}
        </mj-text>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ component_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Lihat Detail Komponen
        </mj-button>

        {% if incident_report_url %}
        <mj-spacer height="10px" />
        <mj-button href="{{ incident_report_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Lihat Laporan Kejadian
        </mj-button>
        {% endif %}

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Jika Anda terus mengalami masalah, silakan hubungi dukungan.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
↩️ ROLLBACK SELESAI

Komponen Dipulihkan

{{ component_name }} telah berhasil dikembalikan ke versi sebelumnya.

DETAIL ROLLBACK:
- Komponen: {{ component_name }}
- Dikembalikan dari: v{{ failed_version }}
- Dipulihkan ke: v{{ previous_version }}
- Selesai: {{ completed_at }}
- Lama: {{ rollback_duration }}

{% if rollback_reason %}
ALASAN ROLLBACK:
{{ rollback_reason }}
{% endif %}

✓ STATUS TOKO:
Toko Anda sekarang berjalan pada versi stabil {{ previous_version }}. Semua fungsi seharusnya sudah dipulihkan.

{% if data_restored %}
PEMULIHAN DATA: {{ data_restoration_message }}
{% endif %}

{% if next_steps %}
LANGKAH SELANJUTNYA:
{{ next_steps }}
{% endif %}

Lihat detail komponen: {{ component_url }}
{% if incident_report_url %}Lihat laporan kejadian: {{ incident_report_url }}{% endif %}

Jika Anda terus mengalami masalah, silakan hubungi dukungan.