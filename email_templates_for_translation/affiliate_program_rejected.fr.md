---
template_type: affiliate_program_rejected
category: Affiliate Program
---

# Email Template: affiliate_program_rejected

## Subject
Mise à jour de la candidature

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
          Mise à jour de l'application
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
          Merci d'avoir postulé pour promouvoir {{ program_name }}.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Après avoir examiné votre candidature, nous avons décidé de ne pas l'approuver pour le moment.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Vous pouvez toujours promouvoir d'autres programmes dans notre réseau d'affiliés.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#6c757d" color="#ffffff" href="{{ portal_url }}">
          Voir d'autres programmes
        </mj-button>
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
Mise à jour de la candidature

Bonjour {{ affiliate_name }},

Merci d'avoir postulé pour promouvoir {{ program_name }}.

Après avoir examiné votre candidature, nous avons décidé de ne pas l'approuver pour le moment.

Vous pouvez toujours promouvoir d'autres programmes dans notre réseau d'affiliés.

Voir d'autres programmes: {{ portal_url }}

{{ shop_name }}
Questions? Contacter {{ support_email }}