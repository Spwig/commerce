---
template_type: blog_post_published
category: Blog
---

# Email Template: blog_post_published

## Subject
New Post: {{ post_title }} - {{ shop_name }} Blog

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          📝 New Blog Post
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ subscriber_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          We just published a new post we think you'll love!
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
          Read Full Article
        </mj-button>

        <mj-spacer height="30px" />

        {% if related_posts %}
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          You Might Also Like:
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
              <a href="{{ post.url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Read more →</a>
            </mj-text>
          </mj-column>
        </mj-section>
        {% endfor %}
        <mj-spacer height="30px" />
        {% endif %}

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          You're receiving this because you subscribed to {{ blog_name }}.<br/>
          <a href="{{ unsubscribe_url }}">Unsubscribe from blog updates</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📝 NEW BLOG POST

Hi {{ subscriber_name }},

We just published a new post we think you'll love!

{{ post_title }}
By {{ author_name }} | {{ publish_date }} | {{ reading_time }} min read

{{ post_excerpt }}

Read full article: {{ post_url }}

{% if related_posts %}
YOU MIGHT ALSO LIKE:
{% for post in related_posts %}
- {{ post.title }}
  {{ post.url }}
{% endfor %}
{% endif %}

---
You're receiving this because you subscribed to {{ blog_name }}.
Unsubscribe from blog updates: {{ unsubscribe_url }}

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| subscriber_name | Subscriber's name | Sarah |
| post_title | Blog post title | 10 Tips for Better Sleep |
| post_excerpt | Post summary | Discover science-backed strategies to improve your sleep quality tonight... |
| author_name | Post author | Dr. Jane Smith |
| publish_date | Publication date | February 15, 2026 |
| reading_time | Estimated minutes | 5 |
| featured_image | Header image | https://shop.com/media/blog/sleep-tips.jpg |
| post_url | Full post link | https://shop.com/en/blog/better-sleep-tips |
| related_posts | Similar posts | [{title, excerpt, url}] |
| blog_name | Blog name | Health & Wellness Blog |
| unsubscribe_url | Unsub link | https://shop.com/en/blog/unsubscribe/abc123 |
| shop_name | Store name | Amazing Shop |

## Notes

- Marketing email - opt-in newsletter
- Sent when new post published
- Includes related posts for engagement
- Reading time helps set expectations
- Unsubscribe link required
