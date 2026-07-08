---
template_type: blog_post_published
category: Blog
---

# Email Template: blog_post_published

## Subject
Новая статья: {{ post_title }} - {{ shop_name }} Блог

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          📝 Новая статья в блоге
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Здравствуйте, {{ subscriber_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Мы только что опубликовали новую статью, которую думаем, что вам понравится!
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
          Автор: {{ author_name }} | {{ publish_date }} | {{ reading_time }} мин чтения
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ post_excerpt }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ post_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Прочитать полную статью
        </mj-button>

        <mj-spacer height="30px" />

        {% if related_posts %}
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Возможно, вам также понравятся:
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
              <a href="{{ post.url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Прочитать больше →</a>
            </mj-text>
          </mj-column>
        </mj-section>
        {% endfor %}
        <mj-spacer height="30px" />
        {% endif %}

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Вы получаете это, потому что подписались на {{ blog_name }}.<br/>
          <a href="{{ unsubscribe_url }}">Отписаться от обновлений блога</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📝 НОВАЯ СТАТЬЯ В БЛОГЕ

Здравствуйте, {{ subscriber_name }},

Мы только что опубликовали новую статью, которую думаем, что вам понравится!

{{ post_title }}
Автор: {{ author_name }} | {{ publish_date }} | {{ reading_time }} мин чтения

{{ post_excerpt }}

Прочитать полную статью: {{ post_url }}

{% if related_posts %}
ВОЗМОЖНО, ВАМ ТАКЖЕ ПОНРАВИТСЯ:
{% for post in related_posts %}
- {{ post.title }}
  {{ post.url }}
{% endfor %}
{% endif %}

---
Вы получаете это, потому что подписались на {{ blog_name }}.
Отписаться от обновлений блога: {{ unsubscribe_url }}