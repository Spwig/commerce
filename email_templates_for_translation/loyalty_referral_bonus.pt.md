---
template_type: loyalty_referral_bonus
category: Loyalty Program
---

# Email Template: loyalty_referral_bonus

## Subject
🎁 Pontos Bônus por Indicar {{ referee_name }}!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          🎁 Bônus de Indicação Ganho!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Obrigado por Compartilhar, {{ customer_name }}!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Grande notícia! {{ referee_name }} acabou de se juntar ao nosso programa de fidelidade através da sua indicação, e você ganhou pontos bônus!
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="18px" font-weight="bold" color="#065f46" align="center">
              Você Ganhou
            </mj-text>
            <mj-text font-size="36px" font-weight="bold" color="#047857" align="center">
              +{{ bonus_points }} Pontos
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              Por indicar {{ referee_name }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Seu Saldo Atualizado:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>Balanço de Pontos:</strong> {{ total_points }} pontos<br/>
          <strong>Bônus de Indicação:</strong> +{{ bonus_points }} pontos<br/>
          <strong>Amigos Indicados:</strong> {{ total_referrals }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Continue Compartilhando, Continue Ganhando!
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Ganhe {{ points_per_referral }} pontos para cada amigo que se juntar. Não há limite!
            </mj-text>
            <mj-spacer height="15px" />
            <mj-button href="{{ referral_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
              Compartilhe Seu Link de Indicação
            </mj-button>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ shop_url }}" background-color="#059669" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Comece a Comprar
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎁 BÔNUS DE INDICAÇÃO GANHO!

Obrigado por Compartilhar, {{ customer_name }}!

Grande notícia! {{ referee_name }} acabou de se juntar ao nosso programa de fidelidade através da sua indicação, e você ganhou pontos bônus!

VOCÊ GANHOU:
+{{ bonus_points }} Pontos
Por indicar {{ referee_name }}

SEU SALDO ATUALIZADO:
- Balanço de Pontos: {{ total_points }} pontos
- Bônus de Indicação: +{{ bonus_points }} pontos
- Amigos Indicados: {{ total_referrals }}

CONTINUE COMPARTILHANDO, CONTINUE GANHANDO!
Ganhe {{ points_per_referral }} pontos para cada amigo que se juntar. Não há limite!

Compartilhe seu link de indicação: {{ referral_url }}
Comece a comprar: {{ shop_url }}