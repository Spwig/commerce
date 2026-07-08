---
template_type: digital_product_license_key
category: Digital Products
---

# Email Template: digital_product_license_key

## Subject
Ваш ключ лицензии - Заказ #{{ order_number }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="#059669" padding="20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          Ваш ключ лицензии готов
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Main Content -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Здравствуйте, {{ customer_name }},
        </mj-text>
        <mj-text>
          Спасибо за покупку {{ product_name }}! Вот ваш ключ лицензии для активации.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Key Box -->
    <mj-section background-color="#f0fdf4" padding="30px" border="2px solid #059669" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#065f46" font-weight="bold" align="center">
          ВАШ КЛЮЧ ЛИЦЕНЗИИ
        </mj-text>
        <mj-text font-size="20px" font-weight="bold" color="#059669" align="center" font-family="'Courier New', monospace" padding="10px 0">
          {{ license_key }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Нажмите, чтобы скопировать или аккуратно запишите
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Details -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" font-weight="bold">
          Детали лицензии:
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Продукт: {{ product_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Версия: {{ product_version }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Тип лицензии: {{ license_type }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Максимальное количество активаций: {{ max_activations }} устройство(а)
        </mj-text>
        {% if is_lifetime %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Срок действия: Лицензия на всю жизнь
        </mj-text>
        {% else %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Действует до: {{ expiration_date }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Activation Instructions -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold">
          Как активировать:
        </mj-text>
        <mj-text font-size="14px">
          1. Скачайте и установите программное обеспечение
        </mj-text>
        <mj-text font-size="14px">
          2. Откройте приложение
        </mj-text>
        <mj-text font-size="14px">
          3. Введите ваш ключ лицензии, когда вас об этом попросят
        </mj-text>
        <mj-text font-size="14px">
          4. Нажмите "Активировать", чтобы завершить процесс
        </mj-text>
      </mj-column>
    </mj-section>

    {% if download_url %}
    <!-- Download Button -->
    <mj-section>
      <mj-column>
        <mj-button href="{{ download_url }}" background-color="#059669" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" padding="15px 30px" border-radius="6px">
          Скачать программное обеспечение
        </mj-button>
      </mj-column>
    </mj-section>
    {% endif %}

    <!-- Important Notice -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.error|default:'#ef4444' }}" font-weight="bold">
          ⚠️ Важно:
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Сохраните это письмо - вам понадобится ключ лицензии для переустановки
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Не делитесь вашим ключом лицензии с другими
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Вы можете деактивировать устройства через панель управления вашей учетной записью
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    <mj-section>
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          Нужна помощь с активацией? Свяжитесь с {{ support_email }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Ваш ключ лицензии готов

Здравствуйте, {{ customer_name }},

Спасибо за покупку {{ product_name }}! Вот ваш ключ лицензии для активации.

ВАШ КЛЮЧ ЛИЦЕНЗИИ:
{{ license_key }}

Детали лицензии:
• Продукт: {{ product_name }}
• Версия: {{ product_version }}
• Тип лицензии: {{ license_type }}
• Максимальное количество активаций: {{ max_activations }} устройство(а)
{% if is_lifetime %}• Срок действия: Лицензия на всю жизнь{% else %}• Действует до: {{ expiration_date }}{% endif %}

Как активировать:
1. Скачайте и установите программное обеспечение
2. Откройте приложение
3. Введите ваш ключ лицензии, когда вас об этом попросят
4. Нажмите "Активировать", чтобы завершить процесс

{% if download_url %}Скачать программное обеспечение: {{ download_url }}

{% endif %}ВАЖНО:
• Сохраните это письмо - вам понадобится ключ лицензии для переустановки
• Не делитесь вашим ключом лицензии с другими
• Вы можете деактивировать устройства через панель управления вашей учетной записью

Нужна помощь с активацией? Свяжитесь с {{ support_email }}