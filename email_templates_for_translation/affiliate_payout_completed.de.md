---
template_type: affiliate_payout_completed
category: Affiliate Program
---

# Email Template: affiliate_payout_completed

## Subject
✓ Auszahlung abgeschlossen: {{ payout_amount }}

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
          🎉 Auszahlung abgeschlossen!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Payout Display -->
    <mj-section background-color="#28a745" padding="40px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-bottom="10px">
          ✓ Erfolgreich bezahlt
        </mj-text>
        <mj-text font-size="48px" font-weight="bold" color="#ffffff" align="center" line-height="1">
          {{ payout_amount }}
        </mj-text>
        <mj-text font-size="14px" color="rgba(255, 255, 255, 0.9)" align="center" padding-top="10px">
          Auszahlung-ID: {{ payout_id }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          Hallo {{ affiliate_name }},
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Ihre Auszahlung in Höhe von {{ payout_amount }} wurde erfolgreich abgeschlossen!
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Die Gelder wurden an Ihre Zahlungsmethode gesendet. Je nach Bank oder Zahlungsdienstleister kann es 1-2 Geschäftstage dauern, bis das Geld auf Ihrem Konto erscheint.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Vielen Dank, dass Sie {{ shop_name }} beworben haben. Weiter so!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          Auszahlungsdetails ansehen
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
✓ Auszahlung abgeschlossen: {{ payout_amount }}

Hallo {{ affiliate_name }},

Ihre Auszahlung in Höhe von {{ payout_amount }} wurde erfolgreich abgeschlossen!

Auszahlungsdetails:
- Auszahlung-ID: {{ payout_id }}
- Betrag: {{ payout_amount }}
- Zahlungsmethode: {{ payout_method }}

Die Gelder wurden an Ihre Zahlungsmethode gesendet. Je nach Bank oder Zahlungsdienstleister kann es 1-2 Geschäftstage dauern, bis das Geld auf Ihrem Konto erscheint.

Vielen Dank, dass Sie {{ shop_name }} beworben haben. Weiter so!

Auszahlungsdetails ansehen: {{ portal_url }}

{{ shop_name }}
Fragen? Kontaktieren Sie {{ support_email }}