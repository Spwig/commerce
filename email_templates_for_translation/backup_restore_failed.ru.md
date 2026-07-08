---
template_type: backup_restore_failed
category: Backups
---

# Email Template: backup_restore_failed

## Subject
🚨 КРИТИЧЕСКИЙ: Восстановление резервной копии не удалось - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef2f2">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#dc2626" align="center">
          🚨 КРИТИЧЕСКИЙ: Восстановление резервной копии не удалось
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#1f2937' }}" font-weight="bold">
          Здравствуйте, {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Критическая операция восстановления резервной копии завершилась неудачно. Ваш магазин может находиться в несогласованном состоянии и требует немедленного внимания.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              Детали восстановления:
            </mj-text>
            <mj-text color="#7f1d1d">
              <strong>Файл резервной копии:</strong> {{ backup_filename }}<br/>
              <strong>Начало:</strong> {{ restore_started_at }}<br/>
              <strong>Не удалось:</strong> {{ restore_failed_at }}<br/>
              <strong>Продолжительность:</strong> {{ restore_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Детали ошибки:
        </mj-text>

        <mj-section background-color="#f9fafb" border-radius="4px" padding="15px">
          <mj-column>
            <mj-text font-family="'Courier New', monospace" font-size="13px" color="#dc2626">
              {{ error_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#92400e">
              🚨 ТРЕБУЕТСЯ СРОЧНОЕ ДЕЙСТВИЕ:
            </mj-text>
            <mj-text color="#92400e">
              1. <strong>НЕ</strong> вносите никаких изменений в магазин<br/>
              2. Проверьте соединение и целостность базы данных<br/>
              3. Изучите журналы ошибок для получения подробного трассировки стека<br/>
              4. Свяжитесь с технической поддержкой немедленно<br/>
              5. Рассмотрите возможность отката до последнего известного хорошего состояния
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Просмотреть журналы восстановления
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ support_url }}" background-color="#92400e" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          Свяжитесь с экстренной техподдержкой
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 КРИТИЧЕСКИЙ: ВОССТАНОВЛЕНИЕ РЕЗЕРВНОЙ КОПИИ ПРОВАЛОСЬ

Здравствуйте, {{ admin_name }},

Критическая операция восстановления резервной копии завершилась неудачно. Ваш магазин может находиться в несогласованном состоянии и требует немедленного внимания.

Детали восстановления:
- Файл резервной копии: {{ backup_filename }}
- Начало: {{ restore_started_at }}
- Не удалось: {{ restore_failed_at }}
- Продолжительность: {{ restore_duration }}

Детали ошибки:
{{ error_message }}

🚨 ТРЕБУЕТСЯ СРОЧНОЕ ДЕЙСТВИЕ:
1. НЕ вносите никаких изменений в магазин
2. Проверьте соединение и целостность базы данных
3. Изучите журналы ошибок для получения подробного трассировки стека
4. Свяжитесь с технической поддержкой немедленно
5. Рассмотрите возможность отката до последнего известного хорошего состояния

Просмотреть журналы восстановления: {{ admin_backup_url }}
Свяжитесь с экстренной техподдержкой: {{ support_url }}