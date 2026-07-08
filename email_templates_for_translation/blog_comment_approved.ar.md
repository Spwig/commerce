---
template_type: blog_comment_approved
category: Blog
---

# Email Template: blog_comment_approved

## Subject
تمت الموافقة على تعليقك حول "{{ post_title }}" - {{ blog_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#f0fdf4">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#059669" align="center">
          ✓ تمت الموافقة على التعليق
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          مرحباً {{ commenter_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          أخبار سارة! تم تأكيد تعليقك حول "{{ post_title }}" وتم عرضه الآن على القراء الآخرين.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="14px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              تعليقك:
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.6">
              {{ comment_text }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ comment_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          اعرض تعليقك
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          سنقوم بإعلامك عندما يستجيب شخص ما لتعليقك.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ تمت الموافقة على التعليق

مرحباً {{ commenter_name }},

أخبار سارة! تم تأكيد تعليقك حول "{{ post_title }}" وتم عرضه الآن على القراء الآخرين.

تعليقك:
{{ comment_text }}

عرض تعليقك: {{ comment_url }}

سنقوم بإعلامك عندما يستجيب شخص ما لتعليقك.