---
template_type: affiliate_commission_reversed
category: Affiliate Program
---

# Email Template: affiliate_commission_reversed

## Subject
Комиссия отменена - Заказ #{{ order_number }}

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
          Комиссия отменена
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
          Комиссия за заказ #{{ order_number }} ({{ commission_amount }}) была отменена из-за возврата клиента.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Когда клиенты запрашивают возвраты, связанные комиссии автоматически отменяются, чтобы обеспечить точную бухгалтерию.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Это нормальная часть процесса аффилиатов. Продолжайте продвигать {{ shop_name }}, чтобы получать новые комиссии!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
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
Комиссия отменена - Заказ #{{ order_number }}

Здравствуйте, {{ affiliate_name }},

Комиссия за заказ #{{ order_number }} ({{ commission_amount }}) была отменена из-за возврата клиента.

Когда клиенты запрашивают возвраты, связанные комиссии автоматически отменяются, чтобы обеспечить точную бухгалтерию.

Это нормальная часть процесса аффилиатов. Продолжайте продвигать {{ shop_name }}, чтобы получать новые комиссии!

Просмотреть панель аффилиатов: {{ portal_url }}

{{ shop_name }}
Вопросы? Свяжитесь с {{ support_email }}
