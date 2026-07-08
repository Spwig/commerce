---
template_type: loyalty_double_points_event
category: Loyalty Program
---

# Email Template: loyalty_double_points_event

## Subject
🔥 ¡Evento de 2X PUNTOS! - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#92400e" align="center">
          🔥 ¡EVENTO DE 2X PUNTOS!
        </mj-text>
        <mj-text font-size="18px" color="#92400e" align="center">
          {{ event_start }} - {{ event_end }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Exclusivo para Miembros de Fidelización!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hola {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Prepárate para ganar ¡UN TONELLO! Por un tiempo limitado, ganarás {{ points_multiplier }}X puntos en cada compra.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#dcfce7" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="24px" font-weight="bold" color="#047857" align="center">
              Gana {{ points_multiplier }}X Puntos
            </mj-text>
            <mj-text font-size="16px" color="#065f46" align="center">
              En todas las compras<br/>
              {{ event_start }} - {{ event_end }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Ganancias Ejemplo:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="4px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Gasta $50 → Gana {{ example_points_normal }} puntos normalmente<br/>
              <strong style="color: #047857;">Durante este evento → Gana {{ example_points_bonus }} puntos! 🎉</strong>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="4px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Gasta $100 → Gana {{ example_points_normal_2 }} puntos normalmente<br/>
              <strong style="color: #047857;">Durante este evento → Gana {{ example_points_bonus_2 }} puntos! 🎉</strong>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Tu Saldo Actual:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>Puntos:</strong> {{ current_points }} puntos<br/>
          <strong>Nivel:</strong> {{ loyalty_tier }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ shop_url }}" background-color="#dc2626" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Comprar ahora & ganar {{ points_multiplier }}X Puntos
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="#dc2626" align="center" font-weight="bold">
          El evento termina {{ event_end }} - ¡No te lo pierdas!
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🔥 ¡EVENTO DE 2X PUNTOS!
{{ event_start }} - {{ event_end }}

Exclusivo para Miembros de Fidelización!

Hola {{ customer_name }},

Prepárate para ganar ¡UN TONELLO! Por un tiempo limitado, ganarás {{ points_multiplier }}X puntos en cada compra.

GANAR {{ points_multiplier }}X PUNTOS
En todas las compras
{{ event_start }} - {{ event_end }}

GANANCIAS EJEMPLO:
- Gasta $50 → Gana {{ example_points_normal }} puntos normalmente
  Durante este evento → Gana {{ example_points_bonus }} puntos! 🎉

- Gasta $100 → Gana {{ example_points_normal_2 }} puntos normalmente
  Durante este evento → Gana {{ example_points_bonus_2 }} puntos! 🎉

TU SALDO ACTUAL:
- Puntos: {{ current_points }} puntos
- Nivel: {{ loyalty_tier }}

Comprar ahora & ganar {{ points_multiplier }}X puntos: {{ shop_url }}

El evento termina {{ event_end }} - ¡No te lo pierdas!