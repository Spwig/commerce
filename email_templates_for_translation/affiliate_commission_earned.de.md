---
template_type: affiliate_commission_earned
category: Affiliate Program
---

# Email Template: affiliate_commission_earned

## Subject
Sie haben eine {{ commission_amount }} Provision verdient!

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="#f8f9fa">
    <!-- Header -->
    <mj-section background-color="#ffffff" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="#212529" align="center">
          💰 Provision verdient!
        </mj-text>
        <mj-text font-size="18px" color="#6c757d" align="center">
          Große Nachrichten von {{ shop_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Commission Display -->
    <mj-section background-color="#28a745" padding="40px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-bottom="10px">
          💵 Ihre Provision
        </mj-text>
        <mj-text font-size="48px" font-weight="bold" color="#ffffff" align="center" line-height="1">
          {{ commission_amount }}
        </mj-text>
        <mj-text font-size="14px" color="rgba(255, 255, 255, 0.9)" align="center" padding-top="10px">
          Aus Bestellung #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          Hi {{ affiliate_name }},
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Herzlichen Glückwunsch! Sie haben eine {{ commission_amount }} Provision aus der Bestellung #{{ order_number }} verdient.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Machen Sie weiter mit der Promotion von {{ shop_name }}, um mehr Provisionen zu verdienen. Je mehr Verkäufe Sie erzeugen, desto mehr verdienen Sie!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Commission Details -->
    <mj-section background-color="#f8f9fa" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          <strong>Bestellnummer:</strong> #{{ order_number }}<br/>
          <strong>Provisionsbetrag:</strong> {{ commission_amount }}<br/>
          <strong>Provisionsrate:</strong> {{ commission_rate }}%
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          Affiliate-Dashboard ansehen
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          Fragen? <a href="mailto:{{ support_email }}" style="color: #007bff;">Support kontaktieren</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Sie haben eine {{ commission_amount }} Provision verdient!

Hi {{ affiliate_name }},

Herzlichen Glückwunsch! Sie haben eine {{ commission_amount }} Provision aus der Bestellung #{{ order_number }} verdient.

Provisionsdetails:
- Bestellnummer: #{{ order_number }}
- Provisionsbetrag: {{ commission_amount }}
- Provisionsrate: {{ commission_rate }}%

Machen Sie weiter mit der Promotion von {{ shop_name }}, um mehr Provisionen zu verdienen.

Sehen Sie sich Ihr Dashboard an: {{ portal_url }}

{{ shop_name }}
Fragen? Kontaktieren Sie {{ support_email }}