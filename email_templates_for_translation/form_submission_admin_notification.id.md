---
template_type: form_submission_admin_notification
category: Form Builder
---

# Email Template: form_submission_admin_notification

## Subject
Pengajuan {{ form_name }} Baru dari {{ submitter_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          📝 Pengajuan {{ form_name }} Baru
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Pengajuan Baru Diterima
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Sebuah pengajuan {{ form_name }} baru telah diterima.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Info Pengajuan:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Form:</strong> {{ form_name }}<br/>
              <strong>Diajukan oleh:</strong> {{ submitter_name }}<br/>
              <strong>Email:</strong> {{ submitter_email }}<br/>
              <strong>Diajukan:</strong> {{ submission_date }}<br/>
              <strong>Nomor Referensi:</strong> {{ submission_id }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Data yang Diajukan:
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
          Lihat di Admin
        </mj-button>

        {% if reply_to_email %}
        <mj-spacer height="10px" />
        <mj-button href="mailto:{{ reply_to_email }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Balas ke Pengajuan
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📝 PENGAJUAN BARU

Pengajuan Baru Diterima

Sebuah pengajuan {{ form_name }} baru telah diterima.

INFO PENGAJUAN:
- Form: {{ form_name }}
- Diajukan oleh: {{ submitter_name }}
- Email: {{ submitter_email }}
- Diajukan: {{ submission_date }}
- Nomor Referensi: {{ submission_id }}

DATA YANG DIAJUKAN:
{% for field in submission_data %}
{{ field.label }}:
{{ field.value }}

{% endfor %}

Lihat di admin: {{ admin_submission_url }}
{% if reply_to_email %}Balas ke pengajuan: mailto:{{ reply_to_email }}{% endif %}