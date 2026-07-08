---
template_type: backup_completed
category: Backups
---

# Email Template: backup_completed

## Subject
✓ Резервная копия завершена успешно - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#f0fdf4">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#059669" align="center">
          ✓ Резервная копия завершена успешно
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Здравствуйте, {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Ваш запланированный резервный копии для {{ shop_name }} успешно завершен.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Детали резервной копии:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Тип:</strong> {{ backup_type }}<br/>
              <strong>Начало:</strong> {{ backup_started_at }}<br/>
              <strong>Завершено:</strong> {{ backup_completed_at }}<br/>
              <strong>Продолжительность:</strong> {{ backup_duration }}<br/>
              <strong>Размер:</strong> {{ backup_size }}<br/>
              <strong>Местоположение:</strong> {{ backup_location }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          Просмотреть детали резервной копии
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>Следующая запланированная резервная копия:</strong> {{ next_scheduled_backup }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ РЕЗЕРВНАЯ КОПИЯ ЗАВЕРШЕНА УСПЕШНО

Здравствуйте, {{ admin_name }},

Ваш запланированный резервный копии для {{ shop_name }} успешно завершен.

ДЕТАЛИ РЕЗЕРВНОЙ КОПИИ:
- Тип: {{ backup_type }}
- Начало: {{ backup_started_at }}
- Завершено: {{ backup_completed_at }}
- Продолжительность: {{ backup_duration }}
- Размер: {{ backup_size }}
- Местоположение: {{ backup_location }}

Просмотреть детали резервной копии: {{ admin_backup_url }}

Следующая запланированная резервная копия: {{ next_scheduled_backup }}