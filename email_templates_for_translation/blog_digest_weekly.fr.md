---
template_type: blog_digest_weekly
category: Blog
---

# Email Template: blog_digest_weekly

## Subject
Ce week-end sur {{ blog_name }}: {{ post_count }} nouvel article{{ post_count|pluralize }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          📰 Weekly Digest
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          {{ week_start }} - {{ week_end }}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ subscriber_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Here's what we published this week - {{ post_count }} new article{{ post_count|pluralize }} just for you!
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
              By {{ post.author }} | {{ post.reading_time }} min read
            </mj-text>
            <mj-spacer height="10px" />
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.6">
              {{ post.excerpt }}
            </mj-text>
            <mj-spacer height="10px" />
            <mj-text font-size="14px">
              <a href="{{ post.url }}" style="color: {{ theme.color.primary|default:'#2563eb' }}; font-weight: bold;">Read more →</a>
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="20px" />
        {% endfor %}

        <mj-button href="{{ blog_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          View All Posts
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          You're receiving weekly digests from {{ blog_name }}.<br/>
          <a href="{{ unsubscribe_url }}">Unsubscribe</a> | <a href="{{ preferences_url }}">Email Preferences</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📰 WEEKLY DIGEST
{{ week_start }} - {{ week_end }}

Hi {{ subscriber_name }},

Here's what we published this week - {{ post_count }} new article{{ post_count|pluralize }} just for you!

{% for post in posts %}
{{ post.title }}
By {{ post.author }} | {{ post.reading_time }} min read
{{ post.excerpt }}
Read more: {{ post.url }}

{% endfor %}

View all posts: {{ blog_url }}

---
You're receiving weekly digests from {{ blog_name }}.
Unsubscribe: {{ unsubscribe_url }}
Email Preferences: {{ preferences_url }}