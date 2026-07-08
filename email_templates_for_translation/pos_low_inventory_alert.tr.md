---
template_type: pos_low_inventory_alert
category: POS
---

# Email Template: pos_low_inventory_alert

## Subject
📦 Stok Seviyesi Düşük Uyarısı: {{ product_count }} ürün {{ product_count|pluralize }} {{ location_name }} de stokta azalmakta

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          📦 Stok Seviyesi Düşük Uyarısı
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Stok Seviyesi Düşük
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ product_count }} ürün {{ product_count|pluralize }} {{ product_count|pluralize:'is,are' }} {{ location_name }} de stokta azalmakta.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Uyarı Ayrıntıları:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Location:</strong> {{ location_name }}<br/>
              <strong>Products Affected:</strong> {{ product_count }}<br/>
              <strong>Detected:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Stok Seviyesi Düşük Ürünler:
        </mj-text>

        {% for item in low_stock_items %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ item.product_name }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              {% if item.variant_name %}<strong>Variant:</strong> {{ item.variant_name }}<br/>{% endif %}
              <strong>Current Stock:</strong> <span style="color: #dc2626; font-weight: bold;">{{ item.current_stock }}</span><br/>
              <strong>Reorder Point:</strong> {{ item.reorder_point }}<br/>
              <strong>SKU:</strong> {{ item.sku }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Önerilen Eylemler:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Stokta azalmakta olan ürün için satın alma emri oluşturun<br/>
          • Diğer konumlardan stok aktarın<br/>
          • Gerekirse yeniden sipariş noktası güncelleyin<br/>
          • Par seviyelerini ayarlamayı göz önünde bulundurun
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ inventory_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Stokları Görüntüle
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ purchase_orders_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Satın Alma Emri Oluştur
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📦 STOK SEVİYESİ DÜŞÜK UYARISI

Stok Seviyesi Düşük

{{ product_count }} ürün {{ product_count|pluralize }} {{ product_count|pluralize:'is,are' }} {{ location_name }} de stokta azalmakta.

UYARI AYRINTILARI:
- Konum: {{ location_name }}
- Etkilenen Ürünler: {{ product_count }}
- Tespit Edildi: {{ detected_at }}

STOK SEVİYESİ DÜŞÜK ÜRÜNLER:
{% for item in low_stock_items %}
{{ item.product_name }}
{% if item.variant_name %}Variant: {{ item.variant_name }}{% endif %}
Mevcut Stok: {{ item.current_stock }}
Yeniden Sipariş Noktası: {{ item.reorder_point }}
SKU: {{ item.sku }}

{% endfor %}

ÖNERİLEN EYLEMLER:
• Stokta azalmakta olan ürün için satın alma emri oluşturun
• Diğer konumlardan stok aktarın
• Gerekirse yeniden sipariş noktası güncelleyin
• Par seviyelerini ayarlamayı göz önünde bulundurun

Stokları Görüntüle: {{ inventory_url }}
Satın Alma Emri Oluştur: {{ purchase_orders_url }}