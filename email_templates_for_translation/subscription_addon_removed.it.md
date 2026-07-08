---
template_type: subscription_addon_removed
category: Subscriptions
---

# Email Template: subscription_addon_removed

## Subject
L'add-on {{ addon_name }} è stato rimosso dalla tua sottoscrizione

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          Add-on Rimosso
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Add-on Rimosso
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          L'add-on {{ addon_name }} è stato rimosso dalla tua sottoscrizione {{ plan_name }}.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Dettagli della Rimozione:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Add-on:</strong> {{ addon_name }}<br/>
              <strong>Sottoscrizione:</strong> {{ plan_name }}<br/>
              <strong>Rimosso Il:</strong> {{ removed_date }}<br/>
              <strong>Applicabile Da:</strong> {{ effective_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if access_until %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              Accesso Fino a {{ access_until }}
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              Continuerai ad avere accesso a {{ addon_name }} fino alla fine del tuo periodo di fatturazione corrente.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Informazioni sul Fatturazione:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Totale Precedente:</strong> {{ old_total }} / {{ billing_period }}<br/>
              <strong>Prezzo dell'Add-on:</strong> -{{ addon_price }} / {{ billing_period }}<br/>
              <strong>Totale Nuovo:</strong> {{ new_total }} / {{ billing_period }}<br/>
              <strong>Data di Applicazione:</strong> {{ effective_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if credit_applied %}
        <mj-spacer height="20px" />
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              💰 È stato applicato un credito di {{ credit_amount }} al tuo account per la parte non utilizzata di questo add-on.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        {% if data_retention_info %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Informazioni Importanti:
        </mj-text>
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ data_retention_info }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Hai Bisogno di Riaggiungerlo?
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Puoi riaggiungere {{ addon_name }} alla tua sottoscrizione in qualsiasi momento.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-button href="{{ addons_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Esplora gli Add-on
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ account_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Visualizza la Mia Sottoscrizione
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
ADD-ON RIMOSSO

Add-on Rimosso

Hi {{ customer_name }},

L'add-on {{ addon_name }} è stato rimosso dalla tua sottoscrizione {{ plan_name }}.

DETTAGLI DELLA RIMOZIONE:
- Add-on: {{ addon_name }}
- Sottoscrizione: {{ plan_name }}
- Rimozione Effettuata: {{ removed_date }}
- Applicabile Da: {{ effective_date }}

{% if access_until %}
ACCESSO FINO A {{ access_until }}:
You'll continue to have access to {{ addon_name }} until the end of your current billing period.
{% endif %}

INFORMAZIONI SULLA FATTURAZIONE:
- Totale Precedente: {{ old_total }} / {{ billing_period }}
- Prezzo dell'Add-on: -{{ addon_price }} / {{ billing_period }}
- Totale Nuovo: {{ new_total }} / {{ billing_period }}
- Data di Applicazione: {{ effective_date }}

{% if credit_applied %}
💰 È stato applicato un credito di {{ credit_amount }} al tuo account per la parte non utilizzata di questo add-on.
{% endif %}

{% if data_retention_info %}
INFORMAZIONI IMPORTANTI:
{{ data_retention_info }}
{% endif %}

HAI BISOGNO DI RIAGGIUNGERLO?
You can add {{ addon_name }} back to your subscription at any time.

Browse add-ons: {{ addons_url }}
View my subscription: {{ account_url }}