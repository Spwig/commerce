---
template_type: password_reset
category: Authentication
---

# Email Template: password_reset

## Subject
密碼重設請求

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          密碼重設請求
        </mj-text>
        <mj-text>
          我們收到了重設您密碼的請求。點擊下方按鈕以重設密碼。
        </mj-text>
        <mj-button href="{{ reset_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          重設密碼
        </mj-button>
        <mj-text color="#666666" font-size="12px">
          如果您沒有請求此操作，您可以放心忽略此郵件。
        </mj-text>
        <mj-text color="#666666" font-size="12px">
          此連結將在 {{ expiry_hours }} 小時後過期。
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
密碼重設請求

我們收到了重設您密碼的請求。點擊下方連結以重設密碼。

{{ reset_url }}

如果您沒有請求此操作，您可以放心忽略此郵件。此連結將在 {{ expiry_hours }} 小時後過期。