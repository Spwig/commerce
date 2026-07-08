---
template_type: affiliate_monthly_report
category: Affiliate Program
---

# Email Template: affiliate_monthly_report

## Subject
Ваш ежемесячный отчет аффилиата - {{ month_name }} {{ year }}

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
          📊 Ежемесячный отчет аффилиата
        </mj-text>
        <mj-text font-size="18px" color="#6c757d" align="center">
          Сводка производительности за {{ month_name }} {{ year }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Summary Cards -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column width="33%">
        <mj-text font-size="14px" color="#6c757d" align="center" padding-bottom="5px">
          💰 Общий заработок
        </mj-text>
        <mj-text font-size="28px" font-weight="bold" color="#28a745" align="center" line-height="1">
          {{ total_earned }}
        </mj-text>
      </mj-column>
      <mj-column width="33%">
        <mj-text font-size="14px" color="#6c757d" align="center" padding-bottom="5px">
          📦 Комиссии
        </mj-text>
        <mj-text font-size="28px" font-weight="bold" color="#007bff" align="center" line-height="1">
          {{ commission_count }}
        </mj-text>
      </mj-column>
      <mj-column width="33%">
        <mj-text font-size="14px" color="#6c757d" align="center" padding-bottom="5px">
          📈 Среднее на продажу
        </mj-text>
        <mj-text font-size="28px" font-weight="bold" color="#6f42c1" align="center" line-height="1">
          {{ avg_commission }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section background-color="#f8f9fa" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          Здравствуйте {{ affiliate_name }},
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Вот сводка вашей производительности за {{ month_name }} {{ year }}. Отличная работа в этом месяце!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Top Orders Table -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="#212529" padding-bottom="15px">
          🏆 Топ {{ top_orders_count }} заказов
        </mj-text>
        <mj-text font-size="14px" color="#212529">
          <table style="width: 100%; border-collapse: collapse;">
            <thead>
              <tr style="background-color: #f8f9fa;">
                <th style="padding: 10px; text-align: left; border-bottom: 2px solid #dee2e6;">Заказ</th>
                <th style="padding: 10px; text-align: right; border-bottom: 2px solid #dee2e6;">Комиссия</th>
                <th style="padding: 10px; text-align: right; border-bottom: 2px solid #dee2e6;">Дата</th>
              </tr>
            </thead>
            <tbody>
              {% for order in top_orders %}
              <tr>
                <td style="padding: 10px; border-bottom: 1px solid #dee2e6;">#{{ order.order_number }}</td>
                <td style="padding: 10px; text-align: right; border-bottom: 1px solid #dee2e6; color: #28a745; font-weight: 600;">{{ order.commission_amount }}</td>
                <td style="padding: 10px; text-align: right; border-bottom: 1px solid #dee2e6; color: #6c757d;">{{ order.order_date }}</td>
              </tr>
              {% endfor %}
            </tbody>
          </table>
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Payment Status -->
    <mj-section background-color="#e3f2fd" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          <strong>💳 Статус выплаты</strong>
        </mj-text>
        <mj-text font-size="14px" color="#212529">
          Ожидающая баланс: <strong>{{ pending_balance }}</strong><br/>
          Статус: {{ payment_status }}
          {% if next_payout_date %}
          <br/>Следующая выплата: {{ next_payout_date }}
          {% endif %}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          Посмотреть полный дашборд
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
Ваш ежемесячный отчет аффилиата - {{ month_name }} {{ year }}

Здравствуйте {{ affiliate_name }},

Вот сводка вашей производительности за {{ month_name }} {{ year }}:

📊 ЕЖЕМЕСЯЧНЫЙ ОБЗОР
- Общий заработок: {{ total_earned }}
- Количество комиссий: {{ commission_count }}
- Среднее на продажу: {{ avg_commission }}

🏆 ТОП {{ top_orders_count }} ЗАКАЗОВ
{% for order in top_orders %}
#{{ order.order_number }} - {{ order.commission_amount }} ({{ order.order_date }})
{% endfor %}

💳 СТАТУС ВЫПЛАТЫ
Ожидающая баланс: {{ pending_balance }}
Статус: {{ payment_status }}
{% if next_payout_date %}Следующая выплата: {{ next_payout_date }}{% endif %}

Посмотрите полный дашборд: {{ portal_url }}

Отличная работа в этом месяце!

{{ shop_name }}
Вопросы? Свяжитесь с {{ support_email }}