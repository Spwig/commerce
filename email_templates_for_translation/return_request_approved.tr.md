---
template_type: return_request_approved
category: Returns
---

# Email Template: return_request_approved

## Subject
İade Talebiniz Onaylandı - Sipariş #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f0fdf4' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#166534' }}">
          İade Onaylandı
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#166534' }}">
          Sipariş #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Merhaba {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Siparişinize ait <strong>#{{ order_number }}</strong> iade talebiniz onaylanmıştır.
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>Sonraki Adımlar:</strong>
        </mj-text>

        <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          1. Aşağıdaki iade etiketini indirin ve yazdırın<br/>
          2. Mümkünse ürünlerin orijinal ambalajında güvenli şekilde paklayınız<br/>
          3. Paketin dış yüzeyine iade etiketini yapıştırın<br/>
          4. En yakın kargo noktasına teslim edin
        </mj-text>

        {% if return_label_url %}
        <mj-spacer height="20px" />
        <mj-button href="{{ return_label_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          İade Etiketi İndir
        </mj-button>
        {% endif %}

        {% if return_tracking_number %}
        <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>İade Takip Numarası:</strong> {{ return_tracking_number }}
        </mj-text>
        {% endif %}

        <mj-section background-color="{{ theme.color.surface|default:'#fffbeb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#92400e' }}">
              <strong>Önemli:</strong> Lütfen iadeyi 7 gün içinde gönderin, böylece iade ücretinizin hızlıca işlenmesi sağlanır.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          İadeyi aldığımızda ve incelediğimizde, iade ücretinizi orijinal ödeme yönteminize geri ödeceğiz.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
İade Onaylandı - Sipariş #{{ order_number }}

Merhaba {{ customer_name }},

Sipariş #{{ order_number }} iade talebiniz onaylanmıştır.

Sonraki Adımlar:
1. İade etiketini indirin ve yazdırın
2. Mümkünse ürünlerin orijinal ambalajında güvenli şekilde paklayın
3. Paketin dış yüzeyine iade etiketini yapıştırın
4. En yakın kargo noktasına teslim edin

{% if return_label_url %}İade etiketi: {{ return_label_url }}{% endif %}
{% if return_tracking_number %}İade Takip Numarası: {{ return_tracking_number }}{% endif %}

Önemli: Lütfen iadeyi 7 gün içinde gönderin, böylece iade ücretinizin hızlıca işlenmesi sağlanır.

İadeyi aldığımızda ve incelediğimizde, iade ücretinizi orijinal ödeme yönteminize geri ödeceğiz.