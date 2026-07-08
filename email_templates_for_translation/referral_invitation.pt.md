---
template_type: referral_invitation
category: Referral Program
---

# Email Template: referral_invitation

## Subject
{{ referrer_name }} enviou um presente para você!

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          🎁 Você foi convidado!
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          {{ referrer_name }} quer compartilhar {{ shop_name }} com você
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reward Offer -->
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="18px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-bottom="10px">
          Pegue Seu Presente de Bem-vindo
        </mj-text>
        <mj-text font-size="48px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center" line-height="1">
          {{ reward_amount }}
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-top="10px">
          Na sua primeira compra
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Personal Message -->
    {% if personal_message %}
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" font-style="italic" padding="15px" background-color="{{ theme.color.background|default:'#ffffff' }}" border-left="3px solid {{ theme.color.primary|default:'#2563eb' }}">
          "{{ personal_message }}"
          <br/><br/>
          - {{ referrer_name }}
        </mj-text>
      </mj-column>
    </mj-section>
    {% endif %}

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Olá,
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          {{ referrer_name }} acha que você vai adorar comprar em {{ shop_name }}. Para te dar as boas-vindas, estamos oferecendo {{ reward_amount }} de desconto na sua primeira compra!
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Basta clicar no botão abaixo para começar e seu recompensa será aplicada automaticamente em sua primeira encomenda.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- How it Works -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="10px">
          Como Funciona
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          1. Clique no botão para visitar {{ shop_name }}<br/>
          2. Navegue e adicione itens ao seu carrinho<br/>
          3. Conclua sua compra<br/>
          4. Seu {{ reward_amount }} de recompensa é aplicado automaticamente!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.success|default:'#10b981' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ referral_link }}">
          Reclamar Meu Presente de {{ reward_amount }}
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          {{ shop_name }}<br/>
          Esta convite foi enviado por {{ referrer_name }}<br/>
          Perguntas? <a href="mailto:{{ support_email }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Contate o Suporte</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
{{ referrer_name }} enviou um presente para você!

Olá,

{{ referrer_name }} acha que você vai adorar comprar em {{ shop_name }}. Para te dar as boas-vindas, estamos oferecendo {{ reward_amount }} de desconto na sua primeira compra!

{% if personal_message %}"{{ personal_message }}"
- {{ referrer_name }}
{% endif %}

Como Funciona:
1. Visite {{ shop_name }}
2. Navegue e adicione itens ao seu carrinho
3. Conclua sua compra
4. Seu {{ reward_amount }} de recompensa é aplicado automaticamente!

Reclame seu presente: {{ referral_link }}

{{ shop_name }}
Este convite foi enviado por {{ referrer_name }}
Perguntas? Contate {{ support_email }}