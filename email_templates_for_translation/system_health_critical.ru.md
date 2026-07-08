---
template_type: system_health_critical
category: System Health
---

# Email Template: system_health_critical

## Subject
🚨 КРИТИЧЕСКОЕ ПРЕДУПРЕЖДЕНИЕ: {{ metric_name }} - {{ current_value }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#991b1b" align="center">
          🚨 КРИТИЧЕСКОЕ ПРЕДУПРЕЖДЕНИЕ СИСТЕМЫ
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Требуется немедленное внимание
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Обнаружена критическая проблема с состоянием системы на вашем установке Spwig.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b" font-size="16px">
              🚨 Критическая проблема
            </mj-text>
            <mj-text color="#991b1b">
              <strong>Метрика:</strong> {{ metric_name }}<br/>
              <strong>Текущее значение:</strong> <span style="font-size: 18px; font-weight: bold;">{{ current_value }}</span><br/>
              <strong>Критический порог:</strong> {{ critical_threshold }}<br/>
              <strong>Обнаружено:</strong> {{ detected_at }}<br/>
              <strong>Серьезность:</strong> КРИТИЧЕСКИЙ
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Влияние:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ impact_description }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Требуются немедленные действия:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ recommended_actions }}
        </mj-text>

        {% if trend_data %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Тренд:
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

        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ Предупреждение о снижении производительности
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              Эта проблема может вызвать прерывания в работе или снижение производительности. Срочно решите проблему, чтобы избежать влияния на клиентов.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ dashboard_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Просмотреть системную панель
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ logs_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Просмотреть системные журналы
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 КРИТИЧЕСКОЕ ПРЕДУПРЕЖДЕНИЕ СИСТЕМЫ

Требуется немедленное внимание

Обнаружена критическая проблема с состоянием системы на вашем установке Spwig.

🚨 КРИТИЧЕСКАЯ ПРОБЛЕМА:
- Метрика: {{ metric_name }}
- Текущее значение: {{ current_value }}
- Критический порог: {{ critical_threshold }}
- Обнаружено: {{ detected_at }}
- Серьезность: КРИТИЧЕСКИЙ

ВЛИЯНИЕ:
{{ impact_description }}

ТРЕБУЮТСЯ НЕМЕДЛЕННЫЕ ДЕЙСТВИЯ:
{{ recommended_actions }}

{% if trend_data %}
ТРЕНД:
{{ trend_data }}
{% endif %}

⚠️ ПРЕДУПРЕЖДЕНИЕ О СНИЖЕНИИ ПРОИЗВОДИТЕЛЬНОСТИ:
Эта проблема может вызвать прерывания в работе или снижение производительности. Срочно решите проблему, чтобы избежать влияния на клиентов.

Просмотреть системную панель: {{ dashboard_url }}
Просмотреть системные журналы: {{ logs_url }}
