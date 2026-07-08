---
template_type: affiliate_account_rejected
category: Affiliate Program
---

# Email Template: affiliate_account_rejected

## Subject
Aktualisierung der Affiliate-Anmeldung

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
          Aktualisierung der Anmeldung
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
          Vielen Dank für Ihr Interesse daran, dem Affiliate-Programm von {{ shop_name }} beizutreten.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Nach Prüfung Ihrer Bewerbung haben wir uns entschieden, nicht weiterzugehen.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Diese Entscheidung basiert auf unseren aktuellen Anforderungen des Affiliate-Programms und spiegelt nicht unbedingt Ihre Qualifikationen oder Ihr Potenzial wider.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Sie können sich gerne erneut bewerben, wenn sich Ihre Umstände ändern.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          Fragen? <a href="mailto:{{ support_email }}" style="color: #007bff;">Kontaktieren Sie den Unterstützungs-Team</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Aktualisierung der Affiliate-Anmeldung

Hi {{ affiliate_name }},

Vielen Dank für Ihr Interesse daran, dem {{ shop_name }} Affiliate-Programm beizutreten.

Nach Prüfung Ihrer Bewerbung haben wir uns entschieden, nicht weiterzugehen.

Diese Entscheidung basiert auf unseren aktuellen Affiliate-Programm-Anforderungen und spiegelt nicht unbedingt Ihre Qualifikationen oder Ihr Potenzial wider.

Sie können sich gerne erneut bewerben, wenn sich Ihre Umstände ändern.

{{ shop_name }}
Fragen? Kontaktieren Sie {{ support_email }}