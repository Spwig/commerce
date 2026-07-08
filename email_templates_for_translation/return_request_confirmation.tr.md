---
template_type: return_request_confirmation
category: Returns
---

# Email Template: return_request_confirmation

## Subject
İade Talebi Alındı - Sipariş #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#eff6ff' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1e40af' }}">
          İade Talebi Alındı
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1e40af' }}">
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
          Siparişinizi <strong>#{{ order_number }}</strong> için iade talebinizi aldık.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              İade Detayları:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Neden:</strong> {{ return_reason }}<br/>
              <strong>Ürünler:</strong> {{ items_count }} ürün(ler)<br/>
              <strong>Durum:</strong> {{ return_status }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Sonraki Adım Nedir?
        </mj-text>

        <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          1. Ekibimiz, iade talebinizi 24-48 saat içinde inceleyecektir<br/>
          2. Onaylandıktan sonra, iade kargo etiketi e-posta ile size gönderilecektir<br/>
          3. Ürünleri güvenli şekilde pakleyin ve iade etiketini ekleyin<br/>
          4. En yakın kargo noktasına paketi teslim edin<br/>
          5. Ürünleri aldığımızda ve incelediğimizde iade talebiniz işlenecektir
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Herhangi bir sorunuz varsa, lütfen bize ulaşmaktan çekinmeyin.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
İADE TALEBI ALINDI
Sipariş #{{ order_number }}

Merhaba {{ customer_name }},

Sipariş #{{ order_number }} için iade talebinizi aldık.

İADE DETAYLARI:
- Neden: {{ return_reason }}
- Ürünler: {{ items_count }} ürün(ler)
- Durum: {{ return_status }}

SONRAKİ ADIM NEDİR?
1. Ekibimiz, iade talebinizi 24-48 saat içinde inceleyecektir
2. Onaylandıktan sonra, iade kargo etiketi e-posta ile size gönderilecektir
3. Ürünleri güvenli şekilde pakleyin ve iade etiketini ekleyin
4. En yakın kargo noktasına paketi teslim edin
5. Ürünleri aldığımızda ve incelediğimizde iade talebiniz işlenecektir

Herhangi bir sorunuz varsa, lütfen bize ulaşmaktan çekinmeyin.