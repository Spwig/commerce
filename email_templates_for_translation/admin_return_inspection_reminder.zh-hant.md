---
template_type: admin_return_inspection_reminder
category: Admin Notifications
---

# Email Template: admin_return_inspection_reminder

## Subject
退貨已收到 - 需要檢查訂單 #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          需要退貨檢查
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          已收到退貨包裹，需要進行檢查。
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>訂單：</strong>#{{ order_number }}<br/>
              <strong>收到時間：</strong>{{ received_at }}<br/>
              <strong>需檢查項目數：</strong>{{ items_count }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        {% if admin_url %}
        <mj-button href="{{ admin_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          在管理後台查看退貨
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
需要退貨檢查

已收到退貨包裹，需要進行檢查。

訂單：#{{ order_number }}
收到時間：{{ received_at }}
需檢查項目數：{{ items_count }}

{% if admin_url %}在管理後台查看：{{ admin_url }}{% endif %}