---
template_type: hosted_onboarding_tips
category: License
---

# Email Template: hosted_onboarding_tips

## Subject
Советы по использованию {{ store_name }}

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
          Советы для начала работы
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Сделайте максимум из вашего магазина Spwig
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Здравствуйте {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          Теперь, когда <strong>{{ store_name }}</strong> запущен, вот несколько советов, которые помогут вам максимально использовать ваш магазин.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 1: Theme -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Настройте внешний вид
        </mj-text>
        <mj-text font-size="14px">
          Перейдите в <strong>Дизайн > Настройки темы</strong>, чтобы выбрать тему, загрузить логотип и задать цвета бренда. Ваш магазин обновляется мгновенно, поэтому вы можете предварительно просмотреть изменения в режиме реального времени.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 2: Products -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Добавьте товары
        </mj-text>
        <mj-text font-size="14px">
          Перейдите в <strong>Каталог > Товары</strong>, чтобы начать добавлять товары. Вы можете создавать варианты товаров (размер, цвет), задавать цены, управлять запасами и загружать высококачественные изображения.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 3: Payments -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Настройте оплату
        </mj-text>
        <mj-text font-size="14px">
          Перейдите в <strong>Настройки > Поставщики оплаты</strong>, чтобы подключить Stripe, PayPal или другой способ оплаты. Вы можете включить несколько поставщиков, чтобы клиенты могли платить тем способом, который им удобен.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 4: Shipping -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Настройте доставку
        </mj-text>
        <mj-text font-size="14px">
          В разделе <strong>Настройки > Доставка</strong> настройте зоны доставки и тарифы. Вы можете создать правила доставки с фиксированной стоимостью, по весу или бесплатную доставку для разных регионов.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 5: SEO -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Улучшите SEO
        </mj-text>
        <mj-text font-size="14px">
          Spwig автоматически генерирует карты сайта и метатеги. Перейдите в <strong>Настройки > SEO</strong>, чтобы настроить заголовки страниц, описания и изображения для социальных сетей, чтобы помочь клиентам найти ваш магазин.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Go to Admin Panel" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Советы для начала работы - {{ store_name }}

Здравствуйте {{ name|default:'there' }},

Теперь, когда {{ store_name }} запущен, вот несколько советов, которые помогут вам максимально использовать ваш магазин.

1. Настройте внешний вид
Перейдите в Дизайн > Настройки темы, чтобы выбрать тему, загрузить логотип и задать цвета бренда.

2. Добавьте товары
Перейдите в Каталог > Товары, чтобы начать добавлять товары с вариантами, ценами и изображениями.

3. Настройте оплату
Перейдите в Настройки > Поставщики оплаты, чтобы подключить Stripe, PayPal или другой способ оплаты.

4. Настройте доставку
В разделе Настройки > Доставка настройте зоны доставки и тарифы для разных регионов.

5. Улучшите SEO
Перейдите в Настройки > SEO, чтобы настроить заголовки страниц, описания и изображения для социальных сетей, чтобы помочь клиентам найти ваш магазин.

Перейти в панель администратора: {{ admin_url }}

Нужна помощь? Свяжитесь с {{ support_email }}