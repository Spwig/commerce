---
template_type: subscription_trial_ending
category: Subscriptions
---

# Email Template: subscription_trial_ending

## Subject
⏰ Seu teste do {{ plan_name }} termina em {{ days_remaining }} dias - {{ shop_name }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          ⏰ Teste Terminando em Breve
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          Seu teste do {{ plan_name }} termina em {{ trial_end_date|date:"F d, Y" }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Trial Info Card -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-wrapper background-color="#fff7ed" padding="30px" border="2px solid {{ theme.color.warning|default:'#f59e0b' }}" border-radius="12px">
          <mj-section background-color="transparent">
            <mj-column>
              <mj-text font-size="48px" font-weight="bold" color="#ea580c" align="center" padding-bottom="10px">
                {{ days_remaining }}
              </mj-text>
              <mj-text font-size="16px" color="#9a3412" align="center" text-transform="uppercase" letter-spacing="1px">
                Dias Restantes
              </mj-text>

              <mj-divider border-color="#fed7aa" border-width="1px" padding="20px 0" />

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>Termina o Teste:</strong> {{ trial_end_date|date:"F d, Y at g:i A" }}
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>Primeiro Cobrança:</strong> {{ subscription_amount }} em {{ trial_end_date|date:"F d, Y" }}
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>Método de Pagamento:</strong> {{ payment_method }}
              </mj-text>
            </mj-column>
          </mj-section>
        </mj-wrapper>
      </mj-column>
    </mj-section>

    <!-- What Happens Next -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="20px" font-weight="600" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="15px">
          O Que Acontece em Seguida?
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.info|default:'#3b82f6' }}; font-size: 18px; margin-right: 8px;">•</span>
          Sua assinatura continuará automaticamente após o teste
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.info|default:'#3b82f6' }}; font-size: 18px; margin-right: 8px;">•</span>
          Cobraremos {{ subscription_amount }} do seu {{ payment_method }}
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.info|default:'#3b82f6' }}; font-size: 18px; margin-right: 8px;">•</span>
          Você pode cancelar a qualquer momento antes de {{ trial_end_date|date:"F d, Y" }} sem cobrança
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Buttons -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="10px 20px 30px 20px">
      <mj-column>
        <mj-button href="{{ manage_subscription_url }}" background-color="{{ theme.color.info|default:'#3b82f6' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" font-weight="600" border-radius="6px" padding="14px 32px">
          Gerenciar Assinatura
        </mj-button>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="15px">
          <a href="{{ cancel_subscription_url }}" style="color: {{ theme.color.error|default:'#ef4444' }}; text-decoration: underline;">
            Cancelar Antes do Fim do Teste
          </a>
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support Block -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          Precisa de ajuda? Entre em contato conosco em {{ support_email }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Spwig Branding Footer -->
    <mj-section padding="15px 0 10px 0" background-color="transparent">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" border-width="1px" padding="0 0 12px 0"></mj-divider>
        <mj-text align="center" padding="0" font-size="11px" color="#9ca3af" line-height="16px">
          <a href="https://spwig.com" style="color: #9ca3af; text-decoration: none; display: inline-flex; align-items: center; gap: 4px;" target="_blank">
            <img src="{{ shop_url }}/static/email_system/img/spwig-favicon.png" alt="Spwig" width="12" height="12" style="vertical-align: middle; display: inline-block;" />
            Powered by Spwig
          </a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⏰ Teste Terminando em Breve

Seu teste do {{ plan_name }} termina em {{ trial_end_date|date:"F d, Y" }}

INFORMAÇÕES DO TESTE:
{{ days_remaining }} Dias Restantes

Termina o Teste: {{ trial_end_date|date:"F d, Y at g:i A" }}
Primeira Cobrança: {{ subscription_amount }} em {{ trial_end_date|date:"F d, Y" }}
Método de Pagamento: {{ payment_method }}

O Que Acontece em Seguida?
• Sua assinatura continuará automaticamente após o teste
• Cobraremos {{ subscription_amount }} do seu {{ payment_method }}
• Você pode cancelar a qualquer momento antes de {{ trial_end_date|date:"F d, Y" }} sem cobrança

Gerenciar Assinatura: {{ manage_subscription_url }}
Cancelar Antes do Fim do Teste: {{ cancel_subscription_url }}

Precisa de ajuda? Entre em contato conosco em {{ support_email }}

---
Powered by Spwig - https://spwig.com