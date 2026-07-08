---
template_type: affiliate_account_rejected
category: Affiliate Program
---

# Email Template: affiliate_account_rejected

## Subject
Mise à jour de la candidature affiliée

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
          Mise à jour de la candidature
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
          Merci d'avoir exprimé votre intérêt pour le programme d'affiliation {{ shop_name }}.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Après avoir examiné votre candidature, nous avons décidé de ne pas poursuivre pour le moment.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Cette décision est basée sur les exigences actuelles de notre programme d'affiliation et ne reflète peut-être pas vos qualités ou votre potentiel.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Vous pouvez postuler à nouveau à l'avenir si votre situation change.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          Questions ? <a href="mailto:{{ support_email }}" style="color: #007bff;">Contactez le support</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Mise à jour de la candidature affiliée

Bonjour {{ affiliate_name }},

Merci d'avoir exprimé votre intérêt pour le programme d'affiliation {{ shop_name }}.

Après avoir examiné votre candidature, nous avons décidé de ne pas poursuivre pour le moment.

Cette décision est basée sur les exigences actuelles de notre programme d'affiliation et ne reflète peut-être pas vos qualités ou votre potentiel.

Vous pouvez postuler à nouveau à l'avenir si votre situation change.

{{ shop_name }}
Questions ? Contactez {{ support_email }}