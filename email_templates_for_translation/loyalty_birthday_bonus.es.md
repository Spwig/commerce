---
template_type: loyalty_birthday_bonus
category: Loyalty Program
---

# Email Template: loyalty_birthday_bonus

## Subject
🎂 ¡Feliz Cumpleaños {{ customer_name }}! Aquí tienes un regalo especial de {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="32px" align="center">🎂🎉🎁</mj-text>
        <mj-text font-size="26px" font-weight="bold" color="#92400e" align="center">
          ¡Feliz Cumpleaños!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ¡Feliz Cumpleaños, {{ customer_name }}!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Para celebrar tu día especial, hemos agregado {{ bonus_points }} puntos bonus a tu cuenta de lealtad.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#dcfce7" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="18px" font-weight="bold" color="#065f46" align="center">
              Tu Regalo de Cumpleaños
            </mj-text>
            <mj-text font-size="36px" font-weight="bold" color="#047857" align="center">
              {{ bonus_points }} Puntos
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              Añadidos a tu cuenta.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Tu Cuenta de Lealtad:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>Saldo de Puntos:</strong> {{ total_points }} puntos<br/>
          <strong>Nivel Actual:</strong> {{ loyalty_tier }}<br/>
          <strong>Bono de Cumpleaños:</strong> +{{ bonus_points }} puntos
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ shop_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Comienza a comprar y usa tus puntos
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          ¡Disfruta mucho tu cumpleaños! 🎉<br/>
          - El equipo de {{ shop_name }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎂🎉🎁 ¡FELIZ CUMPLEAÑOS!

¡Feliz Cumpleaños, {{ customer_name }}!

Para celebrar tu día especial, hemos agregado {{ bonus_points }} puntos bonus a tu cuenta de lealtad.

TU REGALO DE CUMPLEAÑOS:
{{ bonus_points }} Puntos
Añadidos a tu cuenta.

TU CUENTA DE LEALTAD:
- Saldo de Puntos: {{ total_points }} puntos
- Nivel Actual: {{ loyalty_tier }}
- Bono de Cumpleaños: +{{ bonus_points }} puntos

Comienza a comprar & usa tus puntos: {{ shop_url }}

¡Disfruta mucho tu cumpleaños! 🎉
- El equipo de {{ shop_name }}