---
template_type: affiliate_payout_threshold_reached
category: Affiliate Program
---

# Email Template: affiliate_payout_threshold_reached

## Subject
💰 Вы достигли минимального порога выплаты!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          💰 Порог выплаты достигнут!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Отличная новость!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Здравствуйте, {{ affiliate_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Поздравляем! Ваша баланс партнера достиг минимального порога выплаты. Теперь вы можете запросить выплату.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Ваш баланс:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Доступный баланс:</strong> <span style="font-size: 24px; font-weight: bold; color: #059669;">{{ available_balance }}</span><br/>
              <strong>Минимальная выплата:</strong> {{ minimum_payout }}<br/>
              <strong>Ожидающие комиссии:</strong> {{ pending_balance }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Что делать дальше:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Запросить выплату через панель управления партнера<br/>
          • Выплаты обрабатываются {{ payout_schedule }}<br/>
          • Средства будут отправлены через {{ payment_method }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ request_payout_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Запросить выплату
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ portal_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Посмотреть панель управления
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
💰 ПОРТАЛ ВЫПЛАТЫ ДОСТИГНУТ!

Отличная новость!

Здравствуйте, {{ affiliate_name }},

Поздравляем! Ваш баланс партнера достиг минимального порога выплаты. Теперь вы можете запросить выплату.

ВАШ БАЛАНС:
- Доступный баланс: {{ available_balance }}
- Минимальная выплата: {{ minimum_payout }}
- Ожидающие комиссии: {{ pending_balance }}

ЧТО СЛЕДУЕТ СДЕЛАТЬ:
• Запросить выплату через панель управления партнера
• Выплаты обрабатываются {{ payout_schedule }}
• Средства будут отправлены через {{ payment_method }}

Запросить выплату: {{ request_payout_url }}
Посмотреть панель управления: {{ portal_url }}