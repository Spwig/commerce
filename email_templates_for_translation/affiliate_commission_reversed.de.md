---
template_type: affiliate_commission_reversed
category: Affiliate Program
---

# Email Template: affiliate_commission_reversed

## Subject
Kommission rückgängig gemacht - Bestellung #{{ order_number }}

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
          Kommission rückgängig gemacht
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
          Die Kommission für Bestellung #{{ order_number }} ({{ commission_amount }}) wurde aufgrund einer Kundenrückgabe zurückgewiesen.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Wenn Kunden Rückgaben anfordern, werden alle damit verbundenen Kommissionen automatisch zurückgewiesen, um eine korrekte Buchhaltung sicherzustellen.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Dies ist ein normaler Teil des Affiliate-Prozesses. Fahren Sie mit der Promotion von {{ shop_name }} fort, um neue Kommissionen zu verdienen!
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
          Fragen? <a href="mailto:{{ support_email }}" style="color: #007bff;">Unterstützung kontaktieren</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Kommission rückgängig gemacht - Bestellung #{{ order_number }}

Hi {{ affiliate_name }},

Die Kommission für Bestellung #{{ order_number }} ({{ commission_amount }}) wurde aufgrund einer Kundenrückgabe zurückgewiesen.

Wenn Kunden Rückgaben anfordern, werden alle damit verbundenen Kommissionen automatisch zurückgewiesen, um eine korrekte Buchhaltung sicherzustellen.

Dies ist ein normaler Teil des Affiliate-Prozesses. Fahren Sie mit der Promotion von {{ shop_name }} fort, um neue Kommissionen zu verdienen!

View your dashboard: {{ portal_url }}

{{ shop_name }}
Fragen? Kontaktieren Sie {{ support_email }}