---
template_type: affiliate_high_commission_alert
category: Affiliate Program
---

# Email Template: affiliate_high_commission_alert

## Subject
⚠️ 發現異常傭金活動 - {{ affiliate_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ 高傭金警示
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          發現異常活動
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          代理商 {{ affiliate_name }} 獲得了異常高的傭金。這需要審核以防止詐騙。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              警示詳情：
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>代理商：</strong> {{ affiliate_name }} ({{ affiliate_id }})<br/>
              <strong>傭金金額：</strong> <span style="font-weight: bold; color: #dc2626;">{{ commission_amount }}</span><br/>
              <strong>訂單金額：</strong> {{ order_value }}<br/>
              <strong>訂單編號：</strong> {{ order_number }}<br/>
              <strong>檢測時間：</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          為什麼會被標記：
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ flag_reason }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          建議操作：
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • 檢查訂單詳情以確認合法性<br/>
          • 查看代理商的推薦歷史<br/>
          • 確認客戶與推薦人無關聯<br/>
          • 在管理面板中批准或拒絕傭金
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ review_commission_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          審核傭金
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ affiliate_details_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          查看代理商詳情
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          這筆傭金正在等待審核，直到獲得批准前將不會支付。
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ 高傭金警示

發現異常活動

代理商 {{ affiliate_name }} 獲得了異常高的傭金。這需要審核以防止詐騙。

警示詳情：
- 代理商：{{ affiliate_name }} ({{ affiliate_id }})
- 傭金金額：{{ commission_amount }}
- 訂單金額：{{ order_value }}
- 訂單編號：{{ order_number }}
- 檢測時間：{{ detected_at }}

為什麼會被標記：
{{ flag_reason }}

建議操作：
• 檢查訂單詳情以確認合法性
• 查看代理商的推薦歷史
• 確認客戶與推薦人無關聯
• 在管理面板中批准或拒絕傭金

審核傭金：{{ review_commission_url }}
查看代理商詳情：{{ affiliate_details_url }}

這筆傭金正在等待審核，直到獲得批准前將不會支付。