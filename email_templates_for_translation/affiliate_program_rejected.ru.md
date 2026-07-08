---
template_type: affiliate_program_rejected
category: Affiliate Program
---

# Email Template: affiliate_program_rejected

## Subject
Обновление заявки на программу

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
          Спасибо, что подали заявку на продвижение {{ program_name }}.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          После рассмотрения вашей заявки мы решили не одобрить её в данный момент.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Вы всё ещё можете продвигать другие программы в нашей партнёрской сети.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#6c757d" color="#ffffff" href="{{ portal_url }}">
          Посмотреть другие программы
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
Обновление заявки на программу

Здравствуйте {{ affiliate_name }},

Спасибо, что подали заявку на продвижение {{ program_name }}.

После рассмотрения вашей заявки мы решили не одобрить её в данный момент.

Вы всё ещё можете продвигать другие программы в нашей партнёрской сети.

Посмотреть другие программы: {{ portal_url }}

{{ shop_name }}
Вопросы? Свяжитесь с {{ support_email }}