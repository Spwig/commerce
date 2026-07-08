---
template_type: feed_validation_errors
category: Product Feeds
---

# Email Template: feed_validation_errors

## Subject
⚠️ {{ feed_name }}: обнаружено {{ error_count }} ошибок валидации

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Ошибки проверки фида
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Обнаружены проблемы с качеством данных
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Обнаружено {{ error_count }} ошибок валидации в {{ feed_name }}. Эти проблемы могут препятствовать появлению товаров на {{ platform_name }}.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Резюме проверки:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Feed:</strong> {{ feed_name }}<br/>
              <strong>Platform:</strong> {{ platform_name }}<br/>
              <strong>Validated:</strong> {{ validated_at }}<br/>
              <strong>Total Products:</strong> {{ total_products }}<br/>
              <strong>Products with Errors:</strong> {{ affected_products }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Основные ошибки:
        </mj-text>

        {% for error in top_errors %}
        <mj-section background-color="#fee2e2" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="#991b1b" font-weight="bold">
              {{ error.type }}
            </mj-text>
            <mj-text font-size="13px" color="#991b1b">
              {{ error.count }} продукт{{ error.count|pluralize }} повреждены: {{ error.message }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Что исправить:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ fix_instructions }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ errors_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Просмотреть все ошибки
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ admin_feed_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Управление фидом
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Исправьте эти ошибки, чтобы убедиться, что все товары появятся на {{ platform_name }}.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ ОШИБКИ ПРОВЕРКИ ФИДА

Обнаружены проблемы с качеством данных

Обнаружено {{ error_count }} ошибок валидации в {{ feed_name }}. Эти проблемы могут препятствовать появлению товаров на {{ platform_name }}.

РЕЗЮМЕ ПРОВЕРКИ:
- Feed: {{ feed_name }}
- Platform: {{ platform_name }}
- Validated: {{ validated_at }}
- Total Products: {{ total_products }}
- Products with Errors: {{ affected_products }}

TOP ERRORS:
{% for error in top_errors %}
{{ error.type }}: {{ error.count }} продукт{{ error.count|pluralize }} - {{ error.message }}
{% endfor %}

WHAT TO FIX:
{{ fix_instructions }}

Просмотреть все ошибки: {{ errors_url }}
Управление фидом: {{ admin_feed_url }}

Исправьте эти ошибки, чтобы убедиться, что все товары появятся на {{ platform_name }}.