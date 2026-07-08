---
template_type: loyalty_double_points_event
category: Loyalty Program
---

# Email Template: loyalty_double_points_event

## Subject
🔥 Событие удвоения баллов начинается прямо сейчас! - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#92400e" align="center">
          🔥 Событие удвоения баллов!
        </mj-text>
        <mj-text font-size="18px" color="#92400e" align="center">
          {{ event_start }} - {{ event_end }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Исключительно для членов программы лояльности!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Здравствуйте, {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Готовьтесь получать много баллов! В течение ограниченного времени вы будете получать {{ points_multiplier }}X баллов за каждую покупку.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#dcfce7" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="24px" font-weight="bold" color="#047857" align="center">
              Получите {{ points_multiplier }}X баллов
            </mj-text>
            <mj-text font-size="16px" color="#065f46" align="center">
              На всех покупках<br/>
              {{ event_start }} - {{ event_end }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Пример заработка:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="4px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Потратите $50 → Получите {{ example_points_normal }} баллов в обычном режиме<br/>
              <strong style="color: #047857;">Во время этого события → Получите {{ example_points_bonus }} баллов! 🎉</strong>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="4px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Потратите $100 → Получите {{ example_points_normal_2 }} баллов в обычном режиме<br/>
              <strong style="color: #047857;">Во время этого события → Получите {{ example_points_bonus_2 }} баллов! 🎉</strong>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Ваш текущий баланс:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>Баллы:</strong> {{ current_points }} баллов<br/>
          <strong>Уровень:</strong> {{ loyalty_tier }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ shop_url }}" background-color="#dc2626" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Покупайте сейчас и получайте {{ points_multiplier }}X баллов
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="#dc2626" align="center" font-weight="bold">
          Событие заканчивается {{ event_end }} - Не упустите!
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🔥 Событие удвоения баллов!
{{ event_start }} - {{ event_end }}

Исключительно для членов программы лояльности!

Здравствуйте, {{ customer_name }},

Готовьтесь получать много баллов! В течение ограниченного времени вы будете получать {{ points_multiplier }}X баллов за каждую покупку.

ПОЛУЧИТЕ {{ points_multiplier }}X БАЛЛОВ
На всех покупках
{{ event_start }} - {{ event_end }}

ПРИМЕР ЗАРАБОТКА:
- Потратите $50 → Получите {{ example_points_normal }} баллов в обычном режиме
  Во время этого события → Получите {{ example_points_bonus }} баллов! 🎉

- Потратите $100 → Получите {{ example_points_normal_2 }} баллов в обычном режиме
  Во время этого события → Получите {{ example_points_bonus_2 }} баллов! 🎉

ВАШ ТЕКУЩИЙ БАЛАНС:
- Баллы: {{ current_points }} баллов
- Уровень: {{ loyalty_tier }}

Покупайте сейчас и получайте {{ points_multiplier }}X баллов: {{ shop_url }}

Событие заканчивается {{ event_end }} - Не упустите!