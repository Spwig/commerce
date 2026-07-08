---
template_type: hosted_onboarding_day7
category: License
---

# Email Template: hosted_onboarding_day7

## Subject
Расширьте свои продажи - {{ store_name }}

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
          Начало работы: маркетинг и рост
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Привлекайте трафик и продажи в {{ store_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Привет, {{ name|default:'there' }}!
        </mj-text>
        <mj-text>
          Теперь, когда <strong>{{ store_name }}</strong> начинает формироваться, пришло время сосредоточиться на привлечении трафика и росте продаж. Вот пять советов по маркетингу, чтобы начать.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 1 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Создайте свой первый промокод
        </mj-text>
        <mj-text font-size="14px">
          Предложите запусковый скидку, чтобы привлечь первых клиентов. Перейдите в <strong>Маркетинг > Промокоды</strong>, чтобы создать скидки с необязательными ограничениями по использованию и датой истечения срока.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 2 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Настройте восстановление заброшенных корзин
        </mj-text>
        <mj-text font-size="14px">
          Автоматически восстановите упущенные продажи. Включите письма по восстановлению заброшенных корзин в разделе <strong>Маркетинг > Заброшенные корзины</strong>, чтобы напомнить клиентам о товарах, которые они оставили.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 3 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Подключите свои социальные сети
        </mj-text>
        <mj-text font-size="14px">
          Свяжите свои профили в социальных сетях со своим магазином, чтобы клиенты могли найти и подписаться на вас. Добавьте ссылки на социальные сети в разделе <strong>Настройки > Социальные сети</strong>, чтобы отобразить их в подвале вашего магазина.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 4 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Настройте отслеживание Google Analytics
        </mj-text>
        <mj-text font-size="14px">
          Понимайте, откуда приходят ваши посетители и как они взаимодействуют с вашим магазином. Добавьте ваш идентификатор отслеживания Google Analytics в разделе <strong>Настройки > Анализ</strong>, чтобы начать сбор данных.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 5 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Создайте форму подписки на рассылку
        </mj-text>
        <mj-text font-size="14px">
          Начните строить свою базу электронной почты с самого начала. Добавьте форму подписки на рассылку в ваш магазин, чтобы собирать электронные адреса посетителей. Используйте эти контакты для продвижения, запуска новых продуктов и взаимодействия с клиентами.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Go to Marketing" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Начало работы: маркетинг и рост - {{ store_name }}

Привет, {{ name|default:'there' }},

Теперь, когда {{ store_name }} начинает формироваться, пришло время сосредоточиться на привлечении трафика и росте продаж. Вот пять советов по маркетингу, чтобы начать.

1. Создайте свой первый промокод
Предложите запусковый скидку, чтобы привлечь первых клиентов. Перейдите в Маркетинг > Промокоды, чтобы создать скидки с необязательными ограничениями по использованию и датой истечения срока.

2. Настройте восстановление заброшенных корзин
Автоматически восстановите упущенные продажи. Включите письма по восстановлению заброшенных корзин в разделе Маркетинг > Заброшенные корзины.

3. Подключите свои социальные сети
Свяжите свои профили в социальных сетях со своим магазином. Добавьте ссылки на социальные сети в разделе Настройки > Социальные сети.

4. Настройте отслеживание Google Analytics
Понимайте, откуда приходят ваши посетители. Добавьте ваш идентификатор отслеживания Google Analytics в разделе Настройки > Анализ.

5. Создайте форму подписки на рассылку
Начните строить свою базу электронной почты с самого начала. Добавьте форму подписки на рассылку, чтобы собирать электронные адреса посетителей для продвижения и взаимодействия.

Перейдите в раздел Маркетинг: {{ admin_url }}

Нужна помощь? Свяжитесь с {{ support_email }}