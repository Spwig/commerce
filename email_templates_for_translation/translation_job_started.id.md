---
template_type: translation_job_started
category: Translation Service
---

# Email Template: translation_job_started

## Subject
🌐 Pekerjaan Terjemahan Dimulai: {{ content_type }} ({{ source_language }} → {{ target_languages }})

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          🌐 Pekerjaan Terjemahan Dimulai
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Pemrosesan Terjemahan Massal
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Pekerjaan terjemahan massal Anda telah dimulai dan kini sedang diproses.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detail Pekerjaan:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>ID Pekerjaan:</strong> {{ job_id }}<br/>
              <strong>Jenis Konten:</strong> {{ content_type }}<br/>
              <strong>Bahasa Sumber:</strong> {{ source_language }}<br/>
              <strong>Bahasa Target:</strong> {{ target_languages }}<br/>
              <strong>Jumlah Item Terjemahan:</strong> {{ item_count }}<br/>
              <strong>Dibuat:</strong> {{ started_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Estimasi Selesaikan:
        </mj-text>

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#065f46" font-weight="bold" align="center">
              {{ estimated_completion }}
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              (Berdasarkan {{ word_count }} kata)
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Apa yang Terjadi Selanjutnya:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Layanan terjemahan AI memproses konten Anda<br/>
          2. Terjemahan disimpan sebagai draf untuk ditinjau<br/>
          3. Anda akan menerima email saat pekerjaan selesai<br/>
          4. Tinjau dan terbitkan terjemahan dari panel admin Anda
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ job_status_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Lihat Status Pekerjaan
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Anda dapat menutup email ini. Kami akan memberi tahu Anda saat terjemahan selesai.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🌐 PEKERJAAN TERJEMAHAN DIMULAI

Pemrosesan Terjemahan Massal

Pekerjaan terjemahan massal Anda telah dimulai dan kini sedang diproses.

DETAIL PEKERJAAN:
- ID Pekerjaan: {{ job_id }}
- Jenis Konten: {{ content_type }}
- Bahasa Sumber: {{ source_language }}
- Bahasa Target: {{ target_languages }}
- Jumlah Item Terjemahan: {{ item_count }}
- Dibuat: {{ started_at }}

ESTIMASI SELESAI:
{{ estimated_completion }}
(Berdasarkan {{ word_count }} kata)

APA YANG TERJADI SELANJUTNYA:
1. Layanan terjemahan AI memproses konten Anda
2. Terjemahan disimpan sebagai draf untuk ditinjau
3. Anda akan menerima email saat pekerjaan selesai
4. Tinjau dan terbitkan terjemahan dari panel admin Anda

Lihat status pekerjaan: {{ job_status_url }}

Anda dapat menutup email ini. Kami akan memberi tahu Anda saat terjemahan selesai.