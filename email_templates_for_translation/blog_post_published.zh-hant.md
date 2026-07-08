---
template_type: blog_post_published
category: Blog
---

# Email Template: blog_post_published

## Subject
新文章：{{ post_title }} - {{ shop_name }} 部落格

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          📝 新部落格文章
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ subscriber_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          我們剛剛發布了一篇新文章，我們認為您會喜歡！
        </mj-text>

        <mj-spacer height="30px" />

        {% if featured_image %}
        <mj-image src="{{ featured_image }}" alt="{{ post_title }}" border-radius="8px" />
        <mj-spacer height="20px" />
        {% endif %}

        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" line-height="1.3">
          {{ post_title }}
        </mj-text>

        <mj-spacer height="15px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          By {{ author_name }} | {{ publish_date }} | {{ reading_time }} min read
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ post_excerpt }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ post_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          閱讀完整文章
        </mj-button>

        <mj-spacer height="30px" />

        {% if related_posts %}
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          你可能也會喜歡：
        </mj-text>

        {% for post in related_posts %}
        <mj-spacer height="15px" />
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="4px" padding="12px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ post.title }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              {{ post.excerpt }}
            </mj-text>
            <mj-text font-size="14px">
              <a href="{{ post.url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">閱讀更多 →</a>
            </mj-text>
          </mj-column>
        </mj-section>
        {% endfor %}
        <mj-spacer height="30px" />
        {% endif %}

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          您收到此郵件是因為您訂閱了 {{ blog_name }}。<br/>
          <a href="{{ unsubscribe_url }}">取消訂閱部落格更新</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📝 新部落格文章

Hi {{ subscriber_name }},

我們剛剛發布了一篇新文章，我們認為您會喜歡！

{{ post_title }}
By {{ author_name }} | {{ publish_date }} | {{ reading_time }} min read

{{ post_excerpt }}

閱讀完整文章：{{ post_url }}

{% if related_posts %}
YOU MIGHT ALSO LIKE:
{% for post in related_posts %}
- {{ post.title }}
  {{ post.url }}
{% endfor %}
{% endif %}

---
您收到此郵件是因為您訂閱了 {{ blog_name }}。
取消訂閱部落格更新：{{ unsubscribe_url }}