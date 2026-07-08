---
template_type: shipping_exception
category: Shipping
---

# Email Template: shipping_exception

## Subject
Gönderim Anomalisi - #{{ order_number }} Siparişi Dikkat Gerekiyor

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Gönderim Anomalisi
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Merhaba {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Siparişinizle ilgili bir istisna durumu olduğunu bildirmek için bu maili yazıyoruz. Bu sorunu mümkün olduğu kadar hızlıca çözmek için çalışıyoruz.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#92400e">
              İstisna Detayı:
            </mj-text>
            <mj-text color="#92400e">
              <strong>İstisna Türü:</strong> {{ exception_type }}<br/>
              <strong>Açıklama:</strong> {{ exception_description }}<br/>
              <strong>Oluştu:</strong> {{ exception_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Sipariş Bilgisi:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Sipariş Numarası:</strong> {{ order_number }}<br/>
              <strong>İzleme Numarası:</strong> {{ tracking_number }}<br/>
              <strong>Kurye:</strong> {{ carrier_name }}<br/>
              <strong>Mevcut Konum:</strong> {{ current_location }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Sonraki Adım Nedir?
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          {{ resolution_steps }}
        </mj-text>

        <mj-spacer height="20px" />

        {% if action_required %}
        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              ⚠️ Yapılacak İşlem:
            </mj-text>
            <mj-text color="#7f1d1d">
              {{ action_required_description }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="20px" />
        {% endif %}

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Siparişinizi Takip Et
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Destekle İletişime Geç
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ GÖNDERİM İSTİSNASI

Merhaba {{ customer_name }},

Siparişinizle ilgili bir istisna durumu olduğunu bildirmek için bu maili yazıyoruz. Bu sorunu mümkün olduğu kadar hızlıca çözmek için çalışıyoruz.

İSTİSNA DETAYLARI:
- İstisna Türü: {{ exception_type }}
- Açıklama: {{ exception_description }}
- Oluştu: {{ exception_date }}

SİPARİŞ BİLGİSİ:
- Sipariş Numarası: {{ order_number }}
- İzleme Numarası: {{ tracking_number }}
- Kurye: {{ carrier_name }}
- Mevcut Konum: {{ current_location }}

SONRAKİ ADIM NEDİR?
{{ resolution_steps }}

{% if action_required %}
⚠️ YAPILACAK İŞLEM:
{{ action_required_description }}
{% endif %}

Siparişinizi takip edin: {{ tracking_url }}
Destekle iletişime geçin: {{ support_url }}