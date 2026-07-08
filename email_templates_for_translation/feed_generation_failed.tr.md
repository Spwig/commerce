---
template_type: feed_generation_failed
category: Product Feeds
---

# Email Template: feed_generation_failed

## Subject
❌ {{ feed_name }} için besleme üretimi başarısız oldu

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ❌ Besleme Üretimi Başarısız Oldu
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Üretim Hatası
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ feed_name }} ürün beslemesi, bir hata nedeniyle üretilemedi.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Hata Detayı:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Besleme:</strong> {{ feed_name }}<br/>
              <strong>Başarısız Oldu:</strong> {{ failed_at }}<br/>
              <strong>Hata Kodu:</strong> {{ error_code }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Hata Mesajı:
        </mj-text>

        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" font-family="monospace" color="#991b1b" line-height="1.6">
              {{ error_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if error_log %}
        <mj-spacer height="20px" />
        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>Hata Günlüğü:</strong><br/>
          <code style="font-size: 12px; color: #6b7280;">{{ error_log|truncatewords:30 }}</code>
        </mj-text>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Yaygın Nedenler:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Gerekli ürün verisi eksik (başlık, fiyat, resim)<br/>
          • Geçersiz ürün verisi formatı<br/>
          • Veritabanı bağlantı sorunları<br/>
          • Yetersiz disk alanı veya bellek
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ retry_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Üretimi Tekrar Dene
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ admin_feed_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Besleme Ayarlarını Görüntüle
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Sorun devam ederse, {{ error_code }} hata koduyla destek ile iletişime geçin.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❌ BESLEME ÜRETİMİ BAŞARISIZ OLDU

Üretim Hatası

{{ feed_name }} ürün beslemesi, bir hata nedeniyle üretilemedi.

HATA DETAYLARI:
- Besleme: {{ feed_name }}
- Başarısız Oldu: {{ failed_at }}
- Hata Kodu: {{ error_code }}

HATA MESAJI:
{{ error_message }}

{% if error_log %}
HATA GÜNLÜĞÜ:
{{ error_log|truncatewords:30 }}
{% endif %}

YAYGIN NEDENLER:
• Gerekli ürün verisi eksik (başlık, fiyat, resim)
• Geçersiz ürün verisi formatı
• Veritabanı bağlantı sorunları
• Yetersiz disk alanı veya bellek

Üretimi tekrar dene: {{ retry_url }}
Besleme ayarlarını görüntüle: {{ admin_feed_url }}

Sorun devam ederse, {{ error_code }} hata koduyla destek ile iletişime geçin.