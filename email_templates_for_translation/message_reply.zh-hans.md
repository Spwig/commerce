---
template_type: message_reply
category: Core E-commerce
---

# Email Template: message_reply

## Subject
Re: {{ original_subject }} - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          {{ staff_name }} 回复了您的消息
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          你好 {{ customer_name }}，
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ reply_message }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" font-style="italic">
              <strong>您原始的消息：</strong><br/>
              {{ original_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        {% if conversation_url %}
        <mj-button href="{{ conversation_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          查看对话
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
{{ staff_name }} 回复了您的消息

你好 {{ customer_name }}，

{{ reply_message }}

---
您原始的消息：
{{ original_message }}
---

{% if conversation_url %}查看对话： {{ conversation_url }}{% endif %}

需要进一步帮助？
邮箱：{{ support_email }}
电话：{{ support_phone }}