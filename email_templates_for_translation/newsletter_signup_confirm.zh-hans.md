---
template_type: newsletter_signup_confirm
category: Newsletter
---

# Email Template: newsletter_signup_confirm

## Subject
请确认您对 {{ store_name }} 的订阅

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          确认您的订阅
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          感谢您订阅 {{ store_name }}！请确认您的电子邮件地址，以开始接收我们的更新和优惠。
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ confirmation_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          确认订阅
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              无法点击按钮？请将此链接复制并粘贴到您的浏览器中：<br/>
              <span style="color: {{ theme.color.primary|default:'#2563eb' }}; font-family: 'Courier New', monospace;">{{ confirmation_url }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>为什么要确认？</strong><br/>
          确认您的电子邮件有助于我们确保您确实希望接收我们的更新，并保持您的收件箱无垃圾邮件。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          未进行订阅？您可以安全地忽略此邮件。
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
请确认您对 {{ store_name }} 的订阅

感谢您订阅 {{ store_name }}！请确认您的电子邮件地址，以开始接收我们的更新和优惠：

{{ confirmation_url }}

确认您的电子邮件有助于我们确保您确实希望接收我们的更新，并保持您的收件箱无垃圾邮件。

未进行订阅？您可以安全地忽略此邮件。