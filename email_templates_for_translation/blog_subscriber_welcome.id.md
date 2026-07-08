---
template_type: blog_subscriber_welcome
category: Blog
---

# Email Template: blog_subscriber_welcome

## Subject
Selamat datang di {{ blog_name }}! 🎉

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          🎉 Selamat datang di {{ blog_name }}!
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ subscriber_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Terima kasih telah berlangganan! Kami sangat bersemangat untuk berbagi konten terbaru kami dengan Anda.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="#065f46">
              Apa yang Diharapkan:
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.8">
              ✓ Artikel baru dikirim ke kotak masuk Anda<br/>
              ✓ Konten eksklusif hanya untuk pelanggan<br/>
              ✓ {{ publish_frequency }} pembaruan<br/>
              ✓ Tidak ada spam, berlangganan kapan saja
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Mulai Membaca:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Cek artikel-artikel populer kami:
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
              {{ post.reading_time }} menit membaca
            </mj-text>
            <mj-text font-size="14px">
              <a href="{{ post.url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Baca sekarang →</a>
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-button href="{{ blog_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Eksplorasi Semua Artikel
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Kelola langganan Anda: <a href="{{ preferences_url }}">Preferensi Email</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 SELAMAT DATANG DI {{ blog_name }}!

Hi {{ subscriber_name }},

Terima kasih telah berlangganan! Kami sangat bersemangat untuk berbagi konten terbaru kami dengan Anda.

APA YANG DIHARAPKAN:
✓ Artikel baru dikirim ke kotak masuk Anda
✓ Konten eksklusif hanya untuk pelanggan
✓ {{ publish_frequency }} pembaruan
✓ Tidak ada spam, berlangganan kapan saja

MULAI MEMBACA - ARTIKEL POPULER:
{% for post in popular_posts %}
- {{ post.title }} ({{ post.reading_time }} menit membaca)
  {{ post.url }}
{% endfor %}

Eksplorasi semua artikel: {{ blog_url }}

Kelola langganan Anda: {{ preferences_url }}