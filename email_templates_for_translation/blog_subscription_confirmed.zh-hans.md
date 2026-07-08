---
template_type: blog_subscription_confirmed
category: Blog
---

# Email Template: blog_subscription_confirmed

## Subject
请确认您对{{ blog_name }}的订阅

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          确认您的订阅
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          你好 {{ subscriber_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          感谢您订阅 {{ blog_name }}！为了完成订阅并开始接收更新，请确认您的电子邮件地址。
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ confirmation_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          确认订阅
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              无法点击按钮？将此链接复制粘贴到浏览器中：<br/>
              <span style="color: {{ theme.color.primary|default:'#2563eb' }}; font-family: 'Courier New', monospace;">{{ confirmation_url }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>为什么要确认？</strong><br/>
          邮件确认可以帮助我们确保您希望接收更新并防止垃圾邮件。您的隐私和收件箱对我们来说很重要。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          没有订阅？您可以安全地忽略此电子邮件。
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
确认您的订阅

你好 {{ subscriber_name }},

感谢您订阅 {{ blog_name }}！为了完成订阅并开始接收更新，请确认您的电子邮件地址。

确认订阅：{{ confirmation_url }}

为什么要确认？
邮件确认可以帮助我们确保您希望接收更新并防止垃圾邮件。您的隐私和收件箱对我们来说很重要。

没有订阅？您可以安全地忽略此电子邮件。