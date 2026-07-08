---
template_type: component_update_available
category: Component Updates
---

# Email Template: component_update_available

## Subject
Доступно обновление: {{ component_name }} v{{ new_version }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📦 Доступно обновление
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Доступна новая версия
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Доступна новая версия {{ component_name }} для вашего магазина Spwig.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Детали обновления:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Компонент:</strong> {{ component_name }}<br/>
              <strong>Текущая версия:</strong> {{ current_version }}<br/>
              <strong>Новая версия:</strong> {{ new_version }}<br/>
              <strong>Дата выпуска:</strong> {{ release_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Что нового:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ changelog }}
        </mj-text>

        {% if breaking_changes %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ Разрывные изменения
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ breaking_changes }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ update_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Установить обновление
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          <a href="{{ changelog_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">
            Просмотреть полный журнал изменений
          </a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📦 ДОСТУПНО ОБНОВЛЕНИЕ

Доступна новая версия

Доступна новая версия {{ component_name }} для вашего магазина Spwig.

ДЕТАЛИ ОБНОВЛЕНИЯ:
- Компонент: {{ component_name }}
- Текущая версия: {{ current_version }}
- Новая версия: {{ new_version }}
- Дата выпуска: {{ release_date }}

ЧТО НОВОГО:
{{ changelog }}

{% if breaking_changes %}
⚠️ РАЗРЫВНЫЕ ИЗМЕНЕНИЯ:
{{ breaking_changes }}
{% endif %}

Установить обновление: {{ update_url }}
Просмотреть полный журнал изменений: {{ changelog_url }}

