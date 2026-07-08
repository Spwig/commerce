---
template_type: loyalty_welcome
category: Loyalty Program
---

# Email Template: loyalty_welcome

## Subject
Bem-vindo ao Programa de Recompensas da {{ shop_name }}!

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
          🎉 Bem-vindo ao Programa de Recompensas!
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Comece a ganhar pontos com cada compra
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Olá {{ customer_name }},
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Bem-vindo ao programa de recompensas da {{ shop_name }}! Você foi automaticamente inscrito e pode começar a ganhar pontos imediatamente.
        </mj-text>

        <!-- Bonus Points (if any) -->
        {% if bonus_points %}
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="20px">
          <strong>🎁 Bônus de Bem-vindo: {{ bonus_points }} pontos!</strong>
        </mj-text>
        {% endif %}

        <!-- Current Tier -->
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" padding="20px 0" />
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Sua Camada:</strong> {{ current_tier }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          {{ tier_benefits }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- How to Earn -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Como Ganhar Pontos
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Faça compras - Ganhe pontos em cada pedido<br/>
          • Escreva avaliações - Compartilhe seu feedback<br/>
          • Indique amigos - Divulgue o programa<br/>
          • Recompensas de aniversário - Pontos especiais no seu aniversário
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ account_url }}">
          Ver Minhas Recompensas
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          {{ shop_name }}<br/>
          Perguntas? <a href="mailto:{{ support_email }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Contate o Suporte</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Bem-vindo ao Programa de Recompensas da {{ shop_name }}!

Olá {{ customer_name }},

Bem-vindo ao programa de recompensas da {{ shop_name }}! Você foi automaticamente inscrito e pode começar a ganhar pontos imediatamente.

{% if bonus_points %}Bônus de Bem-vindo: {{ bonus_points }} pontos!{% endif %}

Sua Camada: {{ current_tier }}
{{ tier_benefits }}

Como Ganhar Pontos:
- Faça compras - Ganhe pontos em cada pedido
- Escreva avaliações - Compartilhe seu feedback
- Indique amigos - Divulgue o programa
- Recompensas de aniversário - Pontos especiais no seu aniversário

Ver suas recompensas: {{ account_url }}

{{ shop_name }}
Perguntas? Contate {{ support_email }}