---
template_type: affiliate_payout_completed
category: Affiliate Program
---

# Email Template: affiliate_payout_completed

## Subject
✓ Выплата завершена: {{ payout_amount }}

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
          🎉 Выплата завершена!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Payout Display -->
    <mj-section background-color="#28a745" padding="40px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-bottom="10px">
          ✓ Успешно оплачено
        </mj-text>
        <mj-text font-size="48px" font-weight="bold" color="#ffffff" align="center" line-height="1">
          {{ payout_amount }}
        </mj-text>
        <mj-text font-size="14px" color="rgba(255, 255, 255, 0.9)" align="center" padding-top="10px">
          ID выплаты: {{ payout_id }}
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
          Ваша выплата в размере {{ payout_amount }} была успешно завершена!
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Средства были отправлены на ваш способ оплаты. В зависимости от вашего банка или платежного процессора, на появление средств на вашем счету может потребоваться 1–2 рабочих дня.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Благодарим вас за продвижение {{ shop_name }}. Продолжайте в том же духе!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          Просмотреть детали выплаты
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
✓ Выплата завершена: {{ payout_amount }}

Здравствуйте, {{ affiliate_name }},

Ваша выплата в размере {{ payout_amount }} была успешно завершена!

Детали выплаты:
- ID выплаты: {{ payout_id }}
- Сумма: {{ payout_amount }}
- Способ оплаты: {{ payout_method }}

Средства были отправлены на ваш способ оплаты. В зависимости от вашего банка или платежного процессора, на появление средств на вашем счету может потребоваться 1–2 рабочих дня.

Благодарим вас за продвижение {{ shop_name }}. Продолжайте в том же духе!

Просмотреть детали выплаты: {{ portal_url }}

{{ shop_name }}
Вопросы? Свяжитесь с {{ support_email }}