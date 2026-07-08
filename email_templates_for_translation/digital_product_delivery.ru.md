---
template_type: digital_product_delivery
category: Digital Products
---

# Email Template: digital_product_delivery

## Subject
Ваш цифровой продукт готов - Заказ #{{ order_number }}

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
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          Ваш цифровой продукт готов!
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
          Спасибо за покупку! Ваш цифровой продукт теперь готов к загрузке.
        </mj-text>
        <mj-text font-weight="bold">
          Заказ #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Product Details -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          {{ product_name }}
        </mj-text>
        <mj-text color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Версия: {{ product_version }}
        </mj-text>
        <mj-text color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Размер файла: {{ file_size }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Download Button -->
    <mj-section>
      <mj-column>
        <mj-button href="{{ download_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" padding="15px 30px" border-radius="6px">
          Скачать сейчас
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Important Information -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          <strong>Важная информация:</strong>
        </mj-text>
        {% if download_limit %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Вы можете загрузить этот продукт {{ download_limit }} раз(а)
        </mj-text>
        {% endif %}
        {% if expiration_days %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Ссылка на загрузку истекает через {{ expiration_days }} дней
        </mj-text>
        {% endif %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Сохраните это письмо для будущего использования
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    <mj-section>
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          Нужна помощь? Свяжитесь с нашей службой поддержки по адресу {{ support_email }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Ваш цифровой продукт готов!

Здравствуйте, {{ customer_name }},

Спасибо за покупку! Ваш цифровой продукт теперь готов к загрузке.

Заказ #{{ order_number }}

Продукт: {{ product_name }}
Версия: {{ product_version }}
Размер файла: {{ file_size }}

Скачайте свой продукт здесь:
{{ download_url }}

Важная информация:
{% if download_limit %}• Вы можете загрузить этот продукт {{ download_limit }} раз(а)
{% endif %}{% if expiration_days %}• Ссылка на загрузку истекает через {{ expiration_days }} дней
{% endif %}• Сохраните это письмо для будущего использования

Нужна помощь? Свяжитесь с нашей службой поддержки по адресу {{ support_email }}