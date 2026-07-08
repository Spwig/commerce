---
template_type: subscription_dunning_final_notice
category: Subscriptions
---

# Email Template: subscription_dunning_final_notice

## Subject
⚠️ ОКОНЧАТЕЛЬНОЕ ПРЕДУПРЕЖДЕНИЕ: Ваша подписка будет отменена через {{ days_until_cancellation }} дней

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#991b1b" align="center">
          ⚠️ ОКОНЧАТЕЛЬНОЕ ПРЕДУПРЕЖДЕНИЕ
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Имминентная отмена подписки
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Здравствуйте, {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Это ваше окончательное предупреждение. Мы не смогли обработать платеж по вашей подписке {{ plan_name }}. Если мы не получим оплату в течение {{ days_until_cancellation }} дней, ваша подписка будет отменена.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b" font-size="16px">
              ⚠️ Оплата не удалась - необходимы действия
            </mj-text>
            <mj-text color="#991b1b">
              <strong>Подписка:</strong> {{ plan_name }}<br/>
              <strong>Сумма к оплате:</strong> {{ amount_due }}<br/>
              <strong>Неудачных попыток:</strong> {{ retry_count }}<br/>
              <strong>Последняя попытка:</strong> {{ last_retry_date }}<br/>
              <strong>Дата отмены:</strong> <span style="font-weight: bold; font-size: 16px;">{{ cancellation_date }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Ошибка оплаты:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" font-family="monospace" color="{{ theme.color.text|default:'#4b5563' }}">
              {{ payment_error_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Что произойдёт:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          Если оплата не будет получена к {{ cancellation_date }}:<br/>
          • Ваша подписка будет отменена<br/>
          • Вы потеряете доступ ко всем преимуществам подписки<br/>
          • Ваши данные могут быть удалены (см. политику хранения)<br/>
          • Вам нужно будет повторно подписаться, чтобы восстановить доступ
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Обновите способ оплаты сейчас
        </mj-text>

        <mj-spacer height="20px" />

        <mj-button href="{{ update_payment_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Обновить способ оплаты
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Распространённые проблемы и решения:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • <strong>Истёкший срок действия карты:</strong> Обновите картой с действительным сроком действия<br/>
          • <strong>Недостаточно средств:</strong> Убедитесь, что баланс достаточен<br/>
          • <strong>Карта отклонена:</strong> Свяжитесь с банком или используйте другую карту<br/>
          • <strong>Не совпадающий адрес:</strong> Проверьте, чтобы адрес, указанный при оплате, совпадал с адресом карты
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" font-weight="bold">
              Нужна помощь?
            </mj-text>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              Если у вас возникли проблемы с оплатой или вам нужна помощь, пожалуйста, немедленно свяжитесь с нашей службой поддержки.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Свяжитесь с поддержкой
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Если вы хотите отменить подписку, вы можете сделать это в настройках вашего аккаунта.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ ОКОНЧАТЕЛЬНОЕ ПРЕДУПРЕЖДЕНИЕ

Имминентная отмена подписки

Здравствуйте, {{ customer_name }},

Это ваше окончательное предупреждение. Мы не смогли обработать платеж по вашей подписке {{ plan_name }}. Если мы не получим оплату в течение {{ days_until_cancellation }} дней, ваша подписка будет отменена.

⚠️ ОПЛАТА НЕ УДАЛСЯ - ТРЕБУЮТСЯ ДЕЙСТВИЯ:
- Подписка: {{ plan_name }}
- Сумма к оплате: {{ amount_due }}
- Неудачных попыток: {{ retry_count }}
- Последняя попытка: {{ last_retry_date }}
- Дата отмены: {{ cancellation_date }}

ОШИБКА ОПЛАТЫ:
{{ payment_error_message }}

ЧТО ПРОИЗОЙДЕТ:
Если оплата не будет получена к {{ cancellation_date }}:
• Ваша подписка будет отменена
• Вы потеряете доступ ко всем преимуществам подписки
• Ваши данные могут быть удалены (см. политику хранения)
• Вам нужно будет повторно подписаться, чтобы восстановить доступ

ОБНОВИТЕ СПОСОБ ОПЛАТЫ ТЕПЕРЬ

Распространённые проблемы и решения:
• Истёкший срок действия карты: Обновите картой с действительным сроком действия
• Недостаточно средств: Убедитесь, что баланс достаточен
• Карта отклонена: Свяжитесь с банком или используйте другую карту
• Не совпадающий адрес: Проверьте, чтобы адрес, указанный при оплате, совпадал с адресом карты

НЕОБХОДИМА ПОМОЩЬ?
Если у вас возникли проблемы с оплатой или вам нужна помощь, пожалуйста, немедленно свяжитесь с нашей службой поддержки.

Обновите способ оплаты: {{ update_payment_url }}
Свяжитесь с поддержкой: {{ support_url }}

Если вы хотите отменить подписку, вы можете сделать это в настройках вашего аккаунта.