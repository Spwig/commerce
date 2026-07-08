---
template_type: affiliate_payout_failed
category: Affiliate Program
---

# Email Template: affiliate_payout_failed

## Subject
Aktion erforderlich: Auszahlung fehlgeschlagen

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
        <mj-text font-size="32px" font-weight="bold" color="#dc3545" align="center">
          ⚠️ Auszahlung fehlgeschlagen
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Warning Display -->
    <mj-section background-color="#fff3cd" padding="40px 20px">
      <mj-column>
        <mj-text font-size="48px" font-weight="bold" color="#856404" align="center" line-height="1">
          {{ payout_amount }}
        </mj-text>
        <mj-text font-size="16px" color="#856404" align="center" padding-top="10px">
          Auszahlung-ID: {{ payout_id }}
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
          Wir haben ein Problem bei der Verarbeitung Ihrer Auszahlung von {{ payout_amount }} festgestellt.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Dies liegt in der Regel an falschen Zahlungsinformationen oder an einem Problem mit Ihrem Zahlungsdienstleister.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Bitte aktualisieren Sie Ihre Zahlungsinformationen in Ihrem Affiliate-Dashboard und kontaktieren Sie unser Support-Team, um dieses Problem zu beheben.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#dc3545" color="#ffffff" href="{{ portal_url }}">
          Zahlungsinformationen aktualisieren
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          Benötigen Sie Hilfe? <a href="mailto:{{ support_email }}" style="color: #007bff;">Support kontaktieren</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Aktion erforderlich: Auszahlung fehlgeschlagen

Hi {{ affiliate_name }},

Wir haben ein Problem bei der Verarbeitung Ihrer Auszahlung von {{ payout_amount }} (Auszahlung-ID: {{ payout_id }}) festgestellt.

Dies liegt in der Regel an falschen Zahlungsinformationen oder an einem Problem mit Ihrem Zahlungsdienstleister.

Bitte aktualisieren Sie Ihre Zahlungsinformationen in Ihrem Affiliate-Dashboard und kontaktieren Sie unser Support-Team, um dieses Problem zu beheben.

Zahlungsinformationen aktualisieren: {{ portal_url }}

{{ shop_name }}
Benötigen Sie Hilfe? Kontaktieren Sie {{ support_email }}