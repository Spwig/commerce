---
template_type: component_incompatible_warning
category: Component Updates
---

# Email Template: component_incompatible_warning

## Subject
⚠️ Проблема совместимости: {{ component_name }} и {{ conflicting_component }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Предупреждение о совместимости
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Обнаружено конфликтующее сочетание версий
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Обнаружен конфликт между компонентами в вашем магазине Spwig.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Детали конфликта:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Компонент 1:</strong> {{ component_name }} v{{ component_version }}<br/>
              <strong>Компонент 2:</strong> {{ conflicting_component }} v{{ conflicting_version }}<br/>
              <strong>Обнаружено:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Проблема совместимости:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ incompatibility_description }}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#991b1b" font-weight="bold">
              Потенциальное влияние
            </mj-text>
            <mj-text font-size="14px" color="#991b1b" line-height="1.6">
              {{ impact_description }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Рекомендуемое действие:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ recommended_action }}
        </mj-text>

        {% if compatible_versions %}
        <mj-spacer height="30px" />
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" font-weight="bold">
              Совместимые версии
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              {{ compatible_versions }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        {% if update_url %}
        <mj-button href="{{ update_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Решить конфликт
        </mj-button>
        <mj-spacer height="10px" />
        {% endif %}

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Обратиться в поддержку
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Ваш магазин всё ещё работает, но мы рекомендуем как можно скорее решить этот конфликт.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ ПРЕДУПРЕЖДЕНИЕ О СОВМЕСТИМОСТИ

Обнаружено конфликтующее сочетание версий

Обнаружен конфликт между компонентами в вашем магазине Spwig.

ДЕТАЛИ КОНФЛИКТА:
- Компонент 1: {{ component_name }} v{{ component_version }}
- Компонент 2: {{ conflicting_component }} v{{ conflicting_version }}
- Обнаружено: {{ detected_at }}

ПРОБЛЕМА СОВМЕСТИМОСТИ:
{{ incompatibility_description }}

ПОТЕНЦИАЛЬНОЕ ВЛИЯНИЕ:
{{ impact_description }}

РЕКОМЕНДУЕМОЕ ДЕЙСТВИЕ:
{{ recommended_action }}

{% if compatible_versions %}СОВМЕСТИМЫЕ ВЕРСИИ:
{{ compatible_versions }}
{% endif %}

{% if update_url %}Решить конфликт: {{ update_url }}{% endif %}
Обратиться в поддержку: {{ support_url }}

Ваш магазин всё ещё работает, но мы рекомендуем как можно скорее решить этот конфликт.