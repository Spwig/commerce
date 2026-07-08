---
template_type: component_security_update
category: Component Updates
---

# Email Template: component_security_update

## Subject
🔒 СРОЧНО: Доступно обновление безопасности для {{ component_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#991b1b" align="center">
          🔒 Требуется обновление безопасности
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Критальное обновление безопасности
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Обнаружена уязвимость безопасности в {{ component_name }}. Пожалуйста, немедленно обновитесь, чтобы защитить свой магазин.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b" font-size="16px">
              ⚠️ Информация об обеспечении безопасности
            </mj-text>
            <mj-text color="#991b1b">
              <strong>Компонент:</strong> {{ component_name }}<br/>
              <strong>Текущая версия:</strong> {{ current_version }}<br/>
              <strong>Обновленная версия:</strong> {{ patched_version }}<br/>
              <strong>Серьезность:</strong> {{ severity_level }}<br/>
              <strong>CVE ID:</strong> {{ cve_id }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Детали уязвимости:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ vulnerability_description }}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Потенциальное воздействие:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ impact_description }}
        </mj-text>

        {% if mitigation_steps %}
        <mj-spacer height="30px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              Временное устранение последствий
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ mitigation_steps }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Требуется действие: немедленно установите обновление
        </mj-text>

        <mj-spacer height="20px" />

        <mj-button href="{{ update_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Установить обновление безопасности
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ advisory_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Прочитать руководство по обеспечению безопасности
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Если вам нужна помощь, немедленно свяжитесь с поддержкой Spwig.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🔒 Требуется обновление безопасности

Критическое обновление безопасности

Обнаружена уязвимость безопасности в {{ component_name }}. Пожалуйста, немедленно обновитесь, чтобы защитить свой магазин.

⚠️ ИНФОРМАЦИЯ О БЕЗОПАСНОСТИ:
- Компонент: {{ component_name }}
- Текущая версия: {{ current_version }}
- Обновленная версия: {{ patched_version }}
- Серьезность: {{ severity_level }}
- CVE ID: {{ cve_id }}

ДЕТАЛИ УВЯЗВИМОСТИ:
{{ vulnerability_description }}

ПОТЕНЦИАЛЬНОЕ ВОЗДЕЙСТВИЕ:
{{ impact_description }}

{% if mitigation_steps %}
ВРЕМЕННОЕ УСТРАНЕНИЕ ПОСЛЕДСТВИЙ:
{{ mitigation_steps }}
{% endif %}

ТРЕБУЕМЫЕ ДЕЙСТВИЯ: НЕМЕДЛЕННО УСТАНОВИТЬ ОБНОВЛЕНИЕ

Установить обновление безопасности: {{ update_url }}
Прочитать руководство по обеспечению безопасности: {{ advisory_url }}

Если вам нужна помощь, немедленно свяжитесь с поддержкой Spwig.