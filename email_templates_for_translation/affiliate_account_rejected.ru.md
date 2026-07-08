---
template_type: affiliate_account_rejected
category: Affiliate Program
---

# Email Template: affiliate_account_rejected

## Subject
Обновление заявки на партнера

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
          Обновление заявки
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
          Спасибо, что проявили интерес к присоединению к партнерской программе {{ shop_name }}.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          После рассмотрения вашей заявки мы решили не продолжать процесс на данном этапе.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Это решение основано на текущих требованиях нашей партнерской программы и может не отражать вашу квалификацию или потенциал.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Вы всегда можете подать заявку снова в будущем, если изменились ваши обстоятельства.
        </mj-text>
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
Обновление заявки на партнера

Здравствуйте {{ affiliate_name }},

Спасибо, что проявили интерес к присоединению к партнерской программе {{ shop_name }}.

После рассмотрения вашей заявки мы решили не продолжать процесс на данном этапе.

Это решение основано на текущих требованиях нашей партнерской программы и может не отражать вашу квалификацию или потенциал.

Вы всегда можете подать заявку снова в будущем, если изменились ваши обстоятельства.

{{ shop_name }}
Вопросы? Свяжитесь с {{ support_email }}