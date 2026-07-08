---
template_type: shipping_exception
category: Shipping
---

# Email Template: shipping_exception

## Subject
Исключение при доставке - Заказ #{{ order_number }} требует внимания

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Исключение при доставке
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Здравствуйте, {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Мы пишем, чтобы сообщить вам о проблеме с вашей доставкой. Мы работаем над тем, чтобы как можно быстрее решить эту проблему.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#92400e">
              Детали исключения:
            </mj-text>
            <mj-text color="#92400e">
              <strong>Тип исключения:</strong> {{ exception_type }}<br/>
              <strong>Описание:</strong> {{ exception_description }}<br/>
              <strong>Произошло:</strong> {{ exception_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Информация о заказе:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Номер заказа:</strong> {{ order_number }}<br/>
              <strong>Номер отслеживания:</strong> {{ tracking_number }}<br/>
              <strong>Перевозчик:</strong> {{ carrier_name }}<br/>
              <strong>Текущее местоположение:</strong> {{ current_location }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Что происходит далее?
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          {{ resolution_steps }}
        </mj-text>

        <mj-spacer height="20px" />

        {% if action_required %}
        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              ⚠️ Действие требуется:
            </mj-text>
            <mj-text color="#7f1d1d">
              {{ action_required_description }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="20px" />
        {% endif %}

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Отслеживать заказ
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Связаться с поддержкой
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ ИСКЛЮЧЕНИЕ ПРИ ДОСТАВКЕ

Здравствуйте, {{ customer_name }},

Мы пишем, чтобы сообщить вам о проблеме с вашей доставкой. Мы работаем над тем, чтобы как можно быстрее решить эту проблему.

ДЕТАЛИ ИСКЛЮЧЕНИЯ:
- Тип исключения: {{ exception_type }}
- Описание: {{ exception_description }}
- Произошло: {{ exception_date }}

ИНФОРМАЦИЯ О ЗАКАЗЕ:
- Номер заказа: {{ order_number }}
- Номер отслеживания: {{ tracking_number }}
- Перевозчик: {{ carrier_name }}
- Текущее местоположение: {{ current_location }}

ЧТО ПРОИСХОДИТ ДАЛЕЕ?
{{ resolution_steps }}

{% if action_required %}
⚠️ ТРЕБУЕТСЯ ДЕЙСТВИЕ:
{{ action_required_description }}
{% endif %}

Отслеживать заказ: {{ tracking_url }}
Связаться с поддержкой: {{ support_url }}