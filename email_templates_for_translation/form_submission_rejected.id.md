---
template_type: form_submission_rejected
category: Form Builder
---

# Email Template: form_submission_rejected

## Subject
Pembaruan mengenai pengajuan Anda {{ form_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Pembaruan mengenai Pengajuan Anda
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hai {{ submitter_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Terima kasih telah mengajukan formulir {{ form_name }}. Setelah tinjauan yang hati-hati, kami saat ini tidak dapat menyetujui pengajuan Anda.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detail Pengajuan:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Form:</strong> {{ form_name }}<br/>
              <strong>Diajukan:</strong> {{ submission_date }}<br/>
              <strong>Ditinjau:</strong> {{ rejection_date }}<br/>
              <strong>Nomor Referensi:</strong> {{ submission_id }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if rejection_reason %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Alasan:
        </mj-text>
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ rejection_reason }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        {% if can_resubmit %}
        <mj-spacer height="30px" />
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" font-weight="bold">
              Anda Dapat Mengajukan Kembali
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              {{ resubmit_instructions }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        {% if resubmit_url %}
        <mj-button href="{{ resubmit_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Ajukan Kembali
        </mj-button>
        <mj-spacer height="10px" />
        {% endif %}

        {% if support_url %}
        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Hubungi Dukungan
        </mj-button>
        <mj-spacer height="20px" />
        {% endif %}

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Jika Anda memiliki pertanyaan mengenai keputusan ini, jangan ragu untuk menghubungi kami.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Pembaruan mengenai pengajuan Anda

Hai {{ submitter_name }},

Terima kasih telah mengajukan formulir {{ form_name }}. Setelah tinjauan yang hati-hati, kami saat ini tidak dapat menyetujui pengajuan Anda.

DETAIL PENGAJUAN:
- Form: {{ form_name }}
- Diajukan: {{ submission_date }}
- Ditinjau: {{ rejection_date }}
- Nomor Referensi: {{ submission_id }}

{% if rejection_reason %}
ALASAN:
{{ rejection_reason }}
{% endif %}

{% if can_resubmit %}
ANDA DAPAT MENGAJUKAN KEMBALI:
{{ resubmit_instructions }}
{% endif %}

{% if resubmit_url %}Ajukan kembali: {{ resubmit_url }}{% endif %}
{% if support_url %}Hubungi dukungan: {{ support_url }}{% endif %}

Jika Anda memiliki pertanyaan mengenai keputusan ini, jangan ragu untuk menghubungi kami.