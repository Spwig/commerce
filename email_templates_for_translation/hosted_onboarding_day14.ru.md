---
template_type: hosted_onboarding_day14
category: License
---

# Email Template: hosted_onboarding_day14

## Subject
Далее - {{ store_name }}

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
          Начало работы: Расширенные функции
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Раскройте полный потенциал {{ store_name }}
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
          Вы уже несколько недель работаете с <strong>{{ store_name }}</strong>. Вот несколько расширенных функций, которые помогут вам вывести ваш магазин на новый уровень.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 1 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Настройте автоматизированные email-процессы
        </mj-text>
        <mj-text font-size="14px">
          Автоматизируйте коммуникацию с клиентами с помощью email-процессов. Настройте приветственные последовательности, послепокупочные напоминания и кампании по повторному вовлечению в разделе <strong>Marketing > Email Workflows</strong>.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 2 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Настройте правила налогообложения для ваших регионов
        </mj-text>
        <mj-text font-size="14px">
          Убедитесь, что вы взимаете правильные налоговые ставки. Перейдите в <strong>Settings > Tax</strong>, чтобы настроить правила налогообложения для каждого региона, в котором вы продаете. Вы можете настроить цену с учетом налогов или без учета налогов.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 3 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Изучите API для интеграций
        </mj-text>
        <mj-text font-size="14px">
          Если ваш план включает доступ к API, вы можете интегрировать свой магазин с внешними инструментами и сервисами. Перейдите в <strong>Settings > API</strong>, чтобы сгенерировать ключи API и изучить документацию.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 4 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Изучите вашу панель аналитики
        </mj-text>
        <mj-text font-size="14px">
          Следите за производительностью вашего магазина. Ваша <strong>Dashboard</strong> отображает ключевые метрики, включая выручку, заказы, топ-продукты и инсайты клиентов, чтобы помочь вам принимать решения на основе данных.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 5 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Рассмотрите возможность добавления POS для продаж в магазине
        </mj-text>
        <mj-text font-size="14px">
          Продаете и в магазине? Функция POS Spwig позволяет обрабатывать продажи в магазине, которые синхронизируются с вашим онлайн-инвентарем и управлением заказами. Перейдите в <strong>Settings > Point of Sale</strong>, чтобы узнать больше.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Explore Your Dashboard" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Начало работы: Расширенные функции - {{ store_name }}

Привет, {{ name|default:'there' }},

Вы уже несколько недель работаете с {{ store_name }}. Вот несколько расширенных функций, которые помогут вам вывести ваш магазин на новый уровень.

1. Настройте автоматизированные email-процессы
Автоматизируйте коммуникацию с клиентами с помощью приветственных последовательностей, послепокупочных напоминаний и кампаний по повторному вовлечению.

2. Настройте правила налогообложения для ваших регионов
Убедитесь, что вы взимаете правильные налоговые ставки. Перейдите в Settings > Tax, чтобы настроить правила для каждого региона.

3. Изучите API для интеграций
Если ваш план включает доступ к API, интегрируйте свой магазин с внешними инструментами. Перейдите в Settings > API, чтобы начать.

4. Изучите вашу панель аналитики
Ваша Dashboard отображает ключевые метрики, включая выручку, заказы, топ-продукты и инсайты клиентов.

5. Рассмотрите возможность добавления POS для продаж в магазине
Продаете и в магазине? Функция POS Spwig синхронизирует продажи в магазине с вашим онлайн-инвентарем.

Изучите вашу панель: {{ admin_url }}

Нужна помощь? Свяжитесь с {{ support_email }}