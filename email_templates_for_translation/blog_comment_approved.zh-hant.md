---
template_type: blog_comment_approved
category: Blog
---

# Email Template: blog_comment_approved

## Subject
您對「{{ post_title }}」的評論已通過審核 - {{ blog_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#f0fdf4">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#059669" align="center">
          ✓ 評論已通過審核
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          您好 {{ commenter_name }}，
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          好消息！您在「{{ post_title }}」上的評論已通過審核，現在對其他讀者可見。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="14px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              您的評論：
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.6">
              {{ comment_text }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ comment_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          查看您的評論
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          當有人回應您的評論時，我們會通知您。
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ 評論已通過審核

您好 {{ commenter_name }}，

好消息！您在「{{ post_title }}」上的評論已通過審核，現在對其他讀者可見。

您的評論：
{{ comment_text }}

查看您的評論：{{ comment_url }}

當有人回應您的評論時，我們會通知您。