---
template_type: loyalty_referral_bonus
category: Loyalty Program
---

# Email Template: loyalty_referral_bonus

## Subject
🎁 Bonus Poin untuk Merujuk {{ referee_name }}!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          🎁 Bonus Referensi Terkumpul!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Terima kasih telah Berbagi, {{ customer_name }}!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Berita baik! {{ referee_name }} baru saja bergabung dengan program loyalitas kami melalui rujukan Anda, dan Anda telah mendapatkan poin bonus!
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="18px" font-weight="bold" color="#065f46" align="center">
              Anda Mendapatkan
            </mj-text>
            <mj-text font-size="36px" font-weight="bold" color="#047857" align="center">
              +{{ bonus_points }} Poin
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              Untuk merujuk {{ referee_name }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Saldo Terbarui Anda:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>Saldo Poin:</strong> {{ total_points }} poin<br/>
          <strong>Bonus Referensi:</strong> +{{ bonus_points }} poin<br/>
          <strong>Teman yang Dirujuk:</strong> {{ total_referrals }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Terus Berbagi, Terus Mendapatkan!
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Dapatkan {{ points_per_referral }} poin untuk setiap teman yang bergabung. Tidak ada batas!
            </mj-text>
            <mj-spacer height="15px" />
            <mj-button href="{{ referral_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
              Bagikan Tautan Referensi Anda
            </mj-button>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ shop_url }}" background-color="#059669" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Mulai Berbelanja
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎁 BONUS REFERENSI TERKUMPUL!

Terima kasih telah Berbagi, {{ customer_name }}!

Berita baik! {{ referee_name }} baru saja bergabung dengan program loyalitas kami melalui rujukan Anda, dan Anda telah mendapatkan poin bonus!

ANDA MENDAPATKAN:
+{{ bonus_points }} Poin
Untuk merujuk {{ referee_name }}

SALDO TERBARU ANDA:
- Saldo Poin: {{ total_points }} poin
- Bonus Referensi: +{{ bonus_points }} poin
- Teman yang Dirujuk: {{ total_referrals }}

TERUS BERBAGI, TERUS MENDAPATKAN!
Dapatkan {{ points_per_referral }} poin untuk setiap teman yang bergabung. Tidak ada batas!

Bagikan tautan referensi Anda: {{ referral_url }}
Mulai berbelanja: {{ shop_url }}