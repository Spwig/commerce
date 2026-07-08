---
template_type: form_submission_admin_notification
category: Form Builder
---

# Email Template: form_submission_admin_notification

## Subject
Yeni {{ form_name }} Gönderimi - {{ submitter_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          📝 Yeni Form Gönderimi
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Yeni Gönderim Alındı
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Yeni bir {{ form_name }} gönderimi alındı.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Gönderim Bilgisi:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Form:</strong> {{ form_name }}<br/>
              <strong>Gönderen:</strong> {{ submitter_name }}<br/>
              <strong>Email:</strong> {{ submitter_email }}<br/>
              <strong>Gönderildi:</strong> {{ submission_date }}<br/>
              <strong>Referans #:</strong> {{ submission_id }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Gönderilen Veri:
        </mj-text>

        {% for field in submission_data %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="4px" padding="12px">
          <mj-column>
            <mj-text font-size="13px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ field.label }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              {{ field.value }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_submission_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Yönetici Panelinde Görüntüle
        </mj-button>

        {% if reply_to_email %}
        <mj-spacer height="10px" />
        <mj-button href="mailto:{{ reply_to_email }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Gönderene Cevap Ver
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📝 YENİ FORM GÖNDERİMİ

Yeni Gönderim Alındı

Yeni bir {{ form_name }} gönderimi alındı.

GÖNDERİM BİLGİSİ:
- Form: {{ form_name }}
- Gönderen: {{ submitter_name }}
- Email: {{ submitter_email }}
- Gönderildi: {{ submission_date }}
- Referans #: {{ submission_id }}

GÖNDERİLEN VERİ:
{% for field in submission_data %}
{{ field.label }}:
{{ field.value }}

{% endfor %}

Yönetici panelinde görüntüle: {{ admin_submission_url }}
{% if reply_to_email %}Gönderene cevap ver: mailto:{{ reply_to_email }}{% endif %}