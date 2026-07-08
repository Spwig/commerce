---
template_type: form_submission_rejected
category: Form Builder
---

# Email Template: form_submission_rejected

## Subject
Atualização sobre a sua submissão de {{ form_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Atualização sobre sua Submissão
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Olá {{ submitter_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Obrigado por enviar o formulário {{ form_name }}. Após uma revisão cuidadosa, não conseguimos aprovar sua submissão neste momento.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detalhes da Submissão:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Formulário:</strong> {{ form_name }}<br/>
              <strong>Enviado:</strong> {{ submission_date }}<br/>
              <strong>Revisado:</strong> {{ rejection_date }}<br/>
              <strong>Número de Referência:</strong> {{ submission_id }}
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
              Você Pode Reenviar
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
          Enviar Novamente
        </mj-button>
        <mj-spacer height="10px" />
        {% endif %}

        {% if support_url %}
        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Contate o Suporte
        </mj-button>
        <mj-spacer height="20px" />
        {% endif %}

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Se você tiver dúvidas sobre essa decisão, não hesite em nos contatar.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
ATUALIZAÇÃO SOBRE SUA SUBMISSÃO

Olá {{ submitter_name }},

Obrigado por enviar o formulário {{ form_name }}. Após uma revisão cuidadosa, não conseguimos aprovar sua submissão neste momento.

DETALHES DA SUBMISSÃO:
- Formulário: {{ form_name }}
- Enviado: {{ submission_date }}
- Revisado: {{ rejection_date }}
- Número de Referência: {{ submission_id }}

{% if rejection_reason %}
MOTIVO:
{{ rejection_reason }}
{% endif %}

{% if can_resubmit %}
VOCÊ PODE REENVIAR:
{{ resubmit_instructions }}
{% endif %}

{% if resubmit_url %}Enviar novamente: {{ resubmit_url }}{% endif %}
{% if support_url %}Contate o suporte: {{ support_url }}{% endif %}

Se você tiver dúvidas sobre essa decisão, não hesite em nos contatar.