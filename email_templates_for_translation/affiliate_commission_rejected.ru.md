---
template_type: affiliate_commission_rejected
category: Affiliate Program
---

# Email Template: affiliate_commission_rejected

## Subject
Обновление статуса комиссии - Заказ #{{ order_number }}

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
          Обновление статуса комиссии
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
          Мы хотели сообщить вам, что комиссия за заказ #{{ order_number }} ({{ commission_amount }}) не была одобрена.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Это обычно происходит, когда заказ отменяется или возвращается до окончания периода комиссии.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Если у вас есть вопросы по этой комиссии, пожалуйста, свяжитесь с нашей службой поддержки.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#6c757d" color="#ffffff" href="{{ portal_url }}">
          Просмотреть панель аффилиатов
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
Обновление статуса комиссии - Заказ #{{ order_number }}

Здравствуйте, {{ affiliate_name }},

Мы хотели сообщить вам, что комиссия за заказ #{{ order_number }} ({{ commission_amount }}) не была одобрена.

Это обычно происходит, когда заказ отменяется или возвращается до окончания периода комиссии.

Если у вас есть вопросы по этой комиссии, пожалуйста, свяжитесь с нашей службой поддержки.

Просмотреть панель аффилиатов: {{ portal_url }}

{{ shop_name }}
Вопросы? Свяжитесь с {{ support_email }}