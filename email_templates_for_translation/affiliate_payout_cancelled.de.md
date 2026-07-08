---
template_type: affiliate_payout_cancelled
category: Affiliate Program
---

# Email Template: affiliate_payout_cancelled

## Subject
Auszahlung abgebrochen - {{ payout_amount }}

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
          Auszahlung abgebrochen
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
          Ihre Auszahlung von {{ payout_amount }} (Auszahlungs-ID: {{ payout_id }}) wurde abgebrochen.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Wenn Sie Fragen dazu haben, warum diese Auszahlung abgebrochen wurde, wenden Sie sich bitte an unser Support-Team.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#6c757d" color="#ffffff" href="{{ portal_url }}">
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
Auszahlung abgebrochen - {{ payout_amount }}

Hi {{ affiliate_name }},

Ihre Auszahlung von {{ payout_amount }} (Auszahlungs-ID: {{ payout_id }}) wurde abgebrochen.

Wenn Sie Fragen dazu haben, warum diese Auszahlung abgebrochen wurde, wenden Sie sich bitte an unser Support-Team.

View your dashboard: {{ portal_url }}

{{ shop_name }}
Fragen? Kontaktieren Sie {{ support_email }}
