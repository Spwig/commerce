---
template_type: wishlist_item_added_confirmation
category: Wishlist
---

# Email Template: wishlist_item_added_confirmation

## Subject
✓ {{ product_name }} favori listenize eklendi - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ❤️ Favori Listenize Eklenen!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Merhaba {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ product_name }} ürünü başarıyla favori listenize eklendi. Size yardımcı olmaktan memnuniyet duyarız!
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column width="35%">
            <mj-image src="{{ product_image }}" alt="{{ product_name }}" border-radius="8px" />
          </mj-column>
          <mj-column width="65%">
            <mj-text font-weight="bold" font-size="18px" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ product_name }}
            </mj-text>
            <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}">
              {{ product_price }}
            </mj-text>
            {% if product_in_stock %}
            <mj-text font-size="13px" color="#059669">
              ✓ Stokta
            </mj-text>
            {% else %}
            <mj-text font-size="13px" color="#dc2626">
              ⚠️ Stokta Yok - Geri döndüğünde sizi bilgilendiririz!
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              💡 <strong>Sizi bilgilendireceğimiz konular:</strong><br/>
              • Fiyat düşüklükleri<br/>
              • Stokta tekrar mevcut olma bildirimleri<br/>
              • Sınırlı süreli satışlar
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ wishlist_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Favori Listemi Görüntüle
        </mj-button>

        {% if product_in_stock %}
        <mj-spacer height="10px" />
        <mj-button href="{{ product_url }}" background-color="#059669" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Şimdi Satın Al
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❤️ FAVORİ LİSTENİZE EKLENDİ!

Merhaba {{ customer_name }},

{{ product_name }} ürünü başarıyla favori listenize eklendi. Size yardımcı olmaktan memnuniyet duyarız!

{{ product_name }}
Fiyat: {{ product_price }}
{% if product_in_stock %}✓ Stokta{% else %}⚠️ Stokta Yok - Geri döndüğünde sizi bilgilendiririz!{% endif %}

💡 SİZİ BİLGİLENDİRMEK İSTEDİĞİMİZ KONULAR:
• Fiyat düşüklükleri
• Stokta tekrar mevcut olma bildirimleri
• Sınırlı süreli satışlar

Favori listeni gör: {{ wishlist_url }}
{% if product_in_stock %}Şimdi satın al: {{ product_url }}{% endif %}