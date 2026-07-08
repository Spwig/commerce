---
template_type: loyalty_birthday_bonus
category: Loyalty Program
---

# Email Template: loyalty_birthday_bonus

## Subject
🎂 Feliz Aniversário {{ customer_name }}! Aqui está um presente especial de {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="32px" align="center">🎂🎉🎁</mj-text>
        <mj-text font-size="26px" font-weight="bold" color="#92400e" align="center">
          Feliz Aniversário!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Feliz Aniversário, {{ customer_name }}!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Para celebrar o seu dia especial, adicionamos {{ bonus_points }} pontos bônus à sua conta de fidelidade!
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#dcfce7" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="18px" font-weight="bold" color="#065f46" align="center">
              Seu Presente de Aniversário
            </mj-text>
            <mj-text font-size="36px" font-weight="bold" color="#047857" align="center">
              {{ bonus_points }} Pontos
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              Adicionado à sua conta!
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Sua Conta de Fidelidade:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>Balanço de Pontos:</strong> {{ total_points }} pontos<br/>
          <strong>Nível Atual:</strong> {{ loyalty_tier }}<br/>
          <strong>Bonus de Aniversário:</strong> +{{ bonus_points }} pontos
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ shop_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Comece a Comprar & Use Seus Pontos
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Tenha um excelente aniversário! 🎉<br/>
          - A Equipe {{ shop_name }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎂🎉🎁 Feliz Aniversário!

Feliz Aniversário, {{ customer_name }}!

Para celebrar o seu dia especial, adicionamos {{ bonus_points }} pontos bônus à sua conta de fidelidade!

SEU PRESENTE DE ANIVERSÁRIO:
{{ bonus_points }} Pontos
Adicionado à sua conta!

SUA CONTA DE FIDELIDADE:
- Balanço de Pontos: {{ total_points }} pontos
- Nível Atual: {{ loyalty_tier }}
- Bonus de Aniversário: +{{ bonus_points }} pontos

Comece a Comprar & Use Seus Pontos: {{ shop_url }}

Tenha um excelente aniversário! 🎉
- A Equipe {{ shop_name }}