---
template_type: blog_post_published
category: Blog
---

# Email Template: blog_post_published

## Subject
Nuovo Post: {{ post_title }} - {{ shop_name }} Blog

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          📝 Nuovo Post del Blog
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ subscriber_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Abbiamo appena pubblicato un nuovo post che pensiamo ti piacerà!
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
          Di {{ author_name }} | {{ publish_date }} | {{ reading_time }} min read
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ post_excerpt }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ post_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Leggi l'articolo completo
        </mj-button>

        <mj-spacer height="30px" />

        {% if related_posts %}
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Potresti anche voler leggere:
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
              <a href="{{ post.url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Leggi di più →</a>
            </mj-text>
          </mj-column>
        </mj-section>
        {% endfor %}
        <mj-spacer height="30px" />
        {% endif %}

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Ricevi questo messaggio perché ti sei iscritto al {{ blog_name }}.<br/>
          <a href="{{ unsubscribe_url }}">Annulla l'iscrizione alle notifiche del blog</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📝 NUOVO POST DEL BLOG

Hi {{ subscriber_name }},

Abbiamo appena pubblicato un nuovo post che pensiamo ti piacerà!

{{ post_title }}
Di {{ author_name }} | {{ publish_date }} | {{ reading_time }} min read

{{ post_excerpt }}

Leggi l'articolo completo: {{ post_url }}

{% if related_posts %}
YOU MIGHT ALSO LIKE:
{% for post in related_posts %}
- {{ post.title }}
  {{ post.url }}
{% endfor %}
{% endif %}

---

Ricevi questo messaggio perché ti sei iscritto al {{ blog_name }}.
Annulla l'iscrizione alle notifiche del blog: {{ unsubscribe_url }}