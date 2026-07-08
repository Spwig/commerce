---
template_type: subscription_addon_removed
category: Subscriptions
---

# Email Template: subscription_addon_removed

## Subject
Das Add-on {{ addon_name }} wurde aus Ihrem Abonnement entfernt

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          Add-on entfernt
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Add-on entfernt
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Das Add-on {{ addon_name }} wurde aus Ihrem {{ plan_name }}-Abonnement entfernt.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Entfernungsdetails:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Add-on:</strong> {{ addon_name }}<br/>
              <strong>Abonnement:</strong> {{ plan_name }}<br/>
              <strong>Entfernt am:</strong> {{ removed_date }}<br/>
              <strong>Gültig ab:</strong> {{ effective_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if access_until %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              Zugriff bis {{ access_until }}
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              Sie haben weiterhin Zugriff auf {{ addon_name }} bis zum Ende Ihres aktuellen Abrechnungszeitraums.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Abrechnungsinformationen:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Früherer Gesamtbetrag:</strong> {{ old_total }} / {{ billing_period }}<br/>
              <strong>Add-on-Preis:</strong> -{{ addon_price }} / {{ billing_period }}<br/>
              <strong>Neuer Gesamtbetrag:</strong> {{ new_total }} / {{ billing_period }}<br/>
              <strong>Gültig ab:</strong> {{ effective_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if credit_applied %}
        <mj-spacer height="20px" />
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              💰 Ein Guthaben von {{ credit_amount }} wurde Ihrem Konto für den nicht genutzten Teil dieses Add-ons gutgeschrieben.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        {% if data_retention_info %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Wichtige Informationen:
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
          Brauchen Sie es zurück?
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Sie können das Add-on {{ addon_name }} jederzeit Ihrem Abonnement hinzufügen.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-button href="{{ addons_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Add-ons durchsuchen
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ account_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Mein Abonnement ansehen
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
ADD-ON ENTFERNT

Add-on entfernt

Hi {{ customer_name }},

Das Add-on {{ addon_name }} wurde aus Ihrem {{ plan_name }}-Abonnement entfernt.

ENTFERNUNGSDETAILS:
- Add-on: {{ addon_name }}
- Abonnement: {{ plan_name }}
- Entfernt am: {{ removed_date }}
- Gültig ab: {{ effective_date }}

{% if access_until %}
ZUGRIFF BIS {{ access_until }}:
Sie haben weiterhin Zugriff auf {{ addon_name }} bis zum Ende Ihres aktuellen Abrechnungszeitraums.
{% endif %}

ABRECHNUNGSDATEN:
- Früherer Gesamtbetrag: {{ old_total }} / {{ billing_period }}
- Add-on-Preis: -{{ addon_price }} / {{ billing_period }}
- Neuer Gesamtbetrag: {{ new_total }} / {{ billing_period }}
- Gültig ab: {{ effective_date }}

{% if credit_applied %}
💰 Ein Guthaben von {{ credit_amount }} wurde Ihrem Konto für den nicht genutzten Teil dieses Add-ons gutgeschrieben.
{% endif %}

{% if data_retention_info %}
WICHTIGE INFORMATIONEN:
{{ data_retention_info }}
{% endif %}

BRAUCHEN SIE ES ZURÜCK?
Sie können das Add-on {{ addon_name }} jederzeit Ihrem Abonnement hinzufügen.

Add-ons durchsuchen: {{ addons_url }}
Mein Abonnement ansehen: {{ account_url }}