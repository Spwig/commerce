---
template_type: form_submission_approved
category: Form Builder
---

# Email Template: form_submission_approved

## Subject
✓ {{ form_name }} onaylandı!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          ✓ Onaylandı!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Harika Haber!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Merhaba {{ submitter_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ form_name }} başvurusu onaylandı!
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Başvuru Detayları:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Form:</strong> {{ form_name }}<br/>
              <strong>Basvuru Tarihi:</strong> {{ submission_date }}<br/>
              <strong>Onay Tarihi:</strong> {{ approval_date }}<br/>
              <strong>Başvuru Numarası:</strong> {{ submission_id }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if approval_message %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Ekibimizden Mesaj:
        </mj-text>
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              {{ approval_message }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Sonraki Adım Nedir?
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ next_steps }}
        </mj-text>

        <mj-spacer height="30px" />

        {% if cta_url %}
        <mj-button href="{{ cta_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          {{ cta_text|default:'Detayları Gör' }}
        </mj-button>
        {% endif %}

        {% if support_url %}
        <mj-spacer height="20px" />
        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Sorularınız var mı? <a href="{{ support_url }}">Destek ile iletişime geçin</a>
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ ONAYLANDI!

Harika Haber!

Merhaba {{ submitter_name }},

{{ form_name }} başvurusu onaylandı!

BAŞVURU DETAYLARI:
- Form: {{ form_name }}
- Submitted: {{ submission_date }}
- Approved: {{ approval_date }}
- Reference #: {{ submission_id }}

{% if approval_message %}EKİBİMİZDEN MESAJ:
{{ approval_message }}{% endif %}

SONRAKİ ADIM NEDİR?
{{ next_steps }}

{% if cta_url %}{{ cta_text|default:'Detayları Gör' }}: {{ cta_url }}{% endif %}

{% if support_url %}Sorularınız var mı? Destek ile iletişime geçin: {{ support_url }}{% endif %}