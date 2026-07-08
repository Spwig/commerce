---
template_type: loyalty_referral_bonus
category: Loyalty Program
---

# Email Template: loyalty_referral_bonus

## Subject
🎁 {{ referee_name }} için Ekstra Puan Kazandınız!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          🎁 {{ referee_name }} için Ekstra Puan Kazandınız!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Paylaşım için teşekkürler, {{ customer_name }}!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Harika haber! {{ referee_name }} sizin referansınız aracılığıyla sadakat programımıza katıldı ve ekstra puan kazandınız!
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="18px" font-weight="bold" color="#065f46" align="center">
              Kazandığınız Puanlar
            </mj-text>
            <mj-text font-size="36px" font-weight="bold" color="#047857" align="center">
              +{{ bonus_points }} Puan
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              {{ referee_name }} için referans vererek
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Güncellenmiş Bakiyeniz:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>Puan Bakiyesi:</strong> {{ total_points }} puan<br/>
          <strong>Referans Puanı:</strong> +{{ bonus_points }} puan<br/>
          <strong>Referans Verilen Arkadaşlar:</strong> {{ total_referrals }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Paylaşmaya Devam Edin, Kazanmaya Devam Edin!
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Her bir arkadaşın katılması için {{ points_per_referral }} puan kazanın. Sınır yok!
            </mj-text>
            <mj-spacer height="15px" />
            <mj-button href="{{ referral_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
              Referans Bağlantınızı Paylaşın
            </mj-button>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ shop_url }}" background-color="#059669" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Alışverişe Başlayın
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎁 REFERANS PUANI KAZANDINIZ!

Paylaşım için teşekkürler, {{ customer_name }}!

Harika haber! {{ referee_name }} sizin referansınız aracılığıyla sadakat programımıza katıldı ve ekstra puan kazandınız!

KAZANDIĞINIZ PUANLAR:
+{{ bonus_points }} Puan
{{ referee_name }} için referans vererek

GÜNCELLEME BAKİYENİZ:
- Puan Bakiyesi: {{ total_points }} puan
- Referans Puanı: +{{ bonus_points }} puan
- Referans Verilen Arkadaşlar: {{ total_referrals }}

PAYLAŞMAYA DEVAM EDİN, KAZANMAYA DEVAM EDİN!
Her bir arkadaşın katılması için {{ points_per_referral }} puan kazanın. Sınır yok!

Referans bağlantınızı paylaşın: {{ referral_url }}
Alışverişe başlayın: {{ shop_url }}