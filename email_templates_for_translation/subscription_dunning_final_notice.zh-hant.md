---
template_type: subscription_dunning_final_notice
category: Subscriptions
---

# Email Template: subscription_dunning_final_notice

## Subject
⚠️ 最後通知：您的訂閱將在 {{ days_until_cancellation }} 天後取消

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#991b1b" align="center">
          ⚠️ 最後通知
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          訂閱取消即將發生
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          這是您的最後通知。我們無法處理您的 {{ plan_name }} 訂閱付款。如果在 {{ days_until_cancellation }} 天內未收到付款，您的訂閱將被取消。
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b" font-size="16px">
              ⚠️ 付款失敗 - 需要採取行動
            </mj-text>
            <mj-text color="#991b1b">
              <strong>訂閱:</strong> {{ plan_name }}<br/>
              <strong>應付金額:</strong> {{ amount_due }}<br/>
              <strong>失敗次數:</strong> {{ retry_count }}<br/>
              <strong>最近一次嘗試:</strong> {{ last_retry_date }}<br/>
              <strong>取消日期:</strong> <span style="font-weight: bold; font-size: 16px;">{{ cancellation_date }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          付款錯誤:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" font-family="monospace" color="{{ theme.color.text|default:'#4b5563' }}">
              {{ payment_error_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          將會發生什麼:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          如果在 {{ cancellation_date }} 前未收到付款：<br/>
          • 您的訂閱將被取消<br/>
          • 您將失去所有訂閱權益的訪問權<br/>
          • 您的數據可能會被刪除（請參閱保留政策）<br/>
          • 您需要重新訂閱才能恢復訪問
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          現在更新您的付款方式
        </mj-text>

        <mj-spacer height="20px" />

        <mj-button href="{{ update_payment_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          更新付款方式
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          常見問題與解決方案:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • <strong>卡片過期:</strong> 使用目前有效的信用卡更新<br/>
          • <strong>資金不足:</strong> 確保賬戶餘額充足<br/>
          • <strong>卡片被拒絕:</strong> 聯絡銀行或使用其他卡片<br/>
          • <strong>地址不匹配:</strong> 確認帳單地址與卡片地址一致
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" font-weight="bold">
              需要幫助嗎？
            </mj-text>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              如果您遇到付款問題或需要協助，請立即聯繫我們的支援團隊。
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          聯絡支援
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          如果您想取消訂閱，可以在您的帳戶設定中進行操作。
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ 最後通知

訂閱取消即將發生

Hi {{ customer_name }},

這是您的最後通知。我們無法處理您的 {{ plan_name }} 訂閱付款。如果在 {{ days_until_cancellation }} 天內未收到付款，您的訂閱將被取消。

⚠️ 付款失敗 - 需要採取行動：
- 訂閱：{{ plan_name }}
- 應付金額：{{ amount_due }}
- 失敗次數：{{ retry_count }}
- 最近一次嘗試：{{ last_retry_date }}
- 取消日期：{{ cancellation_date }}

付款錯誤：
{{ payment_error_message }}

將會發生什麼：
如果在 {{ cancellation_date }} 前未收到付款：
• 您的訂閱將被取消
• 您將失去所有訂閱權益的訪問權
• 您的數據可能會被刪除（請參閱保留政策）
• 您需要重新訂閱才能恢復訪問

現在更新您的付款方式

常見問題與解決方案：
• 卡片過期：使用目前有效的信用卡更新
• 資金不足：確保賬戶餘額充足
• 卡片被拒絕：聯繫銀行或使用其他卡片
• 地址不匹配：確認帳單地址與卡片地址一致

需要幫助嗎？
如果您遇到付款問題或需要協助，請立即聯繫我們的支援團隊。

更新付款方式：{{ update_payment_url }}
聯繫支援：{{ support_url }}

如果您想取消訂閱，可以在您的帳戶設定中進行操作。