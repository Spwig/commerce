---
template_type: affiliate_account_rejected
category: Affiliate Program
---

# Email Template: affiliate_account_rejected

## Subject
Atualização de Candidatura de Afiliado

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
          Atualização de Candidatura
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
          Obrigado por seu interesse em participar do programa de afiliados da {{ shop_name }}.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Depois de revisar sua candidatura, decidimos não seguir em frente neste momento.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Essa decisão é baseada nos requisitos atuais do nosso programa de afiliados e pode não refletir suas qualificações ou potencial.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Você está convidado a se candidatar novamente no futuro, caso suas circunstâncias mudem.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          Dúvidas? <a href="mailto:{{ support_email }}" style="color: #007bff;">Contate o Suporte</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Atualização de Candidatura de Afiliado

Olá {{ affiliate_name }},

Obrigado por seu interesse em participar do programa de afiliados da {{ shop_name }}.

Depois de revisar sua candidatura, decidimos não seguir em frente neste momento.

Essa decisão é baseada nos requisitos atuais do nosso programa de afiliados e pode não refletir suas qualificações ou potencial.

Você está convidado a se candidatar novamente no futuro, caso suas circunstâncias mudem.

{{ shop_name }}
Dúvidas? Contate {{ support_email }}