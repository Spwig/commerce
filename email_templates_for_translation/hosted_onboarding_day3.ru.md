---
template_type: hosted_onboarding_day3
category: License
---

# Email Template: hosted_onboarding_day3

## Subject
Создайте свой каталог - {{ store_name }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Начало работы: Ваши товары
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Создайте отличный каталог для {{ store_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Привет, {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          Ваш магазин <strong>{{ store_name }}</strong> полностью настроен. Теперь пришло время создать каталог товаров. Вот пять советов, чтобы начать.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 1 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Импорт товаров из CSV
        </mj-text>
        <mj-text font-size="14px">
          Уже есть список товаров? Перейдите в <strong>Admin > Catalog > Import</strong>, чтобы массово импортировать товары из файла CSV. Это самый быстрый способ заполнить ваш магазин.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 2 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Организуйте с помощью категорий и фильтров
        </mj-text>
        <mj-text font-size="14px">
          Создайте категории и фильтры атрибутов, чтобы клиенты могли легко просматривать и находить то, что ищут. Хорошо организованные каталоги приводят к более высоким показателям конверсии.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 3 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Напишите убедительные описания товаров
        </mj-text>
        <mj-text font-size="14px">
          Отличные описания продают товары. Сфокусируйтесь на преимуществах, а не только на характеристиках. Расскажите клиентам, почему им нужен ваш товар и как он решает их проблему.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 4 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Загрузите высококачественные изображения товаров
        </mj-text>
        <mj-text font-size="14px">
          Четкие и профессиональные изображения сильно влияют на восприятие. Загрузите несколько ракурсов и используйте одинаковое освещение. Spwig автоматически оптимизирует изображения для быстрой загрузки.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 5 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Настройте варианты товаров
        </mj-text>
        <mj-text font-size="14px">
          Если ваши товары доступны в разных размерах, цветах или стилях, создайте варианты, чтобы клиенты могли выбрать именно то, что им нужно. Каждый вариант может иметь собственную цену, уровень запаса и изображения.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Управление товарами" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Начало работы: Ваши товары - {{ store_name }}

Привет, {{ name|default:'there' }},

Ваш магазин {{ store_name }} полностью настроен. Теперь пришло время создать каталог товаров. Вот пять советов, чтобы начать.

1. Импорт товаров из CSV
Уже есть список товаров? Перейдите в Admin > Catalog > Import, чтобы массово импортировать товары из файла CSV.

2. Организуйте с помощью категорий и фильтров
Создайте категории и фильтры атрибутов, чтобы клиенты могли легко просматривать и находить то, что ищут.

3. Напишите убедительные описания товаров
Отличные описания продают товары. Сфокусируйтесь на преимуществах, а не только на характеристиках. Расскажите клиентам, почему им нужен ваш товар.

4. Загрузите высококачественные изображения товаров
Четкие и профессиональные изображения сильно влияют на восприятие. Загрузите несколько ракурсов и используйте одинаковое освещение.

5. Настройте варианты товаров
Если ваши товары доступны в разных размерах, цветах или стилях, создайте варианты, чтобы клиенты могли выбрать именно то, что им нужно.

Управление товарами: {{ admin_url }}

Нужна помощь? Свяжитесь с {{ support_email }}