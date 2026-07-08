---
template_type: form_submission_rejected
category: Form Builder
---

# Email Template: form_submission_rejected

## Subject
Aggiornamento sulla tua {{ form_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Aggiornamento sulla tua Richiesta
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ submitter_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Grazie per aver inviato il modulo {{ form_name }}. Dopo una revisione attenta, al momento non possiamo approvare la tua richiesta.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Dettagli della Richiesta:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Form:</strong> {{ form_name }}<br/>
              <strong>Inviato:</strong> {{ submission_date }}<br/>
              <strong>Rivisto:</strong> {{ rejection_date }}<br/>
              <strong>Riferimento #:</strong> {{ submission_id }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if rejection_reason %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Motivo:
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
              Puoi Rinviarla
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
          Invia nuovamente
        </mj-button>
        <mj-spacer height="10px" />
        {% endif %}

        {% if support_url %}
        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Contatta l'assistenza
        </mj-button>
        <mj-spacer height="20px" />
        {% endif %}

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Se hai domande su questa decisione, non esitare a contattarci.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
AGGIORNAMENTO SULLA TUA RICHIESTA

Hi {{ submitter_name }},

Grazie per aver inviato il modulo {{ form_name }}. Dopo una revisione attenta, al momento non possiamo approvare la tua richiesta.

DETTAGLI DELLA RICHIESTA:
- Form: {{ form_name }}
- Inviato: {{ submission_date }}
- Rivisto: {{ rejection_date }}
- Riferimento #: {{ submission_id }}

{% if rejection_reason %}MOTIVO:
{{ rejection_reason }}{% endif %}

{% if can_resubmit %}PUOI RINVIARLA:
{{ resubmit_instructions }}{% endif %}

{% if resubmit_url %}Invia nuovamente: {{ resubmit_url }}{% endif %}
{% if support_url %}Contatta l'assistenza: {{ support_url }}{% endif %}

Se hai domande su questa decisione, non esitare a contattarci.