---
template_type: affiliate_account_suspended
category: Affiliate Program
---

# Email Template: affiliate_account_suspended

## Subject
Wichtig: Konto gesperrt

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
          Konto gesperrt
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
          Ihr Affiliate-Konto bei {{ shop_name }} wurde gesperrt.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Dies liegt in der Regel an einer Verletzung unserer Affiliate-Programmbedingungen und -vereinbarungen.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Wenn Sie glauben, dass dies ein Fehler ist, oder wenn Sie diese Entscheidung besprechen möchten, wenden Sie sich bitte an unser Support-Team.
        </mj-text>
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
Wichtig: Konto gesperrt

Hi {{ affiliate_name }},

Ihr Affiliate-Konto bei {{ shop_name }} wurde gesperrt.

Dies liegt in der Regel an einer Verletzung unserer Affiliate-Programmbedingungen und -vereinbarungen.

Wenn Sie glauben, dass dies ein Fehler ist, oder wenn Sie diese Entscheidung besprechen möchten, wenden Sie sich bitte an unser Support-Team.

{{ shop_name }}
Fragen? Kontaktieren Sie {{ support_email }}