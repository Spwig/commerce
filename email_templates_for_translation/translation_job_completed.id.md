---
template_type: translation_job_completed
category: Translation Service
---

# Email Template: translation_job_completed

## Subject
✓ Terjemahan selesai: {{ content_type }} ({{ language_count }} bahasa)

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          ✓ Terjemahan Selesai!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Terjemahan Anda Siap
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Berita baik! Pekerjaan terjemahan massal Anda telah selesai dengan sukses.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Ringkasan Pekerjaan:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>ID Pekerjaan:</strong> {{ job_id }}<br/>
              <strong>Jenis Konten:</strong> {{ content_type }}<br/>
              <strong>Bahasa:</strong> {{ target_languages }}<br/>
              <strong>Item Terjemahan:</strong> {{ items_translated }}<br/>
              <strong>Jumlah Kata Total:</strong> {{ word_count }}<br/>
              <strong>Selesai:</strong> {{ completed_at }}<br/>
              <strong>Lama Waktu:</strong> {{ job_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Kualitas Terjemahan:
        </mj-text>

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#065f46">
              <strong>Skor Kualitas Rata-rata:</strong> {{ quality_score }}%<br/>
              <strong>Kualitas Tinggi:</strong> {{ high_quality_count }} item<br/>
              <strong>Dianjurkan untuk Diperiksa:</strong> {{ review_needed_count }} item
            </mj-text>
          </mj-column>
        </mj-section>

        {% if review_needed_count > 0 %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ Dianjurkan untuk Diperiksa
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ review_needed_count }} terjemahan mendapatkan skor di bawah 85% dan sebaiknya diperiksa sebelum dipublikasikan.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Langkah Berikutnya:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Tinjau terjemahan di panel administrasi Anda<br/>
          2. Ubah terjemahan apa pun yang memerlukan penyempurnaan<br/>
          3. Publikasikan terjemahan untuk membuatnya aktif<br/>
          4. Konten multibahasa Anda akan tersedia bagi pelanggan
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ review_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Tinjau Terjemahan
        </mj-button>

        {% if can_publish_all %}
        <mj-spacer height="10px" />
        <mj-button href="{{ publish_all_url }}" background-color="#059669" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Publikasikan Semua
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ TERJEMAHAN SELESAI!

Terjemahan Anda Siap

Berita baik! Pekerjaan terjemahan massal Anda telah selesai dengan sukses.

RINGKASAN PEKERJAAN:
- ID Pekerjaan: {{ job_id }}
- Jenis Konten: {{ content_type }}
- Bahasa: {{ target_languages }}
- Item Terjemahan: {{ items_translated }}
- Jumlah Kata Total: {{ word_count }}
- Selesai: {{ completed_at }}
- Lama Waktu: {{ job_duration }}

KUALITAS TERJEMAHAN:
- Skor Kualitas Rata-rata: {{ quality_score }}%
- Kualitas Tinggi: {{ high_quality_count }} item
- Dianjurkan untuk Diperiksa: {{ review_needed_count }} item

{% if review_needed_count > 0 %}
⚠️ DIANJURKAN UNTUK DIPERIKSA:
{{ review_needed_count }} terjemahan mendapatkan skor di bawah 85% dan sebaiknya diperiksa sebelum dipublikasikan.
{% endif %}

LANGKAH BERIKUTNYA:
1. Tinjau terjemahan di panel administrasi Anda
2. Ubah terjemahan apa pun yang memerlukan penyempurnaan
3. Publikasikan terjemahan untuk membuatnya aktif
4. Konten multibahasa Anda akan tersedia bagi pelanggan

Tinjau terjemahan: {{ review_url }}
{% if can_publish_all %}Publikasikan semua: {{ publish_all_url }}{% endif %}