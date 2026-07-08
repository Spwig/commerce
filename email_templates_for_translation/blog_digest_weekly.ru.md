---
template_type: blog_digest_weekly
category: Blog
---

# Email Template: blog_digest_weekly

## Subject
На этой неделе на {{ blog_name }}: {{ post_count }} новых статей

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          📰 Еженедельный дайджест
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          {{ week_start }} - {{ week_end }}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Здравствуйте, {{ subscriber_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Вот что мы опубликовали на этой неделе - {{ post_count }} новых статей только для вас!
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
              Автор: {{ post.author }} | {{ post.reading_time }} мин чтения
            </mj-text>
            <mj-spacer height="10px" />
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.6">
              {{ post.excerpt }}
            </mj-text>
            <mj-spacer height="10px" />
            <mj-text font-size="14px">
              <a href="{{ post.url }}" style="color: {{ theme.color.primary|default:'#2563eb' }}; font-weight: bold;">Прочитать больше →</a>
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="20px" />
        {% endfor %}

        <mj-button href="{{ blog_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          Посмотреть все посты
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Вы получаете еженедельные дайджесты от {{ blog_name }}.<br/>
          <a href="{{ unsubscribe_url }}">Отписаться</a> | <a href="{{ preferences_url }}">Параметры электронной почты</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📰 ЕЖЕНЕДЕЛЬНЫЙ ДАЙДЖЕСТ
{{ week_start }} - {{ week_end }}

Здравствуйте, {{ subscriber_name }},

Вот что мы опубликовали на этой неделе - {{ post_count }} новых статей только для вас!

{% for post in posts %}
{{ post.title }}
Автор: {{ post.author }} | {{ post.reading_time }} мин чтения
{{ post.excerpt }}
Прочитать больше: {{ post.url }}

{% endfor %}

Посмотреть все посты: {{ blog_url }}

---

Вы получаете еженедельные дайджесты от {{ blog_name }}.
Отписаться: {{ unsubscribe_url }}
Параметры электронной почты: {{ preferences_url }}