---
template_type: blog_comment_reply
category: Blog
---

# Email Template: blog_comment_reply

## Subject
{{ replier_name }} replied to your comment on "{{ post_title }}"

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          💬 New Reply to Your Comment
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ commenter_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ replier_name }} replied to your comment on "{{ post_title }}".
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              Your comment:
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
              {{ replier_name }} replied:
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              {{ reply_text }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ reply_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          View & Reply
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Don't want reply notifications? <a href="{{ unsubscribe_url }}">Unsubscribe</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
💬 NEW REPLY TO YOUR COMMENT

Hi {{ commenter_name }},

{{ replier_name }} replied to your comment on "{{ post_title }}".

YOUR COMMENT:
{{ original_comment }}

{{ replier_name }} REPLIED:
{{ reply_text }}

View & reply: {{ reply_url }}

Don't want reply notifications? Unsubscribe: {{ unsubscribe_url }}

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| commenter_name | Original commenter | John |
| replier_name | Person who replied | Dr. Smith |
| post_title | Blog post title | 10 Tips for Better Sleep |
| original_comment | Original comment | Great article! These tips helped... |
| reply_text | Reply content | Glad you found it helpful! Try... |
| reply_url | Direct reply link | https://shop.com/en/blog/sleep-tips#comment-124 |
| unsubscribe_url | Unsub from replies | https://shop.com/en/blog/unsubscribe-replies/abc123 |

## Notes

- Transactional notification
- Encourages engagement/discussion
- Respects reply notification preferences
