---
template_type: loyalty_anniversary_bonus
category: Loyalty Program
---

# Email Template: loyalty_anniversary_bonus

## Subject
🎉 {{ years_as_member }} Tahun dengan {{ shop_name }} - Terima Kasih!

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="28px" align="center">🎉</mj-text>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          {{ years_as_member }} Tahun Bersama!
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hari ini menandai {{ years_as_member }} tahun{{ years_as_member|pluralize }} sejak Anda bergabung dengan program loyalitas kami. Terima kasih telah menjadi anggota yang sangat berharga!
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="18px" font-weight="bold" color="#065f46" align="center">
              Bonus Ulang Tahun
            </mj-text>
            <mj-text font-size="36px" font-weight="bold" color="#047857" align="center">
              {{ bonus_points }} Poin
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              Ditambahkan untuk merayakan {{ years_as_member }} tahun{{ years_as_member|pluralize }}!
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Perjalanan {{ years_as_member }}-Tahun Anda:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          <strong>Member Since:</strong> {{ member_since }}<br/>
          <strong>Total Orders:</strong> {{ total_orders }}<br/>
          <strong>Points Earned:</strong> {{ lifetime_points }} points<br/>
          <strong>Current Tier:</strong> {{ loyalty_tier }}<br/>
          <strong>Total Savings:</strong> {{ total_savings }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ loyalty_dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Lihat Dashboard Loyalitas Anda
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Terima kasih untuk {{ years_as_member }} tahun luar biasa{{ years_as_member|pluralize }}!<br/>
          Selamat untuk banyak lebih dari ini 🥂
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 {{ years_as_member }} TAHUN {{ years_as_member|pluralize|upper }} BERSAMA!

Hi {{ customer_name }},

Hari ini menandai {{ years_as_member }} tahun{{ years_as_member|pluralize }} sejak Anda bergabung dengan program loyalitas kami. Terima kasih telah menjadi anggota yang sangat berharga!

BONUS ULANG TAHUN:
{{ bonus_points }} Poin
Ditambahkan untuk merayakan {{ years_as_member }} tahun{{ years_as_member|pluralize }}!

PERJALANAN {{ years_as_member }}-TAHUN ANDA:
- Member Since: {{ member_since }}
- Total Orders: {{ total_orders }}
- Points Earned: {{ lifetime_points }} points
- Current Tier: {{ loyalty_tier }}
- Total Savings: {{ total_savings }}

Lihat dashboard loyalitas Anda: {{ loyalty_dashboard_url }}

Terima kasih untuk {{ years_as_member }} tahun luar biasa{{ years_as_member|pluralize }}!
Selamat untuk banyak lebih dari ini 🥂