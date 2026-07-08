---
template_type: component_update_installed
category: Component Updates
---

# Email Template: component_update_installed

## Subject
✓ {{ component_name }} обновлен до v{{ new_version }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          ✓ Установлено обновление
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Успешное обновление
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ component_name }} было успешно обновлено до версии {{ new_version }}.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Детали установки:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Компонент:</strong> {{ component_name }}<br/>
              <strong>Предыдущая версия:</strong> {{ old_version }}<br/>
              <strong>Новая версия:</strong> {{ new_version }}<br/>
              <strong>Установлено:</strong> {{ installed_at }}<br/>
              <strong>Длительность:</strong> {{ installation_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if post_install_message %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Важная информация:
        </mj-text>
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              {{ post_install_message }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        {% if requires_configuration %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚙️ Требуется настройка
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ configuration_message }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        {% if configuration_url %}
        <mj-button href="{{ configuration_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Настроить компонент
        </mj-button>
        <mj-spacer height="10px" />
        {% endif %}

        <mj-button href="{{ component_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Просмотреть детали компонента
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ УСТАНОВЛЕНО ОБНОВЛЕНИЕ

Успешное обновление

{{ component_name }} было успешно обновлено до версии {{ new_version }}.

ДЕТАЛИ УСТАНОВКИ:
- Компонент: {{ component_name }}
- Предыдущая версия: {{ old_version }}
- Новая версия: {{ new_version }}
- Установлено: {{ installed_at }}
- Длительность: {{ installation_duration }}

{% if post_install_message %}
ВАЖНАЯ ИНФОРМАЦИЯ:
{{ post_install_message }}
{% endif %}

{% if requires_configuration %}
⚙️ ТРЕБУЕТСЯ НАСТРОЙКА:
{{ configuration_message }}
{% endif %}

{% if configuration_url %}Настроить компонент: {{ configuration_url }}{% endif %}
Просмотреть детали компонента: {{ component_url }}