---
template_type: affiliate_high_commission_alert
category: Affiliate Program
---

# Email Template: affiliate_high_commission_alert

## Subject
⚠️ {{ affiliate_name }} Tarafından Anormal Komisyon Aktivitesi Tespit Edildi

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Yüksek Komisyon Uyarısı
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Anormal Aktivite Tespit Edildi
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ affiliate_name }} tarafından anormal olarak yüksek bir komisyon kazanıldı. Bu, dolandırıcılık önleme için gözden geçirilmelidir.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Uyarı Detayı:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Affiliate:</strong> {{ affiliate_name }} ({{ affiliate_id }})<br/>
              <strong>Komisyon Tutarı:</strong> <span style="font-weight: bold; color: #dc2626;">{{ commission_amount }}</span><br/>
              <strong>Sipariş Değeri:</strong> {{ order_value }}<br/>
              <strong>Sipariş Kimliği:</strong> {{ order_number }}<br/>
              <strong>Tespit Edildi:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Neden İşaretlendi:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ flag_reason }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Önerilen Eylemler:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Sipariş detaylarını doğrulamak için incele<br/>
          • Affiliate'in referans geçmişini kontrol et<br/>
          • Müşterinin referans verenle bağlantılı olup olmadığını doğrula<br/>
          • Yönetici panelinde komisyonu onayla veya reddet
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ review_commission_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Komisyonu İncele
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ affiliate_details_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Affiliate Detayı Görüntüle
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Bu komisyon onaylanana kadar gözden geçiriliyor ve ödenmeyecektir.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ YÜKSEK KOMİSYON UYARISI

Anormal Aktivite Tespit Edildi

{{ affiliate_name }} tarafından anormal olarak yüksek bir komisyon kazanıldı. Bu, dolandırıcılık önleme için gözden geçirilmelidir.

UYARI DETAYLARI:
- Affiliate: {{ affiliate_name }} ({{ affiliate_id }})
- Komisyon Tutarı: {{ commission_amount }}
- Sipariş Değeri: {{ order_value }}
- Sipariş Kimliği: {{ order_number }}
- Tespit Edildi: {{ detected_at }}

NEDEN İŞARETLİYDİ:
{{ flag_reason }}

ÖNERİLEN EYLEMLER:
• Sipariş detaylarını doğrulamak için incele
• Affiliate'in referans geçmişini kontrol et
• Müşterinin referans verenle bağlantılı olup olmadığını doğrula
• Yönetici panelinde komisyonu onayla veya reddet

Komisyonu incele: {{ review_commission_url }}
Affiliate detaylarını görüntüle: {{ affiliate_details_url }}

Bu komisyon onaylanana kadar gözden geçiriliyor ve ödenmeyecektir.