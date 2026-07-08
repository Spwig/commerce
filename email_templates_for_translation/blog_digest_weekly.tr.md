---
template_type: blog_digest_weekly
category: Blog
---

# Email Template: blog_digest_weekly

## Subject
Bu hafta {{ blog_name }}: {{ post_count }} yeni makale{{ post_count|pluralize }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          📰 Haftalık Özet
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          {{ week_start }} - {{ week_end }}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Merhaba {{ subscriber_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Bu hafta ne yayımladık - {{ post_count }} yeni makale{{ post_count|pluralize }} sadece sizi için!
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
              {{ post.author }} tarafından | {{ post.reading_time }} dakika okunabilir
            </mj-text>
            <mj-spacer height="10px" />
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.6">
              {{ post.excerpt }}
            </mj-text>
            <mj-spacer height="10px" />
            <mj-text font-size="14px">
              <a href="{{ post.url }}" style="color: {{ theme.color.primary|default:'#2563eb' }}; font-weight: bold;">Daha fazlasını oku →</a>
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="20px" />
        {% endfor %}

        <mj-button href="{{ blog_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          Tüm Yazıları Görüntüle
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Haftalık özeti {{ blog_name }} dan alıyorsunuz.<br/>
          <a href="{{ unsubscribe_url }}">Abonelikten Çık</a> | <a href="{{ preferences_url }}">E-posta Tercihleri</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📰 HAFTALIK ÖZET
{{ week_start }} - {{ week_end }}

Merhaba {{ subscriber_name }},

Bu hafta ne yayımladık - {{ post_count }} yeni makale{{ post_count|pluralize }} sadece sizi için!

{% for post in posts %}
{{ post.title }}
{{ post.author }} tarafından | {{ post.reading_time }} dakika okunabilir
{{ post.excerpt }}
Daha fazlasını oku: {{ post.url }}

{% endfor %}

Tüm yazıları görüntüle: {{ blog_url }}

---

Haftalık özeti {{ blog_name }} dan alıyorsunuz.
Abonelikten çık: {{ unsubscribe_url }}
E-posta tercihleri: {{ preferences_url }}