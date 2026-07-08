---
template_type: affiliate_program_rejected
category: Affiliate Program
---

# Email Template: affiliate_program_rejected

## Subject
Actualización de la solicitud de programa

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
          Actualización de la solicitud
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          Hola {{ affiliate_name }},
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Gracias por aplicar para promocionar {{ program_name }}.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Después de revisar su solicitud, hemos decidido no aprobarla en este momento.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Aún puede promocionar otros programas en nuestra red de afiliados.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#6c757d" color="#ffffff" href="{{ portal_url }}">
          Ver otros programas
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          ¿Preguntas? <a href="mailto:{{ support_email }}" style="color: #007bff;">Contáctenos</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Actualización de la solicitud de programa

Hola {{ affiliate_name }},

Gracias por aplicar para promocionar {{ program_name }}.

Después de revisar su solicitud, hemos decidido no aprobarla en este momento.

Aún puede promocionar otros programas en nuestra red de afiliados.

Ver otros programas: {{ portal_url }}

{{ shop_name }}
¿Preguntas? Contáctenos {{ support_email }}