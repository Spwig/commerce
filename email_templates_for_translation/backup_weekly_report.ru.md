---
template_type: backup_weekly_report
category: Backups
---

# Email Template: backup_weekly_report

## Subject
Еженедельная сводка резервных копий - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Еженедельная сводка резервных копий
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          {{ week_start }} - {{ week_end }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Статистика резервных копий:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Общее количество резервных копий:</strong> {{ total_backups }}<br/>
              <strong>Успешные:</strong> <span style="color: #059669;">{{ successful_backups }}</span><br/>
              <strong>Неудачные:</strong> <span style="color: #dc2626;">{{ failed_backups }}</span><br/>
              <strong>Средний размер:</strong> {{ average_size }}<br/>
              <strong>Общий объем используемого хранилища:</strong> {{ total_storage }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        {% if failed_backups > 0 %}
        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              ⚠️ Обнаружены проблемы:
            </mj-text>
            <mj-text color="#7f1d1d">
              {{ failed_backups }} резервных копий не удалось создать этой неделе. Пожалуйста, проверьте и предпримите исправляющие действия.
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="20px" />
        {% endif %}

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Последние резервные копии:
        </mj-text>

        {% for backup in recent_backups %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="4px" padding="12px" margin-bottom="8px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
              <strong>{{ backup.date }}</strong> - {{ backup.type }}
            </mj-text>
            <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              Размер: {{ backup.size }} | Продолжительность: {{ backup.duration }} |
              {% if backup.status == 'success' %}
              <span style="color: #059669;">✓ Успешно</span>
              {% else %}
              <span style="color: #dc2626;">✗ Неудачно</span>
              {% endif %}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          Просмотреть все резервные копии
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
ЕЖЕНЕДЕЛЬНАЯ СВОДКА РЕЗЕРВНЫХ КОПИЙ
{{ week_start }} - {{ week_end }}

СТАТИСТИКА РЕЗЕРВНЫХ КОПИЙ:
- Общее количество резервных копий: {{ total_backups }}
- Успешные: {{ successful_backups }}
- Неудачные: {{ failed_backups }}
- Средний размер: {{ average_size }}
- Общий объем используемого хранилища: {{ total_storage }}

{% if failed_backups > 0 %}
⚠️ ОБНАРУЖЕНЫ ПРОБЛЕМЫ:
{{ failed_backups }} резервных копий не удалось создать этой неделе. Пожалуйста, проверьте и предпримите исправляющие действия.
{% endif %}

ПОСЛЕДНИЕ РЕЗЕРВНЫЕ КОПИИ:
{% for backup in recent_backups %}
- {{ backup.date }} - {{ backup.type }}
  Размер: {{ backup.size }} | Продолжительность: {{ backup.duration }} | Статус: {{ backup.status }}
{% endfor %}

Просмотреть все резервные копии: {{ admin_backup_url }}