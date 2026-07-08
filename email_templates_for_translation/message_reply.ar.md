---
template_type: message_reply
category: Core E-commerce
---

# Email Template: message_reply

## Subject
إعادة: {{ original_subject }} - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          {{ staff_name }} replied to your message
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ reply_message }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" font-style="italic">
              <strong>Your original message:</strong><br/>
              {{ original_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        {% if conversation_url %}
        <mj-button href="{{ conversation_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          View Conversation
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
{{ staff_name }} replied to your message

Hi {{ customer_name }},

{{ reply_message }}

---
Your original message:
{{ original_message }}
---

{% if conversation_url %}View conversation: {{ conversation_url }}{% endif %}

Need further assistance?
Email: {{ support_email }}
Phone: {{ support_phone }}