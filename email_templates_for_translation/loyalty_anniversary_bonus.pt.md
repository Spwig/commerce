---
template_type: loyalty_anniversary_bonus
category: Loyalty Program
---

# Email Template: loyalty_anniversary_bonus

## Subject
🎉 {{ years_as_member }} Ano{{ years_as_member|pluralize }} com {{ shop_name }} - Obrigado!

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="28px" align="center">🎉</mj-text>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          {{ years_as_member }} Ano{{ years_as_member|pluralize }} Juntos!
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Olá {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hoje marca {{ years_as_member }} ano{{ years_as_member|pluralize }} desde que você se juntou ao nosso programa de fidelidade. Obrigado por ser um membro tão valorizado!
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="18px" font-weight="bold" color="#065f46" align="center">
              Bônus de Aniversário
            </mj-text>
            <mj-text font-size="36px" font-weight="bold" color="#047857" align="center">
              {{ bonus_points }} Pontos
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              Adicionado para celebrar {{ years_as_member }} ano{{ years_as_member|pluralize }}!
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Seu Período de {{ years_as_member }} Ano(s):
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          <strong>Member Since:</strong> {{ member_since }}<br/>
          <strong>Total Orders:</strong> {{ total_orders }}<br/>
          <strong>Points Earned:</strong> {{ lifetime_points }} pontos<br/>
          <strong>Current Tier:</strong> {{ loyalty_tier }}<br/>
          <strong>Total Savings:</strong> {{ total_savings }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ loyalty_dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Ver seu painel de fidelidade
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Obrigado por {{ years_as_member }} ano{{ years_as_member|pluralize }} incríveis!<br/>
          Aqui vai a muitos mais 🥂
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 {{ years_as_member }} ANO{{ years_as_member|pluralize|upper }} JUNTOS!

Olá {{ customer_name }},

Hoje marca {{ years_as_member }} ano{{ years_as_member|pluralize }} desde que você se juntou ao nosso programa de fidelidade. Obrigado por ser um membro tão valorizado!

BÔNUS DE ANIVERSÁRIO:
{{ bonus_points }} Pontos
Adicionado para celebrar {{ years_as_member }} ano{{ years_as_member|pluralize }}!

SEU {{ years_as_member }}-ANO JORNADA:
- Member Since: {{ member_since }}
- Total Orders: {{ total_orders }}
- Points Earned: {{ lifetime_points }} pontos
- Current Tier: {{ loyalty_tier }}
- Total Savings: {{ total_savings }}

Ver seu painel de fidelidade: {{ loyalty_dashboard_url }}

Obrigado por {{ years_as_member }} ano{{ years_as_member|pluralize }} incríveis!
Aqui vai a muitos mais 🥂