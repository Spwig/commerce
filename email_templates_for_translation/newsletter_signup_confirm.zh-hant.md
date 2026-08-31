---
template_type: newsletter_signup_confirm
category: Newsletter
---

# Email Template: newsletter_signup_confirm

## Subject
請確認您對 {{ store_name }} 的訂閱

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          請確認您的訂閱
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          感謝您註冊以接收 {{ store_name }} 的消息！請確認您的電子郵件地址以開始接收我們的更新和優惠。
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ confirmation_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          確認訂閱
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              無法點擊按鈕？將此連結複製貼上到瀏覽器：<br/>
              <span style="color: {{ theme.color.primary|default:'#2563eb' }}; font-family: 'Courier New', monospace;">{{ confirmation_url }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>為什麼要確認？</strong><br/>
          確認您的電子郵件有助於我們確保您真的想要接收我們的更新，並保持您的郵箱免受垃圾郵件。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          沒有註冊？您可以安全地忽略此電子郵件。
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
請確認您對 {{ store_name }} 的訂閱

感謝您註冊以接收 {{ store_name }} 的消息！請確認您的電子郵件地址以開始接收我們的更新和優惠：

{{ confirmation_url }}

確認您的電子郵件有助於我們確保您真的想要接收我們的更新，並保持您的郵箱免受垃圾郵件。

沒有註冊？您可以安全地忽略此電子郵件。