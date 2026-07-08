---
template_type: pos_cash_discrepancy_alert
category: POS
---

# Email Template: pos_cash_discrepancy_alert

## Subject
⚠️ 現金差額警示：{{ terminal_name }} - {{ discrepancy_amount }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ 現金差額警示
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          現金差異警示
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          在 {{ terminal_name }} 結束班次時，發現 {{ discrepancy_amount }} 的現金差額。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              差異細節：
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>終端機：</strong> {{ terminal_name }}<br/>
              <strong>收銀員：</strong> {{ cashier_name }}<br/>
              <strong>班次日期：</strong> {{ shift_date }}<br/>
              <strong>班次時長：</strong> {{ shift_duration }}<br/>
              <strong>發現時間：</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          現金清點：
        </mj-text>

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="#92400e">
              <strong>預期現金：</strong> {{ expected_cash }}<br/>
              <strong>實際清點現金：</strong> {{ counted_cash }}<br/>
              <strong>差額：</strong> <span style="font-weight: bold; font-size: 18px;">{{ discrepancy_amount }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>開班現金：</strong> {{ opening_cash }}<br/>
              <strong>現金銷售：</strong> {{ cash_sales }}<br/>
              <strong>現金退款：</strong> {{ cash_refunds }}<br/>
              <strong>現金支付：</strong> {{ cash_paid_out }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if cashier_note %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          收銀員備註：
        </mj-text>
        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              "{{ cashier_note }}"
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          建議措施：
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. 檢查交易歷史是否有錯誤<br/>
          2. 檢查是否有未記錄的現金付款<br/>
          3. 確認現金清點是否準確<br/>
          4. 在班次備註中記錄差異<br/>
          5. 如有必要，與收銀員聯繫
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ shift_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          查看班次報告
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ transaction_history_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          檢查交易
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ 發現現金差額

現金差異警示

在 {{ terminal_name }} 結束班次時，發現 {{ discrepancy_amount }} 的現金差額。

差異細節：
- 終端機：{{ terminal_name }}
- 收銀員：{{ cashier_name }}
- 班次日期：{{ shift_date }}
- 班次時長：{{ shift_duration }}
- 發現時間：{{ detected_at }}

現金清點：
- 預期現金：{{ expected_cash }}
- 實際清點現金：{{ counted_cash }}
- 差額：{{ discrepancy_amount }}

明細：
- 開班現金：{{ opening_cash }}
- 現金銷售：{{ cash_sales }}
- 現金退款：{{ cash_refunds }}
- 現金支付：{{ cash_paid_out }}

{% if cashier_note %}
收銀員備註：
"{{ cashier_note }}"
{% endif %}

建議措施：
1. 檢查交易歷史是否有錯誤
2. 檢查是否有未記錄的現金付款
3. 確認現金清點是否準確
4. 在班次備註中記錄差異
5. 如有必要，與收銀員聯繫

查看班次報告：{{ shift_report_url }}
檢查交易：{{ transaction_history_url }}