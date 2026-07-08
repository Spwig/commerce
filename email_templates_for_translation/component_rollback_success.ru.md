---
template_type: component_rollback_success
category: Component Updates
---

# Email Template: component_rollback_success

## Subject
✓ {{ component_name }} откатили до v{{ previous_version }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dbeafe">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          ↩️ Откат завершён
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Восстановленный компонент
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ component_name }} успешно откатили до предыдущей версии.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Детали отката:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Компонент:</strong> {{ component_name }}<br/>
              <strong>Откат от:</strong> v{{ failed_version }}<br/>
              <strong>Восстановлен до:</strong> v{{ previous_version }}<br/>
              <strong>Завершён:</strong> {{ completed_at }}<br/>
              <strong>Длительность:</strong> {{ rollback_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if rollback_reason %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Причина отката:
        </mj-text>
        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ rollback_reason }}
        </mj-text>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" font-weight="bold">
              ✓ Состояние магазина
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              Ваш магазин теперь работает на стабильной версии {{ previous_version }}. Все функции должны быть восстановлены.
            </mj-text>
          </mj-column>
        </mj-section>

        {% if data_restored %}
        <mj-spacer height="20px" />
        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>Восстановление данных:</strong> {{ data_restoration_message }}
        </mj-text>
        {% endif %}

        {% if next_steps %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Следующие шаги:
        </mj-text>
        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ next_steps }}
        </mj-text>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ component_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Просмотреть детали компонента
        </mj-button>

        {% if incident_report_url %}
        <mj-spacer height="10px" />
        <mj-button href="{{ incident_report_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Просмотреть отчёт об инциденте
        </mj-button>
        {% endif %}

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Если вы продолжите испытывать проблемы, пожалуйста, свяжитесь с поддержкой.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
↩️ ОТКАТ ЗАВЕРШЁН

Восстановленный компонент

{{ component_name }} успешно откатили до предыдущей версии.

ДЕТАЛИ ОТКАТА:
- Компонент: {{ component_name }}
- Откат от: v{{ failed_version }}
- Восстановлен до: v{{ previous_version }}
- Завершён: {{ completed_at }}
- Длительность: {{ rollback_duration }}

{% if rollback_reason %}
ПРИЧИНА ОТКАТА:
{{ rollback_reason }}
{% endif %}

✓ СОСТОЯНИЕ МАГАЗИНА:
Ваш магазин теперь работает на стабильной версии {{ previous_version }}. Все функции должны быть восстановлены.

{% if data_restored %}
ВОССТАНОВЛЕНИЕ ДАННЫХ: {{ data_restoration_message }}
{% endif %}

{% if next_steps %}
СЛЕДУЮЩИЕ ШАГИ:
{{ next_steps }}
{% endif %}

Просмотреть детали компонента: {{ component_url }}
{% if incident_report_url %}Просмотреть отчёт об инциденте: {{ incident_report_url }}{% endif %}

Если вы продолжите испытывать проблемы, пожалуйста, свяжитесь с поддержкой.