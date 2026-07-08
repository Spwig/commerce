---
template_type: form_submission_admin_notification
category: Form Builder
---

# Email Template: form_submission_admin_notification

## Subject
Nuova {{ form_name }} Invio da {{ submitter_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          📝 Nuovo Invio del Modulo
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Nuovo Invio Ricevuto
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          &Egrave; stato ricevuto un nuovo invio per {{ form_name }}.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Informazioni sull'Invio:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Modulo:</strong> {{ form_name }}<br/>
              <strong>Inviato da:</strong> {{ submitter_name }}<br/>
              <strong>Email:</strong> {{ submitter_email }}<br/>
              <strong>Inviato:</strong> {{ submission_date }}<br/>
              <strong>Numero di riferimento:</strong> {{ submission_id }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Dati Inviati:
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
          Visualizza nell'amministrazione
        </mj-button>

        {% if reply_to_email %}
        <mj-spacer height="10px" />
        <mj-button href="mailto:{{ reply_to_email }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Rispondi all'autore dell'invio
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📝 NUOVO INVIO DEL MODULO

Nuovo Invio Ricevuto

&egrave; stato ricevuto un nuovo invio per {{ form_name }}.

INFORMAZIONI SULL'INVIO:
- Modulo: {{ form_name }}
- Inviato da: {{ submitter_name }}
- Email: {{ submitter_email }}
- Inviato: {{ submission_date }}
- Numero di riferimento: {{ submission_id }}

DATI INVIATI:
{% for field in submission_data %}
{{ field.label }}:
{{ field.value }}

{% endfor %}

Visualizza nell'amministrazione: {{ admin_submission_url }}
{% if reply_to_email %}Rispondi all'autore dell'invio: mailto:{{ reply_to_email }}{% endif %}