---
template_type: blog_comment_reply
category: Blog
---

# Email Template: blog_comment_reply

## Subject
आपके टिप्पणी पर {{ replier_name }} ने उत्तर दिया

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          💬 आपके टिप्पणी पर नई टिप्पणी
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          हेलो {{ commenter_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ replier_name }} आपके टिप्पणी पर {{ post_title }} पर उत्तर दिया।
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              आपके टिप्पणी:
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              {{ original_comment }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="15px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" font-weight="bold" color="#065f46">
              {{ replier_name }} उत्तर दिया:
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              {{ reply_text }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ reply_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          देखें और उत्तर दें
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          उत्तर नोटिफिकेशन चाहते हैं? <a href="{{ unsubscribe_url }}">साबित करें</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
💬 आपके टिप्पणी पर नई टिप्पणी

हेलो {{ commenter_name }},

{{ replier_name }} आपके टिप्पणी पर {{ post_title }} पर उत्तर दिया।

आपके टिप्पणी:
{{ original_comment }}

{{ replier_name }} उत्तर दिया:
{{ reply_text }}

देखें और उत्तर दें: {{ reply_url }}

उत्तर नोटिफिकेशन चाहते हैं? साबित करें: {{ unsubscribe_url }}