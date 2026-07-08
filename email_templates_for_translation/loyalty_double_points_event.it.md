---
template_type: loyalty_double_points_event
category: Loyalty Program
---

# Email Template: loyalty_double_points_event

## Subject
🔥 Evento di Doppio Punti iniziato! - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#92400e" align="center">
          🔥 2X PUNTI EVENTO!
        </mj-text>
        <mj-text font-size="18px" color="#92400e" align="center">
          {{ event_start }} - {{ event_end }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Esclusivo per i Membri della Fedeltà!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Ciao {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Preparati a guadagnare BIG! Per un periodo limitato, guadagnerai {{ points_multiplier }}X punti su ogni acquisto.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#dcfce7" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="24px" font-weight="bold" color="#047857" align="center">
              Guadagna {{ points_multiplier }}X Punti
            </mj-text>
            <mj-text font-size="16px" color="#065f46" align="center">
              Su tutti gli acquisti<br/>
              {{ event_start }} - {{ event_end }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Esempio di Guadagni:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="4px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Spendere $50 → Guadagna {{ example_points_normal }} punti normalmente<br/>
              <strong style="color: #047857;">Durante questo evento → Guadagna {{ example_points_bonus }} punti! 🎉</strong>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="4px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Spendere $100 → Guadagna {{ example_points_normal_2 }} punti normalmente<br/>
              <strong style="color: #047857;">Durante questo evento → Guadagna {{ example_points_bonus_2 }} punti! 🎉</strong>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Il tuo saldo attuale:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>Punti:</strong> {{ current_points }} punti<br/>
          <strong>Livello:</strong> {{ loyalty_tier }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ shop_url }}" background-color="#dc2626" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Acquista Ora & Guadagna {{ points_multiplier }}X Punti
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="#dc2626" align="center" font-weight="bold">
          L'evento termina {{ event_end }} - Non mancare!
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🔥 2X PUNTI EVENTO!
{{ event_start }} - {{ event_end }}

Esclusivo per i Membri della Fedeltà!

Ciao {{ customer_name }},

Preparati a guadagnare BIG! Per un periodo limitato, guadagnerai {{ points_multiplier }}X punti su ogni acquisto.

GUADAGNA {{ points_multiplier }}X PUNTI
Su tutti gli acquisti
{{ event_start }} - {{ event_end }}

ESEMPI DI GUADAGNI:
- Spendere $50 → Guadagna {{ example_points_normal }} punti normalmente
  Durante questo evento → Guadagna {{ example_points_bonus }} punti! 🎉

- Spendere $100 → Guadagna {{ example_points_normal_2 }} punti normalmente
  Durante questo evento → Guadagna {{ example_points_bonus_2 }} punti! 🎉

IL TUO SALDO ATTUALE:
- Punti: {{ current_points }} punti
- Livello: {{ loyalty_tier }}

Acquista ora & guadagna {{ points_multiplier }}X punti: {{ shop_url }}

L'evento termina {{ event_end }} - Non mancare!