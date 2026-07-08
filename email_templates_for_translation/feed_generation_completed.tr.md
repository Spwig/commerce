---
template_type: feed_generation_completed
category: Product Feeds
---

# Email Template: feed_generation_completed

## Subject
✓ {{ feed_name }} ürün beslemesi oluşturuldu

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#065f46" align="center">
          ✓ Besleme Başarıyla Oluşturuldu
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Ürün Beslemesi Hazır
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ feed_name }} ürün beslemeniz başarıyla oluşturuldu ve kullanıma hazırdır.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Besleme Ayrıntıları:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Besleme:</strong> {{ feed_name }}<br/>
              <strong>Format:</strong> {{ feed_format }}<br/>
              <strong>Ürünler:</strong> {{ product_count }}<br/>
              <strong>Oluşturuldu:</strong> {{ generated_at }}<br/>
              <strong>Dosya Boyutu:</strong> {{ file_size }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if warnings_count > 0 %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj:text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ {{ warnings_count }} Uyarı{{ warnings_count|pluralize }}
            </mj:text>
            <mj-text font-size="14px" color="#92400e">
              Bazı ürünlerin veri kalitesi sorunları vardır. Yönetici panelinde uyarıları inceleyin.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Besleme URL'si:
        </mj-text>

        <mj-text font-size="13px" font-family="monospace" color="{{ theme.color.text_secondary|default:'#6b7280' }}" padding="10px" background-color="#f3f4f6">
          {{ feed_url }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ download_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Beslemeyi İndir
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ admin_feed_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Yönetici Panelinde Görüntüle
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ BESLEME BAŞARIYLA OLUŞTURULDU

Ürün Beslemesi Hazır

{{ feed_name }} ürün beslemeniz başarıyla oluşturuldu ve kullanıma hazırdır.

BESLEME AYRINTILARI:
- Besleme: {{ feed_name }}
- Format: {{ feed_format }}
- Ürünler: {{ product_count }}
- Oluşturuldu: {{ generated_at }}
- Dosya Boyutu: {{ file_size }}

{% if warnings_count > 0 %}
⚠️ {{ warnings_count }} UYARI{{ warnings_count|pluralize|upper }}:
Bazı ürünlerin veri kalitesi sorunları vardır. Yönetici panelinde uyarıları inceleyin.
{% endif %}

BESLEME URL'Sİ:
{{ feed_url }}

Beslemeyi İndir: {{ download_url }}
Yönetici Panelinde Görüntüle: {{ admin_feed_url }}