---
template_type: form_submission_admin_notification
category: Form Builder
---

# Email Template: form_submission_admin_notification

## Subject
Nueva presentación de {{ form_name }} de {{ submitter_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          📝 Nueva presentación de formulario
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Nueva presentación recibida
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Se ha recibido una nueva presentación de {{ form_name }}.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Información de la presentación:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Formulario:</strong> {{ form_name }}<br/>
              <strong>Presentado por:</strong> {{ submitter_name }}<br/>
              <strong>Email:</strong> {{ submitter_email }}<br/>
              <strong>Presentado:</strong> {{ submission_date }}<br/>
              <strong>Número de referencia:</strong> {{ submission_id }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Datos presentados:
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
          Ver en el administrador
        </mj-button>

        {% if reply_to_email %}
        <mj-spacer height="10px" />
        <mj-button href="mailto:{{ reply_to_email }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Responder al remitente
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📝 NUEVA PRESENTACIÓN DE FORMULARIO

Nueva presentación recibida

Se ha recibido una nueva presentación de {{ form_name }}.

INFORMACIÓN DE LA PRESENTACIÓN:
- Formulario: {{ form_name }}
- Presentado por: {{ submitter_name }}
- Email: {{ submitter_email }}
- Presentado: {{ submission_date }}
- Número de referencia: {{ submission_id }}

DATOS PRESENTADOS:
{% for field in submission_data %}
{{ field.label }}:
{{ field.value }}

{% endfor %}

Ver en el administrador: {{ admin_submission_url }}
{% if reply_to_email %}Responder al remitente: mailto:{{ reply_to_email }}{% endif %}