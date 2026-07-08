---
template_type: feed_sync_success
category: Product Feeds
---

# Email Template: feed_sync_success

## Subject
✓ {{ feed_name }} {{ platform_name }} ile senkronize edildi

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#065f46" align="center">
          ✓ Senkronizasyon Başarılı
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Beslemeye Başarıyla Senkronize Edildi
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ feed_name }} adlı beslemeniz {{ platform_name }} ile başarıyla senkronize edildi.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Senkronizasyon Detayı:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Beslemeye:</strong> {{ feed_name }}<br/>
              <strong>Platform:</strong> {{ platform_name }}<br/>
              <strong>Senkronize Edildi:</strong> {{ synced_at }}<br/>
              <strong>Senkronize Edilen Ürünler:</strong> {{ products_synced }}<br/>
              <strong>Süre:</strong> {{ sync_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if products_added > 0 or products_updated > 0 or products_removed > 0 %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Değişiklikler Özeti:
        </mj-text>
        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {% if products_added > 0 %}• {{ products_added }} ürün{{ products_added|pluralize }} eklendi<br/>{% endif %}
          {% if products_updated > 0 %}• {{ products_updated }} ürün{{ products_updated|pluralize }} güncellendi<br/>{% endif %}
          {% if products_removed > 0 %}• {{ products_removed }} ürün{{ products_removed|pluralize }} kaldırıldı<br/>{% endif %}
        </mj-text>
        {% endif %}

        {% if sync_warnings %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ Senkronizasyon Uyarıları
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ sync_warnings }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        {% if platform_url %}
        <mj-button href="{{ platform_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          {{ platform_name }} Üzerinde Görünüm
        </mj-button>
        <mj-spacer height="10px" />
        {% endif %}

        <mj-button href="{{ admin_feed_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Besleme Detaylarını Görüntüle
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ SENKRONİZASYON BAŞARILI

Beslemeye Başarıyla Senkronize Edildi

{{ feed_name }} adlı beslemeniz {{ platform_name }} ile başarıyla senkronize edildi.

SENKRONİZASYON DETAYI:
- Beslemeye: {{ feed_name }}
- Platform: {{ platform_name }}
- Senkronize Edildi: {{ synced_at }}
- Senkronize Edilen Ürünler: {{ products_synced }}
- Süre: {{ sync_duration }}

{% if products_added > 0 or products_updated > 0 or products_removed > 0 %}
DEĞİŞİKLİKLER ÖZETİ:
{% if products_added > 0 %}• {{ products_added }} ürün{{ products_added|pluralize }} eklendi{% endif %}
{% if products_updated > 0 %}• {{ products_updated }} ürün{{ products_updated|pluralize }} güncellendi{% endif %}
{% if products_removed > 0 %}• {{ products_removed }} ürün{{ products_removed|pluralize }} kaldırıldı{% endif %}
{% endif %}

{% if sync_warnings %}
⚠️ SENKRONİZASYON UYARILARI:
{{ sync_warnings }}
{% endif %}

{% if platform_url %}{{ platform_name }} Üzerinde Görünüm: {{ platform_url }}{% endif %}
Besleme Detaylarını Görüntüle: {{ admin_feed_url }}