---
template_type: affiliate_commission_earned
category: Affiliate Program
---

# Email Template: affiliate_commission_earned

## Subject
Вы заработали комиссию в размере {{ commission_amount }}!

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
          💰 Заработанная комиссия!
        </mj-text>
        <mj-text font-size="18px" color="#6c757d" align="center">
          Отличные новости от {{ shop_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Commission Display -->
    <mj-section background-color="#28a745" padding="40px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-bottom="10px">
          💵 Ваша комиссия
        </mj-text>
        <mj-text font-size="48px" font-weight="bold" color="#ffffff" align="center" line-height="1">
          {{ commission_amount }}
        </mj-text>
        <mj-text font-size="14px" color="rgba(255, 255, 255, 0.9)" align="center" padding-top="10px">
          От заказа #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          Здравствуйте, {{ affiliate_name }},
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Поздравляем! Вы заработали комиссию в размере {{ commission_amount }} от заказа #{{ order_number }}.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Продвигайте {{ shop_name }}, чтобы заработать больше комиссий. Чем больше продаж вы совершите, тем больше вы заработаете!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Commission Details -->
    <mj-section background-color="#f8f9fa" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          <strong>Номер заказа:</strong> #{{ order_number }}<br/>
          <strong>Размер комиссии:</strong> {{ commission_amount }}<br/>
          <strong>Процент комиссии:</strong> {{ commission_rate }}%
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          Перейти к панели аффилиатов
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          Вопросы? <a href="mailto:{{ support_email }}" style="color: #007bff;">
            Свяжитесь с поддержкой
          </a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Вы заработали комиссию в размере {{ commission_amount }}!

Здравствуйте, {{ affiliate_name }},

Поздравляем! Вы заработали комиссию в размере {{ commission_amount }} от заказа #{{ order_number }}.

Детали комиссии:
- Номер заказа: #{{ order_number }}
- Размер комиссии: {{ commission_amount }}
- Процент комиссии: {{ commission_rate }}%

Продвигайте {{ shop_name }}, чтобы заработать больше комиссий.

Посмотрите на панели: {{ portal_url }}

{{ shop_name }}
Вопросы? Свяжитесь с {{ support_email }}