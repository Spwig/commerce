---
template_type: affiliate_account_activated
category: Affiliate Program
---

# Email Template: affiliate_account_activated

## Subject
Willkommen zurück! Konto wurde reaktiviert

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
          🎉 Konto wurde reaktiviert!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Success Banner -->
    <mj-section background-color="#28a745" padding="40px 20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#ffffff" align="center">
          Willkommen zurück!
        </mj-text>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-top="10px">
          Ihr Affiliate-Konto ist jetzt wieder aktiv
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
          Gute Nachrichten! Ihr Affiliate-Konto bei {{ shop_name }} wurde reaktiviert.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Sie können sofort damit beginnen, unsere Produkte zu bewerben und Provisionen zu verdienen.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          Affiliate-Dashboard aufrufen
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          Fragen? <a href="mailto:{{ support_email }}" style="color: #007bff;">Unterstützung kontaktieren</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Willkommen zurück! Konto wurde reaktiviert

Hallo {{ affiliate_name }},

Gute Nachrichten! Ihr Affiliate-Konto bei {{ shop_name }} wurde reaktiviert.

Sie können sofort damit beginnen, unsere Produkte zu bewerben und Provisionen zu verdienen.

Access your dashboard: {{ portal_url }}

{{ shop_name }}
Fragen? Kontaktieren Sie {{ support_email }}