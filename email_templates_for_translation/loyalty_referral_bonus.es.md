---
template_type: loyalty_referral_bonus
category: Loyalty Program
---

# Email Template: loyalty_referral_bonus

## Subject
🎁 Puntos Bonificación por Referir a {{ referee_name }}!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          🎁 ¡Puntos por Referencia Ganados!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ¡Gracias por Compartir, {{ customer_name }}!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          ¡Buena noticia! {{ referee_name }} acaba de unirse a nuestro programa de lealtad a través de tu referencia, y has ganado puntos adicionales.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="18px" font-weight="bold" color="#065f46" align="center">
              Ganaste
            </mj-text>
            <mj-text font-size="36px" font-weight="bold" color="#047857" align="center">
              +{{ bonus_points }} Puntos
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              Por referir a {{ referee_name }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Tu Saldo Actualizado:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>Saldo de Puntos:</strong> {{ total_points }} puntos<br/>
          <strong>Bono de Referencia:</strong> +{{ bonus_points }} puntos<br/>
          <strong>Amigos Referidos:</strong> {{ total_referrals }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              ¡Sigue Compartiendo, Sigue Ganando!
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Gana {{ points_per_referral }} puntos por cada amigo que se una. ¡No hay límite!
            </mj-text>
            <mj-spacer height="15px" />
            <mj-button href="{{ referral_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
              Comparte Tu Enlace de Referencia
            </mj-button>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ shop_url }}" background-color="#059669" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Comienza a Comprar
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎁 ¡PUNTOS DE REFERIDO GANADOS!

¡Gracias por Compartir, {{ customer_name }}!

¡Buena noticia! {{ referee_name }} acaba de unirse a nuestro programa de lealtad a través de tu referencia, y has ganado puntos adicionales.

GANASTE:
+{{ bonus_points }} Puntos
Por referir a {{ referee_name }}

TU SALDO ACTUALIZADO:
- Saldo de Puntos: {{ total_points }} puntos
- Bono de Referencia: +{{ bonus_points }} puntos
- Amigos Referidos: {{ total_referrals }}

¡SIGUE COMPARTIENDO, SIGUE GANANDO!
Gana {{ points_per_referral }} puntos por cada amigo que se una. ¡No hay límite!

Comparte tu enlace de referencia: {{ referral_url }}
Comienza a comprar: {{ shop_url }}