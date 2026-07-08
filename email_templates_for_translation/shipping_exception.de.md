---
template_type: shipping_exception
category: Shipping
---

# Email Template: shipping_exception

## Subject
Lieferproblem - Bestellung #{{ order_number }} erfordert Aufmerksamkeit

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Lieferproblem
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Wir schreiben, um Sie über eine Ausnahme bei Ihrer Lieferung zu informieren. Wir arbeiten daran, dieses Problem so schnell wie möglich zu lösen.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#92400e">
              Ausnahmedetails:
            </mj-text>
            <mj-text color="#92400e">
              <strong>Ausnahmetyp:</strong> {{ exception_type }}<br/>
              <strong>Beschreibung:</strong> {{ exception_description }}<br/>
              <strong>Geschah:</strong> {{ exception_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Bestellinformationen:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Bestellnummer:</strong> {{ order_number }}<br/>
              <strong>Tracking-Nummer:</strong> {{ tracking_number }}<br/>
              <strong>Frachtführer:</strong> {{ carrier_name }}<br/>
              <strong>Aktueller Standort:</strong> {{ current_location }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Was geschieht als Nächstes?
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          {{ resolution_steps }}
        </mj-text>

        <mj-spacer height="20px" />

        {% if action_required %}
        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              ⚠️ Aktion erforderlich:
            </mj-text>
            <mj-text color="#7f1d1d">
              {{ action_required_description }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="20px" />
        {% endif %}

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Ihre Bestellung verfolgen
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Support kontaktieren
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ LIEFERPROBLEM

Hi {{ customer_name }},

Wir schreiben, um Sie über eine Ausnahme bei Ihrer Lieferung zu informieren. Wir arbeiten daran, dieses Problem so schnell wie möglich zu lösen.

AUSNAHMEDETAILS:
- Ausnahmetyp: {{ exception_type }}
- Beschreibung: {{ exception_description }}
- Geschah: {{ exception_date }}

BESTELLINFORMATIONEN:
- Bestellnummer: {{ order_number }}
- Tracking-Nummer: {{ tracking_number }}
- Frachtführer: {{ carrier_name }}
- Aktueller Standort: {{ current_location }}

WAS GESCHIEHT ALS NÄCHSTES?
{{ resolution_steps }}

{% if action_required %}
⚠️ Aktion erforderlich:
{{ action_required_description }}
{% endif %}

Ihre Bestellung verfolgen: {{ tracking_url }}
Support kontaktieren: {{ support_url }}