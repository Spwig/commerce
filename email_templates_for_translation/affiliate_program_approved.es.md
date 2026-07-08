---
template_type: affiliate_program_approved
category: Affiliate Program
---

# Email Template: affiliate_program_approved

## Subject
Aprobado para {{ program_name }}!

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
          ✓ Programa aprobado!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Success Banner -->
    <mj-section background-color="#007bff" padding="40px 20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#ffffff" align="center">
          {{ program_name }}
        </mj-text>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-top="10px">
          ¡Has sido aprobado!
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
          ¡Buena noticia! Has sido aprobado para promocionar {{ program_name }}.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          ¡Empieza a compartir este programa para ganar comisiones!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          Obtener enlaces de afiliado
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          ¿Preguntas? <a href="mailto:{{ support_email }}" style="color: #007bff;">Contáctanos</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Aprobado para {{ program_name }}!

Hola {{ affiliate_name }},

¡Buena noticia! Has sido aprobado para promocionar {{ program_name }}.

¡Empieza a compartir este programa para ganar comisiones!

Obtener enlaces de afiliado: {{ portal_url }}

{{ shop_name }}
¿Preguntas? Contacto {{ support_email }}

