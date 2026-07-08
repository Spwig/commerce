---
template_type: affiliate_commission_approved
category: Affiliate Program
---

# Email Template: affiliate_commission_approved

## Subject
Provision genehmigt: {{ commission_amount }}

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
          ✓ Provision genehmigt!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Approval Display -->
    <mj-section background-color="#007bff" padding="40px 20px">
      <mj-column>
        <mj-text font-size="48px" font-weight="bold" color="#ffffff" align="center" line-height="1">
          {{ commission_amount }}
        </mj-text>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-top="10px">
          Für Auszahlung genehmigt
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
          Ihre Provision von {{ commission_amount }} aus der Bestellung #{{ order_number }} wurde genehmigt und wird in Ihre nächste Auszahlung einbezogen.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Auszahlungen werden gemäß der von Ihnen festgelegten Zahlungsplan bearbeitet. Sie erhalten eine weitere E-Mail, sobald die Auszahlung verarbeitet wird.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          Provisionen ansehen
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
Provision genehmigt: {{ commission_amount }}

Hi {{ affiliate_name }},

Ihre Provision von {{ commission_amount }} aus der Bestellung #{{ order_number }} wurde genehmigt und wird in Ihre nächste Auszahlung einbezogen.

Auszahlungen werden gemäß der von Ihnen festgelegten Zahlungsplan bearbeitet. Sie erhalten eine weitere E-Mail, sobald die Auszahlung verarbeitet wird.

View your commissions: {{ portal_url }}

{{ shop_name }}
Fragen? Kontaktieren Sie {{ support_email }}