---
template_type: referral_reward_issued_referrer
category: Referral Program
---

# Email Template: referral_reward_issued_referrer

## Subject
¡Ganaste una recompensa de {{ reward_amount }}!

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
          🎉 Ganaste una recompensa!
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Gracias por referir a {{ referee_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reward Display -->
    <mj-section background-color="{{ theme.color.success|default:'#10b981' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-bottom="10px">
          🎉 Tu recompensa
        </mj-text>
        <mj-text font-size="48px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center" line-height="1">
          {{ reward_amount }}
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-top="10px">
          {{ reward_type_display }}
        </mj-text>
        {% if expires_at %}
        <mj-text font-size="13px" color="rgba(255, 255, 255, 0.9)" align="center" padding-top="5px">
          Vence: {{ expires_at }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Hola {{ customer_name }},
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          ¡Felicidades! {{ referee_name }} acaba de realizar su primer compra usando tu enlace de referencia, y has ganado una recompensa de {{ reward_amount }}!
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          ¡Continúa compartiendo tu enlace de referencia para ganar más recompensas! Cuantos más amigos refieras, más ganarás!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Referral Stats -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="20px">
          Estadísticas de referidos
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="10px 20px 30px 20px">
      <mj-group>
        <mj-column width="50%" background-color="{{ theme.color.background|default:'#ffffff' }}" border-radius="8px" padding="20px 10px">
          <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" align="center" line-height="1">
            {{ total_referrals }}
          </mj-text>
          <mj-text font-size="13px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="8px" text-transform="uppercase">
            Referidos exitosos
          </mj-text>
        </mj-column>

        <mj-column width="50%" background-color="{{ theme.color.background|default:'#ffffff' }}" border-radius="8px" padding="20px 10px">
          <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.success|default:'#10b981' }}" align="center" line-height="1">
            {{ total_rewards_earned }}
          </mj-text>
          <mj-text font-size="13px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="8px" text-transform="uppercase">
            Recompensas totales
          </mj-text>
        </mj-column>
      </mj-group>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ referral_dashboard_url }}">
          Ver mis referidos
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Keep Sharing -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="15px">
          ¡Continúa compartiendo, ¡sigue ganando!
        </mj-text>
        <mj-text
          background-color="{{ theme.color.background|default:'#ffffff' }}"
          border="2px dashed {{ theme.color.primary|default:'#2563eb' }}"
          border-radius="8px"
          padding="15px"
          font-size="14px"
          color="{{ theme.color.primary|default:'#2563eb' }}"
          align="center"
          font-family="monospace"
        >
          {{ referral_link }}
        </mj-text>
        <mj-text font-size="13px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          Comparte este enlace con amigos para ganar más recompensas
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          {{ shop_name }}<br/>
          ¿Tienes preguntas? <a href="mailto:{{ support_email }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Contáctanos</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
¡Ganaste una recompensa de {{ reward_amount }}!

Hola {{ customer_name }},

¡Felicidades! {{ referee_name }} acaba de realizar su primer compra usando tu enlace de referencia, y has ganado una recompensa de {{ reward_amount }}!

Tu recompensa: {{ reward_amount }}
Tipo: {{ reward_type_display }}
{% if expires_at %}Vence: {{ expires_at }}{% endif %}

Estadísticas de referidos:
- Referidos exitosos: {{ total_referrals }}
- Recompensas totales: {{ total_rewards_earned }}

¡Continúa compartiendo tu enlace de referencia para ganar más recompensas:
{{ referral_link }}

Ver tus referidos: {{ referral_dashboard_url }}

{{ shop_name }}
¿Tienes preguntas? Contáctanos a {{ support_email }}