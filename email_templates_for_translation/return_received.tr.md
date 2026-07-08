---
template_type: return_received
category: Returns
---

# Email Template: return_received

## Subject
İade Alma - Sipariş #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#eff6ff' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.primary|default:'#1d4ed8' }}">
          İade Alma
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.primary|default:'#1d4ed8' }}">
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
          Siparişinize ait iade edilen ürünlerimizi aldık.
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>Şimdi ne olacak:</strong>
        </mj-text>

        <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          1. Ekibimiz, iade edilen ürünleri 2-3 iş günü içinde inceleyecektir<br/>
          2. Ürünlerin orijinal durumda olduğundan emin olacağız<br/>
          3. İnceleme tamamlandıktan sonra iade talebinizi işleme koyacağız<br/>
          4. İade işleme koyulduktan sonra size onay e-postası göndereceğiz
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          İade, orijinal ödeme yönteminize kredi olarak yansıtılacak ve hesabınıza 5-10 iş günü içinde görünür olabilir.
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Sabır gösterdiğiniz için teşekkür ederiz!
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
İade Alma - Sipariş #{{ order_number }}

Merhaba {{ customer_name }},

Siparişinize ait iade edilen ürünlerimizi aldık.

Şimdi ne olacak:
1. Ekibimiz, iade edilen ürünleri 2-3 iş günü içinde inceleyecektir
2. Ürünlerin orijinal durumda olduğundan emin olacağız
3. İnceleme tamamlandıktan sonra iade talebinizi işleme koyacağız
4. İade işleme koyulduktan sonra size onay e-postası göndereceğiz

İade, orijinal ödeme yönteminize kredi olarak yansıtılacak ve hesabınıza 5-10 iş günü içinde görünür olabilir.

Sabır gösterdiğiniz için teşekkür ederiz!