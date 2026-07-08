---
template_type: loyalty_birthday_bonus
category: Loyalty Program
---

# Email Template: loyalty_birthday_bonus

## Subject
🎂 Selamat Ulang Tahun {{ customer_name }}! Berikut adalah hadiah khusus dari {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="32px" align="center">🎂🎉🎁</mj-text>
        <mj-text font-size="26px" font-weight="bold" color="#92400e" align="center">
          Selamat Ulang Tahun!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Selamat Ulang Tahun, {{ customer_name }}!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Untuk memperingati hari istimewa Anda, kami telah menambahkan {{ bonus_points }} poin bonus ke akun loyalitas Anda!
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#dcfce7" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="18px" font-weight="bold" color="#065f46" align="center">
              Hadiah Ulang Tahun Anda
            </mj-text>
            <mj-text font-size="36px" font-weight="bold" color="#047857" align="center">
              {{ bonus_points }} Poin
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              Telah ditambahkan ke akun Anda!
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Akun Loyalitas Anda:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>Saldo Poin:</strong> {{ total_points }} poin<br/>
          <strong>Tier Saat Ini:</strong> {{ loyalty_tier }}<br/>
          <strong>Bonus Ulang Tahun:</strong> +{{ bonus_points }} poin
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ shop_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Mulai Berbelanja & Gunakan Poin Anda
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Selamat ulang tahun yang luar biasa! 🎉<br/>
          - Tim {{ shop_name }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎂🎉🎁 SELAMAT ULANG TAHUN!

Selamat Ulang Tahun, {{ customer_name }}!

Untuk memperingati hari istimewa Anda, kami telah menambahkan {{ bonus_points }} poin bonus ke akun loyalitas Anda!

HADIAH ULANG TAHUN ANDA:
{{ bonus_points }} Poin
Telah ditambahkan ke akun Anda!

AKUN LOYALITAS ANDA:
- Saldo Poin: {{ total_points }} poin
- Tier Saat Ini: {{ loyalty_tier }}
- Bonus Ulang Tahun: +{{ bonus_points }} poin

Mulai berbelanja & gunakan poin Anda: {{ shop_url }}

Selamat ulang tahun yang luar biasa! 🎉
- Tim {{ shop_name }}