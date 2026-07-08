---
template_type: blog_comment_approved
category: Blog
---

# Email Template: blog_comment_approved

## Subject
Ваш комментарий к "{{ post_title }}" утвержден - {{ blog_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#f0fdf4">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#059669" align="center">
          ✓ Комментарий утвержден
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Здравствуйте {{ commenter_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Великолепные новости! Ваш комментарий к "{{ post_title }}" утвержден и теперь виден другим читателям.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="14px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Ваш комментарий:
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.6">
              {{ comment_text }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ comment_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          Посмотреть ваш комментарий
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          Мы сообщим вам, когда кто-то ответит на ваш комментарий.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ КОММЕНТАРИЙ УТВЕРЖДЁН

Здравствуйте {{ commenter_name }},

Великолепные новости! Ваш комментарий к "{{ post_title }}" утвержден и теперь виден другим читателям.

ВАШ КОММЕНТАРИЙ:
{{ comment_text }}

Посмотреть ваш комментарий: {{ comment_url }}

Мы сообщим вам, когда кто-нибуть ответит на ваш комментарий.