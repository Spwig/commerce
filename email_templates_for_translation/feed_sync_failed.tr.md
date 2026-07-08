---
template_type: feed_sync_failed
category: Product Feeds
---

# Email Template: feed_sync_failed

## Subject
❌ {{ feed_name }} ile {{ platform_name }} senkronizasyonu başarısız oldu

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ❌ Senkronizasyon Başarısız Oldu
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Senkronizasyon Hatası
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ feed_name }} ile {{ platform_name }} senkronizasyonu başarısız oldu.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Hata Detayları:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Feed:</strong> {{ feed_name }}<br/>
              <strong>Platform:</strong> {{ platform_name }}<br/>
              <strong>Failed At:</strong> {{ failed_at }}<br/>
              <strong>Error Code:</strong> {{ error_code }}
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

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Ortak Nedenler:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Geçersiz API kimlik doğrulama bilgileri veya zaman aşımı vermiş token<br/>
          • Ağ bağlantı sorunları<br/>
          • Platform API oran sınırları aşıldı<br/>
          • Feed formatı platform gereksinimlerini karşılamıyor
        </mj-text>

        {% if recommended_action %}
        <mj-spacer height="30px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              Önerilen Eylem
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ recommended_action }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ retry_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Tekrar Senkronize Et
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ admin_feed_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Feed Ayarlarını Kontrol Et
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❌ SENKRONİZASYON BAŞARISIZ

Senkronizasyon Hatası

{{ feed_name }} ile {{ platform_name }} senkronizasyonu başarısız oldu.

HATA DETAYLARI:
- Feed: {{ feed_name }}
- Platform: {{ platform_name }}
- Hata Zamanı: {{ failed_at }}
- Hata Kodu: {{ error_code }}

HATA MESAJI:
{{ error_message }}

ORTAK NEDENLER:
• Geçersiz API kimlik doğrulama bilgileri veya zaman aşımı vermiş token
• Ağ bağlantı sorunları
• Platform API oran sınırları aşıldı
• Feed formatı platform gereksinimlerini karşılamıyor

{% if recommended_action %}
ÖNERİLEN EYLEM:
{{ recommended_action }}
{% endif %}

Senkronizasyonu tekrar deneyin: {{ retry_url }}
Feed ayarlarını kontrol edin: {{ admin_feed_url }}