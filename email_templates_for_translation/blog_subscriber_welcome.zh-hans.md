---
template_type: blog_subscriber_welcome
category: Blog
---

# Email Template: blog_subscriber_welcome

## Subject
欢迎来到 {{ blog_name }}！🎉

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          🎉 欢迎来到 {{ blog_name }}！
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          你好 {{ subscriber_name }}，
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          感谢订阅！我们很兴奋能与你分享我们的最新内容。
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="#065f46">
              你将收到的内容:
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.8">
              ✓ 新文章将发送到你的邮箱<br/>
              ✓ 专属订阅者内容<br/>
              ✓ {{ publish_frequency }} 次更新<br/>
              ✓ 没有垃圾邮件，随时取消订阅
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          开始阅读:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          查看我们最受欢迎的文章:
        </mj-text>

        <mj-spacer height="15px" />

        {% for post in popular_posts %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column width="30%">
            <mj-image src="{{ post.featured_image }}" alt="{{ post.title }}" border-radius="4px" />
          </mj-column>
          <mj-column width="70%">
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ post.title }}
            </mj-text>
            <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              {{ post.reading_time }} 分钟阅读
            </mj-text>
            <mj-text font-size="14px">
              <a href="{{ post.url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">阅读 →</a>
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-button href="{{ blog_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          浏览所有文章
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          管理你的订阅: <a href="{{ preferences_url }}">邮件偏好设置</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 欢迎来到 {{ blog_name }}！

你好 {{ subscriber_name }}，

感谢订阅！我们很兴奋能与你分享我们的最新内容。

你将收到的内容:
✓ 新文章将发送到你的邮箱
✓ 专属订阅者内容
✓ {{ publish_frequency }} 次更新
✓ 没有垃圾邮件，随时取消订阅

开始阅读 - 最受欢迎的文章：
{% for post in popular_posts %}
- {{ post.title }} ({{ post.reading_time }} 分钟阅读)
  {{ post.url }}
{% endfor %}

浏览所有文章：{{ blog_url }}

管理你的订阅：{{ preferences_url }}