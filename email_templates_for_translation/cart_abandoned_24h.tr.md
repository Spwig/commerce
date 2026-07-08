---
template_type: cart_abandoned_24h
category: Cart Recovery
---

# Email Template: cart_abandoned_24h

## Subject
Hâlâ ilgileniyor musunuz? Sepetiniz yakında sona erecek - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Sepetinizdeki {{ cart_item_count }} ürün{{ cart_item_count|pluralize }} {{ cart_item_count|pluralize:'is,are' }} hâlâ bekliyor
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Merhaba {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Siparişinizi bekliyoruz, ancak bu ürünler ömürlerine kadar beklemeyecek. Onlar giden önce siparişinizi tamamlayın!
        </mj-text>

        <mj-spacer height="20px" />

        {% for item in cart_items %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column width="30%">
            <mj-image src="{{ item.product_image }}" alt="{{ item.product_name }}" border-radius="4px" />
          </mj-column>
          <mj-column width="70%">
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ item.product_name }}
            </mj-text>
            <mj-text color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              Adet: {{ item.quantity }} × {{ item.price }}
            </mj-text>
            {% if item.low_stock %}
            <mj-text color="#dc2626" font-size="13px">
              ⚠️ Sadece {{ item.stock_remaining }} adet mevcut!
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="20px" />

        <mj-text font-size="18px" font-weight="bold" align="right" color="{{ theme.color.text|default:'#1f2937' }}">
          Toplam: {{ cart_total }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ cart_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Siparişinizi Şimdi Tamamlayin
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              ✓ {{ free_shipping_threshold }}'dan yüksek siparişlerde ücretsiz kargo<br/>
              ✓ 30 günlük para iadesi garantisi<br/>
              ✓ Güvenli ödeme
            </mj-text>
          </mj-column>
        </mj-section>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Sepetinizdeki {{ cart_item_count }} ürün{{ cart_item_count|pluralize }} {{ cart_item_count|pluralize:'is,are' }} hâlâ bekliyor

Merhaba {{ customer_name }},

Siparişinizi bekliyoruz, ancak bu ürünler ömürlerine kadar beklemeyecek. Onlar giden önce siparişinizi tamamlayın!

SEPETİNİZ:
{% for item in cart_items %}
- {{ item.product_name }}
  Adet: {{ item.quantity }} × {{ item.price }}
  {% if item.low_stock %}⚠️ Sadece {{ item.stock_remaining }} adet mevcut!{% endif %}
{% endfor %}

Toplam: {{ cart_total }}

Siparişinizi şimdi tamamlayın: {{ cart_url }}

Neden bize alışveriş yapmalısınız:
✓ {{ free_shipping_threshold }}'dan yüksek siparişlerde ücretsiz kargo
✓ 30 günlük para iadesi garantisi
✓ Güvenli ödeme

---

Sepet hatırlatmalarını durdurmak için ziyaret edin: {{ preferences_url }}