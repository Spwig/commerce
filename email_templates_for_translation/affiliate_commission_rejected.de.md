---
template_type: affiliate_commission_rejected
category: Affiliate Program
---

# Email Template: affiliate_commission_rejected

## Subject
Kommissionsstatusaktualisierung - Bestellung #{{ order_number }}

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
          Kommissionsstatusaktualisierung
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
          Wir möchten Sie informieren, dass die Kommission für die Bestellung #{{ order_number }} ({{ commission_amount }}) nicht genehmigt wurde.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Dies geschieht in der Regel, wenn eine Bestellung vor Ablauf der Kommissionsperiode storniert oder zurück erstattet wird.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Wenn Sie Fragen zu dieser Kommission haben, wenden Sie sich bitte an unser Support-Team.
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
Kommissionsstatusaktualisierung - Bestellung #{{ order_number }}

Hi {{ affiliate_name }},

Wir möchten Sie informieren, dass die Kommission für die Bestellung #{{ order_number }} ({{ commission_amount }}) nicht genehmigt wurde.

Dies geschieht in der Regel, wenn eine Bestellung vor Ablauf der Kommissionsperiode storniert oder zurück erstattet wird.

Wenn Sie Fragen zu dieser Kommission haben, wenden Sie sich bitte an unser Support-Team.

View your dashboard: {{ portal_url }}

{{ shop_name }}
Fragen? Kontaktieren Sie {{ support_email }}
