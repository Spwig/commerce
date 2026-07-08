---
template_type: loyalty_double_points_event
category: Loyalty Program
---

# Email Template: loyalty_double_points_event

## Subject
🔥 Evento de 2X Pontos Começa Agora! - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#92400e" align="center">
          🔥 EVENTO DE 2X PONTOS!
        </mj-text>
        <mj-text font-size="18px" color="#92400e" align="center">
          {{ event_start }} - {{ event_end }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Exclusivo para Membros de Fidelidade!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Olá {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Prepare-se para ganhar MUITO! Por um tempo limitado, você ganhará {{ points_multiplier }}X pontos em cada compra.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#dcfce7" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="24px" font-weight="bold" color="#047857" align="center">
              Ganhe {{ points_multiplier }}X Pontos
            </mj-text>
            <mj-text font-size="16px" color="#065f46" align="center">
              Em todas as compras<br/>
              {{ event_start }} - {{ event_end }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Exemplo de Ganhos:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="4px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Gaste $50 → Ganhe {{ example_points_normal }} pontos normalmente<br/>
              <strong style="color: #047857;">Durante este evento → Ganhe {{ example_points_bonus }} pontos! 🎉</strong>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="4px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Gaste $100 → Ganhe {{ example_points_normal_2 }} pontos normalmente<br/>
              <strong style="color: #047857;">Durante este evento → Ganhe {{ example_points_bonus_2 }} pontos! 🎉</strong>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Seu Saldo Atual:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>Pontos:</strong> {{ current_points }} pontos<br/>
          <strong>Nível:</strong> {{ loyalty_tier }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ shop_url }}" background-color="#dc2626" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Compre Agora & Ganhe {{ points_multiplier }}X Pontos
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="#dc2626" align="center" font-weight="bold">
          O evento termina {{ event_end }} - Não perca!
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🔥 EVENTO DE 2X PONTOS!
{{ event_start }} - {{ event_end }}

Exclusivo para Membros de Fidelidade!

Olá {{ customer_name }},

Prepare-se para ganhar MUITO! Por um tempo limitado, você ganhará {{ points_multiplier }}X pontos em cada compra.

GANHE {{ points_multiplier }}X PONTOS
Em todas as compras
{{ event_start }} - {{ event_end }}

EXEMPLO DE GANHOS:
- Gaste $50 → Ganhe {{ example_points_normal }} pontos normalmente
  Durante este evento → Ganhe {{ example_points_bonus }} pontos! 🎉

- Gaste $100 → Ganhe {{ example_points_normal_2 }} pontos normalmente
  Durante este evento → Ganhe {{ example_points_bonus_2 }} pontos! 🎉

SEU SALDO ATUAL:
- Pontos: {{ current_points }} pontos
- Nível: {{ loyalty_tier }}

Compre agora & ganhe {{ points_multiplier }}X pontos: {{ shop_url }}

O evento termina {{ event_end }} - Não perca!