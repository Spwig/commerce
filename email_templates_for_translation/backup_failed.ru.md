---
template_type: backup_failed
category: Backups
---

# Email Template: backup_failed

## Subject
🚨 СРОЧНО: Резервное копирование не удалось - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef2f2">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#dc2626" align="center">
          ⚠️ Резервное копирование не удалось
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#1f2937' }}">
          Здравствуйте {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Критическая операция резервного копирования завершилась неудачно для вашего магазина {{ shop_name }}. Требуется немедленное вмешательство для обеспечения защиты данных.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              Детали резервного копирования:
            </mj-text>
            <mj-text color="#7f1d1d">
              <strong>Тип резервного копирования:</strong> {{ backup_type }}<br/>
              <strong>Начало:</strong> {{ backup_started_at }}<br/>
              <strong>Неудача:</strong> {{ backup_failed_at }}<br/>
              <strong>Длительность:</strong> {{ backup_duration }}
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

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Рекомендуемые действия:
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          1. Проверьте доступное место на диске вашего сервера<br/>
          2. Проверьте подключение к базе данных<br/>
          3. Изучите журнал ошибок для получения подробного трассировки стека<br/>
          4. Повторно выполните резервное копирование вручную или дождитесь следующего запланированного запуска<br/>
          5. Обратитесь в службу поддержки, если проблема сохраняется
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Просмотреть журналы резервного копирования
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ retry_backup_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          Повторить резервное копирование сейчас
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>Последняя успешная резервная копия:</strong> {{ last_successful_backup }}<br/>
          <strong>Следующая запланированная резервная копия:</strong> {{ next_scheduled_backup }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 СРОЧНО: РЕЗЕРВНОЕ КОПИРОВАНИЕ НЕ УДАЛОСЬ

Здравствуйте {{ admin_name }},

Критическая операция резервного копирования завершилась неудачно для вашего магазина {{ shop_name }}. Требуется немедленное вмешательство для обеспечения защиты данных.

ДЕТАЛИ РЕЗЕРВНОГО КОПИРОВАНИЯ:
- Тип резервного копирования: {{ backup_type }}
- Начало: {{ backup_started_at }}
- Неудача: {{ backup_failed_at }}
- Длительность: {{ backup_duration }}

ДЕТАЛИ ОШИБКИ:
{{ error_message }}

РЕКОМЕНДУЕМЫЕ ДЕЙСТВИЯ:
1. Проверьте доступное место на диске вашего сервера
2. Проверьте подключение к базе данных
3. Изучите журнал ошибок для получения подробного трассировки стека
4. Повторно выполните резервное копирование вручную или дождитесь следующего запланированного запуска
5. Обратитесь в службу поддержки, если проблема сохраняется

Просмотреть журналы резервного копирования: {{ admin_backup_url }}
Повторить резервное копирование сейчас: {{ retry_backup_url }}

Последняя успешная резервная копия: {{ last_successful_backup }}
Следующая запланированная резервная копия: {{ next_scheduled_backup }}

---
Это критическое системное уведомление для администраторов {{ shop_name }}.