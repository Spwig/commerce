---
template_type: backup_restore_completed
category: Backups
---

# Email Template: backup_restore_completed

## Subject
✓ Восстановление резервной копии завершено - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#f0fdf4">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#059669" align="center">
          ✓ Восстановление резервной копии завершено
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Здравствуйте, {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Восстановление резервной копии завершено успешно. Данные вашего магазина были восстановлены.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Детали восстановления:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Backup File:</strong> {{ backup_filename }}<br/>
              <strong>Backup Date:</strong> {{ backup_date }}<br/>
              <strong>Started:</strong> {{ restore_started_at }}<br/>
              <strong>Completed:</strong> {{ restore_completed_at }}<br/>
              <strong>Duration:</strong> {{ restore_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ Важные следующие шаги:
            </mj-text>
            <mj-text font-size="14px" color="#92400e">
              1. Проверьте, работает ли ваш магазин корректно<br/>
              2. Проверьте ключевые данные (товары, заказы, клиенты)<br/>
              3. Очистите кэш при необходимости<br/>
              4. Проверьте критические рабочие процессы (оплата, доступ к админ-панели)
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Перейти на панель администратора
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ ВОССТАНОВЛЕНИЕ РЕЗЕРВНОЙ КОПИИ ЗАВЕРШЕНО

Здравствуйте, {{ admin_name }},

Восстановление резервной копии завершено успешно. Данные вашего магазина были восстановлены.

ДЕТАЛИ ВОССТАНОВЛЕНИЯ:
- Файл резервной копии: {{ backup_filename }}
- Дата резервной копии: {{ backup_date }}
- Начато: {{ restore_started_at }}
- Завершено: {{ restore_completed_at }}
- Продолжительность: {{ restore_duration }}

⚠️ ВАЖНЫЕ СЛЕДУЮЩИЕ ШАГИ:
1. Проверьте, работает ли ваш магазин корректно
2. Проверьте ключевые данные (товары, заказы, клиенты)
3. Очистите кэш при необходимости
4. Проверьте критические рабочие процессы (оплата, доступ к админ-панели)

Перейти на панель администратора: {{ admin_dashboard_url }}