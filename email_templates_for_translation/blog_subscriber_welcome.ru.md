---
template_type: blog_subscriber_welcome
category: Blog
---

# Email Template: blog_subscriber_welcome

## Subject
Добро пожаловать в {{ blog_name }}! 🎉

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          🎉 Добро пожаловать в {{ blog_name }}!
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Здравствуйте, {{ subscriber_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Спасибо, что подписались! Мы рады делиться с вами нашим последним контентом.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="#065f46">
              Что ожидать:
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.8">
              ✓ Новые посты доставляются в ваш почтовый ящик<br/>
              ✓ Эксклюзивный контент только для подписчиков<br/>
              ✓ {{ publish_frequency }} обновлений<br/>
              ✓ Нет спама, отписаться в любое время
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Начать чтение:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Проверьте наши самые популярные статьи:
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
              {{ post.reading_time }} мин чтения
            </mj-text>
            <mj-text font-size="14px">
              <a href="{{ post.url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Прочитать сейчас →</a>
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-button href="{{ blog_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Изучить все статьи
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Управление подпиской: <a href="{{ preferences_url }}">Параметры электронной почты</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 ДОБРО ПОЖАЛОВАТЬ В {{ blog_name }}!

Здравствуйте, {{ subscriber_name }},

Спасибо, что подписались! Мы рады делиться с вами нашим последним контентом.

ЧТО ОЖИДАТЬ:
✓ Новые посты доставляются в ваш почтовый ящик
✓ Эксклюзивный контент только для подписчиков
✓ {{ publish_frequency }} обновлений
✓ Нет спама, отписаться в любое время

НАЧАТЬ ЧТЕНИЕ - ПОПУЛЯРНЫЕ СТАТЬИ:
{% for post in popular_posts %}
- {{ post.title }} ({{ post.reading_time }} мин чтения)
  {{ post.url }}
{% endfor %}

Изучить все статьи: {{ blog_url }}

Управление подпиской: {{ preferences_url }}