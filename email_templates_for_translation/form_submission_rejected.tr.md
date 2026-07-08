---
template_type: form_submission_rejected
category: Form Builder
---

# Email Template: form_submission_rejected

## Subject
Gönderiminizle ilgili güncelleme: {{ form_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Gönderiminizle ilgili güncelleme
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Merhaba {{ submitter_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ form_name }} formununuzu sunmak için teşekkür ederiz. Dikkatli bir inceleme sonrasında, şu anda gönderiminizi onaylayamayız.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Gönderim Detayları:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Form:</strong> {{ form_name }}<br/>
              <strong>Gönderildi:</strong> {{ submission_date }}<br/>
              <strong>İncelemeye Alındı:</strong> {{ rejection_date }}<br/>
              <strong>Referans #:</strong> {{ submission_id }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if rejection_reason %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Neden:
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
              Tekrar Gönderilebilir
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
          Tekrar Gönder
        </mj-button>
        <mj-spacer height="10px" />
        {% endif %}

        {% if support_url %}
        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Destek ile İletişim
        </mj-button>
        <mj-spacer height="20px" />
        {% endif %}

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Bu kararla ilgili sorularınız varsa, lütfen bizimle iletişime geçmeyi çekinmeyin.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
GÖNDERİMİNİZLE İLGİLİ GÜNCELLEME

Merhaba {{ submitter_name }},

{{ form_name }} formununuzu sunmak için teşekkür ederiz. Dikkatli bir inceleme sonrasında, şu anda gönderiminizi onaylayamayız.

GÖNDERİM DETAYLARI:
- Form: {{ form_name }}
- Gönderildi: {{ submission_date }}
- İncelemeye Alındı: {{ rejection_date }}
- Referans #: {{ submission_id }}

{% if rejection_reason %}
Neden:
{{ rejection_reason }}
{% endif %}

{% if can_resubmit %}
TEKRAR GÖNDERİLEBİLİR:
{{ resubmit_instructions }}
{% endif %}

{% if resubmit_url %}Tekrar Gönder: {{ resubmit_url }}{% endif %}
{% if support_url %}Destek ile İletişim: {{ support_url }}{% endif %}

Bu kararla ilgili sorularınız varsa, lütfen bizimle iletişime geçmeyi çekinmeyin.