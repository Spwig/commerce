---
template_type: subscription_plan_upgraded
category: Subscriptions
---

# Email Template: subscription_plan_upgraded

## Subject
✓ Abonelik Planınız Geliştirildi!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          ✓ Plan Geliştirildi!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          {{ new_plan_name }} Hoş geldiniz
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Merhaba {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Abonelik planınız başarıyla geliştirildi. Artık {{ new_plan_name }} planının tüm avantajlarından yararlanabilirsiniz!
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Plan Değiştirme Detayları:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Önceki Plan:</strong> {{ old_plan_name }}<br/>
              <strong>Yeni Plan:</strong> {{ new_plan_name }}<br/>
              <strong>Geliştirildi:</strong> {{ upgrade_date }}<br/>
              <strong>Hemen Etkili</strong>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Yeni Özellikler:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ new_features }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Fatura Bilgileri:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Yeni Fiyat:</strong> {{ new_price }} / {{ billing_period }}<br/>
              <strong>Sonraki Fatura Tarihi:</strong> {{ next_billing_date }}<br/>
              {% if prorated_charge %}<strong>Günlük Prorated Ücret:</strong> {{ prorated_charge }}{% endif %}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if prorated_charge %}
        <mj-spacer height="20px" />
        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              💡 Bugün mevcut fatura döneminizin kalan kısmı için {{ prorated_charge }} ücreti alınmıştır.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ account_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Abonelikimi Görüntüle
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Sorularınız mı var? <a href="{{ support_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Destek ile iletişime geçin</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ PLAN GELİŞTİRİLDİ!

{{ new_plan_name }} Hoş geldiniz

Merhaba {{ customer_name }},

Abonelik planınız başarıyla geliştirildi. Artık {{ new_plan_name }} planının tüm avantajlarından yararlanabilirsiniz!

PLAN DEĞİŞİRME DETAYLARI:
- Önceki Plan: {{ old_plan_name }}
- Yeni Plan: {{ new_plan_name }}
- Geliştirildi: {{ upgrade_date }}
- Hemen Etkili

YENİ ÖZELLİKLER:
{{ new_features }}

FATURA BİLGİLERİ:
- Yeni Fiyat: {{ new_price }} / {{ billing_period }}
- Sonraki Fatura Tarihi: {{ next_billing_date }}
{% if prorated_charge %}- Günlük Prorated Ücret: {{ prorated_charge }}{% endif %}

{% if prorated_charge %}
💡 Bugün mevcut fatura döneminizin kalan kısmı için {{ prorated_charge }} ücreti alınmıştır.
{% endif %}

Abonelikimi Görüntüle: {{ account_url }}
Sorularınız mı var? Destek ile iletişime geçin: {{ support_url }}