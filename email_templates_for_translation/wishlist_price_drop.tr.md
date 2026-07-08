---
template_type: wishlist_price_drop
category: Wishlist
---

# Email Template: wishlist_price_drop

## Subject
🔥 Fiyat Düşüşü Uyarısı: {{ product_name }} şimdi {{ discount_percentage }}% indirimli!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          🔥 Fiyat Düşüşü Uyarısı!
        </mj-text>
        <mj-text font-size="18px" color="#047857" align="center">
          Favori Ürününüzde {{ discount_percentage }}% İndirim
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Harika Haber, {{ customer_name }}!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Favori ürünler listenizdeki bir ürünün fiyatı düştü! Bu fırsatı kaçırmayın.
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
            <mj-spacer height="10px" />
            <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              Eski Fiyat: <span style="text-decoration: line-through;">{{ original_price }}</span>
            </mj-text>
            <mj-text font-size="24px" font-weight="bold" color="#059669">
              Şimdiki Fiyat: {{ new_price }}
            </mj-text>
            <mj-text font-size="16px" font-weight="bold" color="#dc2626">
              {{ savings_amount }} Kaydedildi ({{ discount_percentage }}% İndirim)
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ product_url }}" background-color="#059669" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Şimdi Al & {{ discount_percentage }}% İndirimde Kal
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#991b1b" align="center">
              ⏰ <strong>Sınırlı Zaman:</strong> Bu indirim her zaman devam etmeyecek. Fiyatlar herhangi bir anda tekrar artabilir!
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Favori listeden kaldır: <a href="{{ remove_wishlist_url }}">Buraya tıklayın</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🔥 FİYAT DÜŞÜŞÜ UYARISI!
Favori Ürününüzde {{ discount_percentage }}% İndirim

Harika Haber, {{ customer_name }}!

Favori ürünler listenizdeki bir ürünün fiyatı düştü! Bu fırsatı kaçırmayın.

{{ product_name }}
Eski Fiyat: {{ original_price }}
Şimdi: {{ new_price }}
{{ savings_amount }} Kaydedildi ({{ discount_percentage }}% İndirim)

Şimdi al & {{ discount_percentage }}% indirimde kal: {{ product_url }}

⏰ SİNİRLİ ZAMAN: Bu indirim her zaman devam etmeyecek. Fiyatlar herhangi bir anda tekrar artabilir!

Favori listeden kaldır: {{ remove_wishlist_url }}