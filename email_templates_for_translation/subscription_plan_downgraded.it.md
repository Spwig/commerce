---
template_type: subscription_plan_downgraded
category: Subscriptions
---

# Email Template: subscription_plan_downgraded

## Subject
Il tuo piano di abbonamento è stato modificato in {{ new_plan_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          Piano Modificato
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Piano di Abbonamento Aggiornato
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Ciao {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Il tuo piano di abbonamento è stato modificato in {{ new_plan_name }}.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Dettagli del Cambio del Piano:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Piano Precedente:</strong> {{ old_plan_name }}<br/>
              <strong>Nuovo Piano:</strong> {{ new_plan_name }}<br/>
              <strong>Cambiato Il:</strong> {{ downgrade_date }}<br/>
              <strong>Applicabile Da:</strong> {{ effective_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Cosa Cambia:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ plan_changes }}
        </mj-text>

        {% if features_lost %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              Funzionalità Non Disponibili Più:
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ features_lost }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Informazioni di Fatturazione:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Nuovo Prezzo:</strong> {{ new_price }} / {{ billing_period }}<br/>
              <strong>Data di Applicazione:</strong> {{ effective_date }}<br/>
              <strong>Data di Fatturazione Successiva:</strong> {{ next_billing_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if credit_applied %}
        <mj-spacer height="20px" />
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              💰 È stata applicata una credito di {{ credit_amount }} al tuo account per la parte non utilizzata del tuo piano precedente.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Cambiato Idea?
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color_secondary|default:'#6b7280' }}" align="center">
          Puoi tornare a {{ old_plan_name }} in qualsiasi momento.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-button href="{{ upgrade_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Aggiorna Piano
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ account_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Visualizza il Mio Abbonamento
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
PIANO MODIFICATO

Piano di Abbonamento Aggiornato

Ciao {{ customer_name }},

Il tuo piano di abbonamento è stato modificato in {{ new_plan_name }}.

DETTAGLI DEL CAMBIO DEL PIANO:
- Piano Precedente: {{ old_plan_name }}
- Nuovo Piano: {{ new_plan_name }}
- Cambiato Il: {{ downgrade_date }}
- Applicabile Da: {{ effective_date }}

COSA CAMBIA:
{{ plan_changes }}

{% if features_lost %}
FUNZIONALITÀ NON DISPOINIBILI PIÙ:
{{ features_lost }}
{% endif %}

INFORMAZIONI DI FATTURAZIONE:
- Nuovo Prezzo: {{ new_price }} / {{ billing_period }}
- Data di Applicazione: {{ effective_date }}
- Data di Fatturazione Successiva: {{ next_billing_date }}

{% if credit_applied %}
💰 È stato applicato un credito di {{ credit_amount }} al tuo account per la parte non utilizzata del tuo piano precedente.
{% endif %}

CAMBIATO IDEA?
Puoi tornare a {{ old_plan_name }} in qualsiasi momento.

Aggiorna piano: {{ upgrade_url }}
Visualizza il mio abbonamento: {{ account_url }}