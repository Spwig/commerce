---
template_type: translation_job_failed
category: Translation Service
---

# Email Template: translation_job_failed

## Subject
❌ Pemesanan Terjemahan Gagal: {{ content_type }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ❌ Pemesanan Terjemahan Gagal
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Kesalahan Terjemahan
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Pemesanan terjemahan Anda mengalami kesalahan dan tidak dapat diselesaikan.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detail Pemesanan:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>ID Pemesanan:</strong> {{ job_id }}<br/>
              <strong>Jenis Konten:</strong> {{ content_type }}<br/>
              <strong>Bahasa Tujuan:</strong> {{ target_languages }}<br/>
              <strong>Gagal Pada:</strong> {{ failed_at }}<br/>
              <strong>Kode Kesalahan:</strong> {{ error_code }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Pesan Kesalahan:
        </mj-text>

        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" font-family="monospace" color="#991b1b" line-height="1.6">
              {{ error_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if partial_completion %}
        <mj-spacer height="30px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              Pemrosesan Sebagian
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ items_completed }} dari {{ total_items }} item berhasil diterjemahkan sebelum kesalahan terjadi.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Penyebab Umum:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Masalah koneksi API layanan terjemahan<br/>
          • Kredit terjemahan tidak cukup<br/>
          • Konten sumber tidak valid atau rusak<br/>
          • Pasangan bahasa tidak didukung
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Tindakan yang Direkomendasikan:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Periksa pengaturan layanan terjemahan Anda<br/>
          2. Pastikan kredit terjemahan tersedia<br/>
          3. Periksa pesan kesalahan untuk isu spesifik<br/>
          4. Ulangi pemesanan terjemahan
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ retry_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Ulangi Terjemahan
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ settings_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Periksa Pengaturan
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Jika masalah ini terus berlanjut, hubungi dukungan dengan kode kesalahan {{ error_code }}.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❌ PEMESANAN TERJEMAHAN GAGAL

Kesalahan Terjemahan

Pemesanan terjemahan Anda mengalami kesalahan dan tidak dapat diselesaikan.

DETAIL PEMESANAN:
- ID Pemesanan: {{ job_id }}
- Jenis Konten: {{ content_type }}
- Bahasa Tujuan: {{ target_languages }}
- Gagal Pada: {{ failed_at }}
- Kode Kesalahan: {{ error_code }}

PESAN KESALAHAN:
{{ error_message }}

{% if partial_completion %}
Pemrosesan Sebagian:
{{ items_completed }} dari {{ total_items }} item berhasil diterjemahkan sebelum kesalahan terjadi.
{% endif %}

Penyebab Umum:
• Masalah koneksi API layanan terjemahan
• Kredit terjemahan tidak cukup
• Konten sumber tidak valid atau rusak
• Pasangan bahasa tidak didukung

Tindakan yang Direkomendasikan:
1. Periksa pengaturan layanan terjemahan Anda
2. Pastikan kredit terjemahan tersedia
3. Periksa pesan kesalahan untuk isu spesifik
4. Ulangi pemesanan terjemahan

Ulangi terjemahan: {{ retry_url }}
Periksa pengaturan: {{ settings_url }}

Jika masalah ini terus berlanjut, hubungi dukungan dengan kode kesalahan {{ error_code }}.