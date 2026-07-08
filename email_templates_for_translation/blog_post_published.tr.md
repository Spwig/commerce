---
template_type: blog_post_published
category: Blog
---

# Email Template: blog_post_published

## Subject
Yeni Gönderi: {{ post_title }} - {{ shop_name }} Blog

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          📝 Yeni Blog Gönderisi
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Merhaba {{ subscriber_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Yeni bir gönderi yayımladık ve bunu çok seveceğinizi düşünüyoruz!
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
          {{ author_name }} tarafından | {{ publish_date }} | {{ reading_time }} dakika okunabilir
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ post_excerpt }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ post_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Tam makaleyi oku
        </mj-button>

        <mj-spacer height="30px" />

        {% if related_posts %}
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Ayrıca ilgilenebileceğiniz:
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
              <a href="{{ post.url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Daha fazlası için tıklayın →</a>
            </mj-text>
          </mj-column>
        </mj-section>
        {% endfor %}
        <mj-spacer height="30px" />
        {% endif %}

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Bu e-postayı {{ blog_name }} aboneliğiniz nedeniyle alıyorsunuz.<br/>
          <a href="{{ unsubscribe_url }}">Blog güncellemelerinden abonelikten çıkın</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📝 YENİ BLOG GÖNDERİSİ

Merhaba {{ subscriber_name }},

Yeni bir gönderi yayımladık ve bunu çok seveceğinizi düşünüyoruz!

{{ post_title }}
{{ author_name }} tarafından | {{ publish_date }} | {{ reading_time }} dakika okunabilir

{{ post_excerpt }}

Tam makaleyi oku: {{ post_url }}

{% if related_posts %}
YAKIN OLARAK İLGİLENEBİLECEĞİNİZ:
{% for post in related_posts %}
- {{ post.title }}
  {{ post.url }}
{% endfor %}
{% endif %}

---

Bu e-postayı {{ blog_name }} aboneliğiniz nedeniyle alıyorsunuz.
Blog güncellemelerinden abonelikten çıkın: {{ unsubscribe_url }}