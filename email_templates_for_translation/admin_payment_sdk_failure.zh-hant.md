---
template_type: admin_payment_sdk_failure
category: Admin Notifications
---

# Email Template: admin_payment_sdk_failure

## Subject
支付服務商問題 - {{ provider_name }} SDK 載入失敗

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.warning|default:'#f59e0b' }}">
          支付服務商問題
        </mj-text>
        <mj-text>
          在結帳過程中，有客戶的 {{ provider_name }} 支付 SDK 無法載入。這可能表示服務商出現服務中斷。
        </mj-text>
        <mj-text>
          <strong>服務商：</strong> {{ provider_name }}
        </mj-text>
        <mj-text>
          <strong>錯誤類型：</strong> {{ error_type }}
        </mj-text>
        <mj-text>
          <strong>時間：</strong> {{ timestamp }}
        </mj-text>
        <mj-text>
          <strong>失敗次數（最近一小時）：</strong> {{ failure_count }}
        </mj-text>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          此通知每小時每服務商僅限發送一次。如果問題仍然存在，請查看服務商儀表板或聯繫他們的支援團隊。
        </mj-text>
        <mj-button href="{{ admin_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          查看支付設定
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
支付服務商問題

在結帳過程中，有客戶的 {{ provider_name }} 支付 SDK 無法載入。這可能表示服務商出現服務中斷。

服務商： {{ provider_name }}
錯誤類型： {{ error_type }}
時間： {{ timestamp }}
失敗次數（最近一小時）： {{ failure_count }}

此通知每小時每服務商僅限發送一次。如果問題仍然存在，請查看服務商儀表板或聯繫他們的支援團隊。

查看支付設定： {{ admin_url }}