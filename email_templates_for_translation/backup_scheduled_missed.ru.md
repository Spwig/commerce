---
template_type: backup_scheduled_missed
category: Backups
---

# Email Template: backup_scheduled_missed

## Subject
⚠️ Запланированная резервная копия не выполнена - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Запланированная резервная копия не выполнена
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Здравствуйте, {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Запланированная резервная копия для {{ shop_name }} не запустилась в ожидаемое время. Ваши данные могут не быть полностью защищены.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Детали расписания резервной копии:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Время выполнения:</strong> {{ scheduled_time }}<br/>
              <strong>Тип резервной копии:</strong> {{ backup_type }}<br/>
              <strong>Последняя успешная резервная копия:</strong> {{ last_successful_backup }}<br/>
              <strong>Время с момента последней резервной копии:</strong> {{ time_since_last }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Возможные причины:
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          • Сервер был недоступен или отключён<br/>
          • Услуга запланированных задач не запущена<br/>
          • Недостаточно разрешений<br/>
          • Недостаточно места на диске<br/>
          • Проблемы с подключением к базе данных
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Выполнить резервную копию вручную
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ admin_logs_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Просмотреть системные журналы
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ ЗАПЛАНИРОВАННАЯ РЕЗЕРВНАЯ КОПИЯ НЕ ВЫПОЛНЕНА

Здравствуйте, {{ admin_name }},

Запланированная резервная копия для {{ shop_name }} не запустилась в ожидаемое время. Ваши данные могут не быть полностью защищены.

Детали расписания резервной копии:
- Время выполнения: {{ scheduled_time }}
- Тип резервной копии: {{ backup_type }}
- Последняя успешная резервная копия: {{ last_successful_backup }}
- Время с момента последней резервной копии: {{ time_since_last }}

Возможные причины:
• Сервер был недоступен или отключён
• Услуга запланированных задач не запущена
• Недостаточно разрешений
• Недостаточно места на диске
• Проблемы с подключением к базе данных

Выполнить резервную копию вручную: {{ admin_backup_url }}
Просмотреть системные журналы: {{ admin_logs_url }}