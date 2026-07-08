---
template_type: affiliate_program_rejected
category: Affiliate Program
---

# Email Template: affiliate_program_rejected

## Subject
Atualização de Aplicação

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
          Atualização de Aplicação
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          Olá {{ affiliate_name }},
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Obrigado por se candidatar a promover {{ program_name }}.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Depois de revisar sua solicitação, decidimos não aprovar nesse momento.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Você ainda pode promover outros programas em nossa rede de afiliados.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#6c757d" color="#ffffff" href="{{ portal_url }}">
          Ver Outros Programas
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          Perguntas? <a href="mailto:{{ support_email }}" style="color: #007bff;">Contate o Suporte</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Atualização de Aplicação

Olá {{ affiliate_name }},

Obrigado por se candidatar a promover {{ program_name }}.

Depois de revisar sua solicitação, decidimos não aprovar nesse momento.

Você ainda pode promover outros programas em nossa rede de afiliados.

Ver outros programas: {{ portal_url }}

{{ shop_name }}
Perguntas? Contate {{ support_email }}