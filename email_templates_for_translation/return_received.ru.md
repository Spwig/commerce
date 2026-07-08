---
template_type: return_received
category: Returns
---

# Email Template: return_received

## Subject
Ваш возврат получен - Заказ #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#eff6ff' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.primary|default:'#1d4ed8' }}">
          Возврат получен
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.primary|default:'#1d4ed8' }}">
          Заказ #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Здравствуйте, {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Мы получили возвращенные товары для заказа <strong>#{{ order_number }}</strong>.
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>Что будет дальше:</strong>
        </mj-text>

        <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          1. Наша команда проверит возвращенные товары в течение 2-3 рабочих дней<br/>
          2. Мы проверим, что товары находятся в оригинальном состоянии<br/>
          3. После завершения проверки мы обработаем ваш возврат<br/>
          4. Вы получите подтверждающее письмо, как только возврат будет обработан
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Возврат будет зачислен на ваш первоначальный способ оплаты и может занять 5-10 рабочих дней, чтобы отобразиться на вашем счете.
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Спасибо за ваше терпение!
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Возврат получен - Заказ #{{ order_number }}

Здравствуйте, {{ customer_name }},

Мы получили возвращенные товары для заказа #{{ order_number }}.

Что будет дальше:
1. Наша команда проверит возвращенные товары в течение 2-3 рабочих дней
2. Мы проверим, что товары находятся в оригинальном состоянии
3. После завершения проверки мы обработаем ваш возврат
4. Вы получите подтверждающее письмо, как только возврат будет обработан

Возврат будет зачислен на ваш первоначальный способ оплаты и может занять 5-10 рабочих дней, чтобы отобразиться на вашем счете.

Спасибо за ваше терпение!