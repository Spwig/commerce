---
template_type: blog_subscription_confirmed
category: Blog
---

# Email Template: blog_subscription_confirmed

## Subject
Confirme sua inscrição no {{ blog_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Confirme Sua Inscrição
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Olá {{ subscriber_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Obrigado por se inscrever no {{ blog_name }}! Para concluir sua inscrição e começar a receber atualizações, confirme seu endereço de e-mail.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ confirmation_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Confirmar Inscrição
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Não consegue clicar no botão? Copie e cole este link em seu navegador:
              <br/>
              <span style="color: {{ theme.color.primary|default:'#2563eb' }}; font-family: 'Courier New', monospace;">
                {{ confirmation_url }}
              </span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>Por quão confirmar?</strong>
          <br/>
          A confirmação de e-mail ajuda-nos a garantir que você deseja receber atualizações e impede o spam. Sua privacidade e caixa de entrada são importantes para nós.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Não se inscreveu? Você pode ignorar este e-mail com segurança.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
CONFIRMAR SUA INSCRIÇÃO

Olá {{ subscriber_name }},

Obrigado por se inscrever no {{ blog_name }}! Para concluir sua inscrição e começar a receber atualizações, confirme seu endereço de e-mail.

Confirmar inscrição: {{ confirmation_url }}

POR QUÃO CONFIRMAR?
A confirmação de e-mail ajuda-nos a garantir que você deseja receber atualizações e impede o spam. Sua privacidade e caixa de entrada são importantes para nós.

Não se inscreveu? Você pode ignorar este e-mail com segurança.