---
template_type: affiliate_high_commission_alert
category: Affiliate Program
---

# Email Template: affiliate_high_commission_alert

## Subject
⚠️ Обнаружена необычная активность комиссии - {{ affiliate_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Высокая комиссия
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Обнаружена необычная активность
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Аффилиат {{ affiliate_name }} получил необычно высокую комиссию. Это требует проверки для предотвращения мошенничества.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Детали предупреждения:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Аффилиат:</strong> {{ affiliate_name }} ({{ affiliate_id }})<br/>
              <strong>Сумма комиссии:</strong> <span style="font-weight: bold; color: #dc2626;">{{ commission_amount }}</span><br/>
              <strong>Сумма заказа:</strong> {{ order_value }}<br/>
              <strong>Идентификатор заказа:</strong> {{ order_number }}<br/>
              <strong>Обнаружено:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Почему это было отмечено:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ flag_reason }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Рекомендуемые действия:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Проверьте детали заказа на подлинность<br/>
          • Проверьте историю рефералов аффилиата<br/>
          • Убедитесь, что клиент не связан с реферером<br/>
          • Одобрите или отклоните комиссию в админ-панели
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ review_commission_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Проверить комиссию
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ affiliate_details_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Просмотреть информацию об аффилиате
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Эта комиссия ожидает проверки и не будет выплачена до ее одобрения.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ ВЫСОКАЯ КОМИССИЯ

Обнаружена необычная активность

Аффилиат {{ affiliate_name }} получил необычно высокую комиссию. Это требует проверки для предотвращения мошенничества.

ДЕТАЛИ ПРЕДУПРЕЖДЕНИЯ:
- Аффилиат: {{ affiliate_name }} ({{ affiliate_id }})
- Сумма комиссии: {{ commission_amount }}
- Сумма заказа: {{ order_value }}
- Идентификатор заказа: {{ order_number }}
- Обнаружено: {{ detected_at }}

ПОЧЕМУ ЭТО БЫЛО ОТМЕЧЕНО:
{{ flag_reason }}

РЕКОМЕНДУЕМЫЕ ДЕЙСТВИЯ:
• Проверьте детали заказа на подлинность
• Проверьте историю рефералов аффилиата
• Убедитесь, что клиент не связан с реферером
• Одобрите или отклоните комиссию в админ-панели

Проверить комиссию: {{ review_commission_url }}
Просмотреть информацию об аффилиате: {{ affiliate_details_url }}

Эта комиссия ожидает проверки и не будет выплачена до ее одобрения.