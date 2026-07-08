---
template_type: cart_abandoned_48h
category: Cart Recovery
---

# Email Template: cart_abandoned_48h

## Subject
Son şans! Sepetiniz 24 saat sonra sona erecek - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="#92400e" align="center">
          ⏰ Son Şans - Sepetiniz 24 Saat Sonra Sona Erecektir
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Kaçırmayın, {{ customer_name }}!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Bu son hatırlatmanızdır. Sepetiniz 24 saat sonra sona erecek ve bu ürünlerin daha fazla bekletilmesine izin vermeyebiliriz.
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
              {{ item.quantity }} × {{ item.price }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="20px" />

        <mj-text font-size="20px" font-weight="bold" align="right" color="{{ theme.color.text|default:'#1f2937' }}">
          Toplam: {{ cart_total }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ cart_url }}" background-color="#dc2626" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Siparişi Tamamlayınız, Aksi Taktirde Kaybedersiniz
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Sorularınız mı var? Ekibimiz yardımcı olmaktan memnuniyet duyar: <a href="{{ support_url }}">Destek ile İletişime Geçin</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⏰ SON ŞANS - SEPETİNİZ 24 SAAT SONRA SONA ERECEKTİR

Kaçırmayın, {{ customer_name }}!

Bu son hatırlatmanızdır. Sepetiniz 24 saat sonra sona erecek ve bu ürünlerin daha fazla bekletilmesine izin vermeyebiliriz.

SEPETİNİZ:
{% for item in cart_items %}
- {{ item.product_name }}
  {{ item.quantity }} × {{ item.price }}
{% endfor %}

Toplam: {{ cart_total }}

Siparişi tamamlayınız, aksi taktirde kaybedersiniz: {{ cart_url }}

Sorularınız mı var? Ekibimiz yardımcı olmaktan memnuniyet duyar: {{ support_url }}

---
Bu, sepet #{{ cart_id }} için son hatırlatmadır.