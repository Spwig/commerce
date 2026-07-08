---
template_type: system_health_recovered
category: System Health
---

# Email Template: system_health_recovered

## Subject
✓ Решено: {{ metric_name }} вернулся к норме

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          ✓ Проблема решена
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Восстановление состояния системы
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Хорошая новость! Проблема с состоянием системы {{ metric_name }} решена.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Детали восстановления:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Метрика:</strong> {{ metric_name }}<br/>
              <strong>Текущее значение:</strong> <span style="color: #059669; font-weight: bold;">{{ current_value }}</span><br/>
              <strong>Нормальный порог:</strong> {{ normal_threshold }}<br/>
              <strong>Обнаружено проблема:</strong> {{ issue_detected_at }}<br/>
              <strong>Восстановлено:</strong> {{ recovered_at }}<br/>
              <strong>Продолжительность:</strong> {{ issue_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#065f46" font-weight="bold">
              ✓ Состояние системы: Нормальное
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              {{ metric_name }} вернулся к нормальным уровням и работает в пределах допустимых параметров.
            </mj-text>
          </mj-column>
        </mj-section>

        {% if resolution_summary %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Сводка решения:
        </mj-text>
        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ resolution_summary }}
        </mj-text>
        {% endif %}

        {% if actions_taken %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Принятые действия:
        </mj-text>
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.6">
              {{ actions_taken }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        {% if preventive_measures %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Профилактические меры:
        </mj-text>
        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              {{ preventive_measures }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Посмотреть системную панель
        </mj-button>

        {% if incident_report_url %}
        <mj-spacer height="10px" />
        <mj-button href="{{ incident_report_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Посмотреть отчет об инциденте
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ ПРОБЛЕМА РЕШЕНА

Восстановление состояния системы

Хорошая новость! Проблема с состоянием системы {{ metric_name }} решена.

ДЕТАЛИ ВОССТАНОВЛЕНИЯ:
- Метрика: {{ metric_name }}
- Текущее значение: {{ current_value }}
- Нормальный порог: {{ normal_threshold }}
- Обнаружено проблема: {{ issue_detected_at }}
- Восстановлено: {{ recovered_at }}
- Продолжительность: {{ issue_duration }}

✓ СОСТОЯНИЕ СИСТЕМЫ: НОРМАЛЬНОЕ
{{ metric_name }} вернулся к нормальным уровням и работает в пределах допустимых параметров.

{% if resolution_summary %}
СВОДКА РЕШЕНИЯ:
{{ resolution_summary }}
{% endif %}

{% if actions_taken %}
ПРИНЯТЫЕ ДЕЙСТВИЯ:
{{ actions_taken }}
{% endif %}

{% if preventive_measures %}
ПРОФИЛАКТИЧЕСКИЕ МЕРЫ:
{{ preventive_measures }}
{% endif %}

Посмотреть системную панель: {{ dashboard_url }}
{% if incident_report_url %}Посмотреть отчет об инциденте: {{ incident_report_url }}{% endif %}