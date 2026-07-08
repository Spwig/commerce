---
template_type: loyalty_anniversary_bonus
category: Loyalty Program
---

# Email Template: loyalty_anniversary_bonus

## Subject
🎉 {{ years_as_member }} Año{{ years_as_member|pluralize }} con {{ shop_name }} - ¡Gracias!

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="28px" align="center">🎉</mj-text>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          {{ years_as_member }} Año{{ years_as_member|pluralize }} Juntos!
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hola {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hoy marca {{ years_as_member }} año{{ years_as_member|pluralize }} desde que te uniste a nuestro programa de fidelidad. ¡Gracias por ser un miembro tan valioso!
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="18px" font-weight="bold" color="#065f46" align="center">
              Bonus de Aniversario
            </mj-text>
            <mj-text font-size="36px" font-weight="bold" color="#047857" align="center">
              {{ bonus_points }} Puntos
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              Añadidos para celebrar {{ years_as_member }} año{{ years_as_member|pluralize }}!
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Tu viaje de {{ years_as_member }}-Año:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          <strong>Member Since:</strong> {{ member_since }}<br/>
          <strong>Total Orders:</strong> {{ total_orders }}<br/>
          <strong>Points Earned:</strong> {{ lifetime_points }} puntos<br/>
          <strong>Current Tier:</strong> {{ loyalty_tier }}<br/>
          <strong>Total Savings:</strong> {{ total_savings }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ loyalty_dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Ver tu panel de fidelidad
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          ¡Gracias por {{ years_as_member }} año{{ years_as_member|pluralize }} increíbles!
          <br/>
          ¡Brindemos por muchos más 🥂
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 {{ years_as_member }} AÑO{{ years_as_member|pluralize|upper }} JUNTOS!

Hola {{ customer_name }},

Hoy marca {{ years_as_member }} año{{ years_as_member|pluralize }} desde que te uniste a nuestro programa de fidelidad. ¡Gracias por ser un miembro tan valioso!

BONUS DE ANIVERSARIO:
{{ bonus_points }} Puntos
Añadidos para celebrar {{ years_as_member }} año{{ years_as_member|pluralize }}!

TU {{ years_as_member }}-AÑO JORNADA:
- Member Since: {{ member_since }}
- Total Orders: {{ total_orders }}
- Points Earned: {{ lifetime_points }} puntos
- Current Tier: {{ loyalty_tier }}
- Total Savings: {{ total_savings }}

Ver tu panel de fidelidad: {{ loyalty_dashboard_url }}

¡Gracias por {{ years_as_member }} año{{ years_as_member|pluralize }} increíbles!
¡Brindemos por muchos más 🥂