---
template_type: blog_digest_weekly
category: Blog
---

# Email Template: blog_digest_weekly

## Subject
本周在 {{ blog_name }}: {{ post_count }} 篇新文章

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          📰 周报
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          {{ week_start }} - {{ week_end }}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          你好 {{ subscriber_name }}，
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          本周我们发布了以下内容 - {{ post_count }} 篇新文章只为你而写！
        </mj-text>

        <mj-spacer height="30px" />

        {% for post in posts %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          {% if post.featured_image %}
          <mj-column width="35%">
            <mj-image src="{{ post.featured_image }}" alt="{{ post.title }}" border-radius="8px" />
          </mj-column>
          <mj-column width="65%">
          {% else %}
          <mj-column width="100%">
          {% endif %}
            <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" line-height="1.3">
              {{ post.title }}
            </mj-text>
            <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              作者 {{ post.author }} | {{ post.reading_time }} 分钟阅读
            </mj-text>
            <mj-spacer height="10px" />
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.6">
              {{ post.excerpt }}
            </mj-text>
            <mj-spacer height="10px" />
            <mj-text font-size="14px">
              <a href="{{ post.url }}" style="color: {{ theme.color.primary|default:'#2563eb' }}; font-weight: bold;">阅读更多 →</a>
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="20px" />
        {% endfor %}

        <mj-button href="{{ blog_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          查看所有文章
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          你正在从 {{ blog_name }} 接收周报。
          <br/>
          <a href="{{ unsubscribe_url }}">退订</a> | <a href="{{ preferences_url }}">电子邮件偏好设置</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📰 周报
{{ week_start }} - {{ week_end }}

你好 {{ subscriber_name }}，

本周我们发布了以下内容 - {{ post_count }} 篇新文章只为你而写！

{% for post in posts %}
{{ post.title }}
作者 {{ post.author }} | {{ post.reading_time }} 分钟阅读
{{ post.excerpt }}
阅读更多：{{ post.url }}

{% endfor %}

查看所有文章：{{ blog_url }}

---
你正在从 {{ blog_name }} 接收周报。
退订：{{ unsubscribe_url }}
电子邮件偏好设置：{{ preferences_url }}