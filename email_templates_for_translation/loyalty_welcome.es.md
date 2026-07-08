---
template_type: loyalty_welcome
category: Loyalty Program
---

# Email Template: loyalty_welcome

## Subject
¡Bienvenido a {{ shop_name }} Rewards!

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
          🎉 ¡Bienvenido a Rewards!
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Comienza a acumular puntos con cada compra
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Hola {{ customer_name }},
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          ¡Bienvenido al programa de recompensas de {{ shop_name }}! Has sido inscrito automáticamente y puedes comenzar a acumular puntos de inmediato.
        </mj-text>

        <!-- Bonus Points (if any) -->
        {% if bonus_points %}
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="20px">
          <strong>🎁 Bonus de bienvenida: {{ bonus_points }} puntos!</strong>
        </mj-text>
        {% endif %}

        <!-- Current Tier -->
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" padding="20px 0" />
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Tu nivel:</strong> {{ current_tier }}
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
          Cómo ganar puntos
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Haz compras - Gana puntos en cada pedido<br/>
          • Escribe reseñas - Comparte tu opinión<br/>
          • Revisa a amigos - Difunde la palabra<br/>
          • Recompensas de cumpleaños - Puntos especiales en tu cumpleaños
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ account_url }}">
          Ver mis recompensas
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          {{ shop_name }}<br/>
          ¿Tienes preguntas? <a href="mailto:{{ support_email }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Contactar soporte</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
¡Bienvenido a {{ shop_name }} Rewards!

Hola {{ customer_name }},

¡Bienvenido al programa de recompensas de {{ shop_name }}! Has sido inscrito automáticamente y puedes comenzar a acumular puntos de inmediato.

{% if bonus_points %}Bonus de bienvenida: {{ bonus_points }} puntos!{% endif %}

Tu nivel: {{ current_tier }}
{{ tier_benefits }}

Cómo ganar puntos:
- Haz compras - Gana puntos en cada pedido
- Escribe reseñas - Comparte tu opinión
- Revisa a amigos - Difunde la palabra
- Recompensas de cumpleaños - Puntos especiales en tu cumpleaños

Ver tus recompensas: {{ account_url }}

{{ shop_name }}
¿Tienes preguntas? Contacta a {{ support_email }}