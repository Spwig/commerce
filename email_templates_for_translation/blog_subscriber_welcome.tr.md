---
template_type: blog_subscriber_welcome
category: Blog
---

# Email Template: blog_subscriber_welcome

## Subject
🎉 {{ blog_name }}'a Hoş Geldiniz!

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          🎉 {{ blog_name }}'a Hoş Geldiniz!
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Merhaba {{ subscriber_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Aboneliğiniz için teşekkür ederiz! En son içeriklerimizi sizinle paylaşmaktan memnuniyet duyarız.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="#065f46">
              Bekleyeceğiniz Şeyler:
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.8">
              ✓ Postlarımızı e-posta adresinize sunacağız<br/>
              ✓ Sadece aboneler için özel içerikler
              ✓ {{ publish_frequency }} güncellemeler
              ✓ Spam yok, her zaman abonelikten çıkabilirsiniz
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Okuma Başlat:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          En popüler makalelerimizi inceleyin:
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
              {{ post.reading_time }} dakika okuma
            </mj-text>
            <mj-text font-size="14px">
              <a href="{{ post.url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Şimdi Oku →</a>
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-button href="{{ blog_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Tüm Makaleleri Keşfet
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Aboneliklerinizi yönetin: <a href="{{ preferences_url }}">E-posta Tercihlerim</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 {{ blog_name }}'a Hoş Geldiniz!

Merhaba {{ subscriber_name }},

Aboneliğiniz için teşekkür ederiz! En son içeriklerimizi sizinle paylaşmaktan memnuniyet duyarız.

Bekleyeceğiniz Şeyler:
✓ Postlarımızı e-posta adresinize sunacağız
✓ Sadece aboneler için özel içerikler
✓ {{ publish_frequency }} güncellemeler
✓ Spam yok, her zaman abonelikten çıkabilirsiniz

OKUMA BAŞLAT - POPÜLER MAKALELER:
{% for post in popular_posts %}
- {{ post.title }} ({{ post.reading_time }} dakika okuma)
  {{ post.url }}
{% endfor %}

Tüm makaleleri keşfet: {{ blog_url }}

Aboneliklerinizi yönetin: {{ preferences_url }}