---
template_type: affiliate_program_rejected
category: Affiliate Program
---

# Email Template: affiliate_program_rejected

## Subject
Antrag auf Programmaktualisierung

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
          Antrag auf Programmaktualisierung
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
          Vielen Dank, dass Sie sich beworben haben, {{ program_name }} zu bewerben.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Nach Prüfung Ihrer Bewerbung haben wir beschlossen, sie nicht in diesem Zeitpunkt zu genehmigen.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Sie können weiterhin andere Programme in unserem Affiliate-Netzwerk bewerben.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#6c757d" color="#ffffff" href="{{ portal_url }}">
          Andere Programme ansehen
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
Programm Antrag

Hi {{ affiliate_name }},

Vielen Dank, dass Sie sich beworben haben, {{ program_name }} zu bewerben.

Nach Prüfung Ihrer Bewerbung haben wir beschlossen, sie nicht in diesem Zeitpunkt zu genehmigen.

Sie können weiterhin andere Programme in unserem Affiliate-Netzwerk bewerben.

Andere Programme ansehen: {{ portal_url }}

{{ shop_name }}
Fragen? Kontaktieren Sie {{ support_email }}
