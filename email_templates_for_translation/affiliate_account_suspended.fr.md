---
template_type: affiliate_account_suspended
category: Affiliate Program
---

# Email Template: affiliate_account_suspended

## Subject
Important : Compte suspendu

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
          Compte suspendu
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          Bonjour {{ affiliate_name }},
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Votre compte affilié avec {{ shop_name }} a été suspendu.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Cela est généralement dû à une violation des conditions générales de notre programme d'affiliation.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Si vous pensez que cela est une erreur ou si vous souhaitez discuter de cette décision, veuillez contacter notre équipe de support.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          Questions? <a href="mailto:{{ support_email }}" style="color: #007bff;">Contacter le support</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Important : Compte suspendu

Bonjour {{ affiliate_name }},

Votre compte affilié avec {{ shop_name }} a été suspendu.

Cela est généralement dû à une violation des conditions générales de notre programme d'affiliation.

Si vous pensez que cela est une erreur ou si vous souhaitez discuter de cette décision, veuillez contacter notre équipe de support.

{{ shop_name }}
Questions? Contacter {{ support_email }}