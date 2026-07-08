---
template_type: system_health_warning
category: System Health
---

# Email Template: system_health_warning

## Subject
⚠️ Предупреждение о состоянии системы: {{ metric_name }} - {{ current_value }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Предупреждение о состоянии системы
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Превышено пороговое значение предупреждения
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          На вашем установке Spwig метрика состояния системы превысила пороговое значение предупреждения.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Детали предупреждения:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Метрика:</strong> {{ metric_name }}<br/>
              <strong>Текущее значение:</strong> <span style="color: #d97706; font-weight: bold;">{{ current_value }}</span><br/>
              <strong>Пороговое значение предупреждения:</strong> {{ warning_threshold }}<br/>
              <strong>Пороговое значение критического уровня:</strong> {{ critical_threshold }}<br/>
              <strong>Обнаружено:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Потенциальное влияние:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ impact_description }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Рекомендуемые действия:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ recommended_actions }}
        </mj-text>

        {% if trend_data %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Анализ тренда:
        </mj-text>
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              {{ trend_data }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              💡 Требуется действие: Хотя это не критично, устранение этого предупреждения сейчас может предотвратить проблемы с обслуживанием в будущем.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Посмотреть системную панель управления
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ metrics_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Посмотреть подробные метрики
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ ПРЕДУПРЕЖДЕНИЕ О СОСТОЯНИИ СИСТЕМЫ

Превышено пороговое значение предупреждения

На вашем установке Spwig метрика состояния системы превысила пороговое значение предупреждения.

ДЕТАЛИ ПРЕДУПРЕЖДЕНИЯ:
- Метрика: {{ metric_name }}
- Текущее значение: {{ current_value }}
- Пороговое значение предупреждения: {{ warning_threshold }}
- Пороговое значение критического уровня: {{ critical_threshold }}
- Обнаружено: {{ detected_at }}

ПОТЕНЦИАЛЬНОЕ ВЛИЯНИЕ:
{{ impact_description }}

РЕКОМЕНДУЕМЫЕ ДЕЙСТВИЯ:
{{ recommended_actions }}

{% if trend_data %}
АНАЛИЗ ТРЕНДА:
{{ trend_data }}
{% endif %}

💡 ТРЕБУЕТСЯ ДЕЙСТВИЕ: Хотя это не критично, устранение этого предупреждения сейчас может предотвратить проблемы с обслуживанием в будущем.

Посмотреть системную панель управления: {{ dashboard_url }}
Посмотреть подробные метрики: {{ metrics_url }}