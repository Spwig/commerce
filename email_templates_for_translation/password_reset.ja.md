---
template_type: password_reset
category: Authentication
---

# Email Template: password_reset

## Subject
パスワードリセットのリクエスト

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          パスワードリセットのリクエスト
        </mj-text>
        <mj-text>
          パスワードのリセットを要求するメールを受け取りました。下のボタンをクリックしてリセットしてください。
        </mj-text>
        <mj-button href="{{ reset_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          パスワードをリセット
        </mj-button>
        <mj-text color="#666666" font-size="12px">
          このメールを要求していない場合は、無視しても安全です。
        </mj-text>
        <mj-text color="#666666" font-size="12px">
          このリンクは{{ expiry_hours }}時間後に無効になります。
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
パスワードリセットのリクエスト

パスワードのリセットを要求するメールを受け取りました。下のリンクをクリックしてリセットしてください。

{{ reset_url }}

このメールを要求していない場合は、無視しても安全です。
このリンクは{{ expiry_hours }}時間後に無効になります。