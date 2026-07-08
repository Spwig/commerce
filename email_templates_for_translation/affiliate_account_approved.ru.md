---
template_type: affiliate_account_approved
category: Affiliate Program
---

# Email Template: affiliate_account_approved

## Subject
🎉 Добро пожаловать в партнерскую программу {{ shop_name }}!

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="#f8f9fa">
    <!-- Header -->
    <mj-section background-color="#ffffff" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="#212529" align="center">
          🎉 Ваша заявка одобрена!
        </mj-text>
        <mj-text font-size="18px" color="#6c757d" align="center">
          Добро пожаловать в нашу партнерскую программу
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Success Banner -->
    <mj-section background-color="#28a745" padding="40px 20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#ffffff" align="center">
          Теперь вы партнер!
        </mj-text>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-top="10px">
          Начните получать комиссионные сегодня
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          Здравствуйте {{ affiliate_name }},
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Поздравляем! Ваша заявка на участие в партнерской программе {{ shop_name }} одобрена.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Теперь вы можете начать продвижение наших продуктов и получать комиссионные за каждую сделку, которую вы сгенерируете.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- How it Works -->
    <mj-section background-color="#f8f9fa" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="#212529" align="center" padding-bottom="10px">
          Как это работает
        </mj-text>
        <mj-text font-size="14px" color="#6c757d">
          1. Получите уникальные партнерские ссылки из панели управления<br/>
          2. Поделитесь этими ссылками со своей аудиторией<br/>
          3. Получайте комиссию, когда люди покупают через ваши ссылки<br/>
          4. Получайте выплаты в соответствии с вашим графиком выплат
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          Доступ к панели управления партнером
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          Вопросы? <a href="mailto:{{ support_email }}" style="color: #007bff;">Свяжитесь с поддержкой</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 Добро пожаловать в партнерскую программу {{ shop_name }}!

Здравствуйте {{ affiliate_name }},

Поздравляем! Ваша заявка на участие в партнерской программе {{ shop_name }} одобрена.

Теперь вы можете начать продвижение наших продуктов и получать комиссионные за каждую сделку, которую вы сгенерируете.

Как это работает:
1. Получите уникальные партнерские ссылки из панели управления
2. Поделитесь этими ссылками со своей аудиторией
3. Получайте комиссию, когда люди покупают через ваши ссылки
4. Получайте выплаты в соответствии с вашим графиком выплат

Доступ к панели управления: {{ portal_url }}

{{ shop_name }}
Вопросы? Свяжитесь с {{ support_email }}