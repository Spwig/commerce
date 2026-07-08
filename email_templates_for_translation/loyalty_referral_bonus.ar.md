---
template_type: loyalty_referral_bonus
category: Loyalty Program
---

# Email Template: loyalty_referral_bonus

## Subject
🎁 نقاط مكافآت إضافية لمشاركة {{ referee_name }}!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          🎁 تم استلام مكافأة الإحالة!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          شكرًا لمشاركتك، {{ customer_name }}!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          أخبار سارة! {{ referee_name }} انضم فقط إلى برنامج الولاء الخاص بنا من خلال إحالتك، وحصلت على نقاط مكافآت إضافية!
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="18px" font-weight="bold" color="#065f46" align="center">
              حصلت على
            </mj-text>
            <mj-text font-size="36px" font-weight="bold" color="#047857" align="center">
              +{{ bonus_points }} نقطة
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              من خلال إحالة {{ referee_name }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          رصيدك المحدث:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>رصيد النقاط:</strong> {{ total_points }} نقطة<br/>
          <strong>مكافأة الإحالة:</strong> +{{ bonus_points }} نقطة<br/>
          <strong>الزملاء المدعوين:</strong> {{ total_referrals }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              استمر في المشاركة واستمر في الربح!
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              اربح {{ points_per_referral }} نقطة لكل زميل ينضم. لا يوجد حد أقصى!
            </mj-text>
            <mj-spacer height="15px" />
            <mj-button href="{{ referral_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
              شارك رابط إحالتك
            </mj-button>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ shop_url }}" background-color="#059669" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          ابدأ بالتسوق
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎁 تم استلام مكافأة الإحالة!

شكرًا لمشاركتك، {{ customer_name }}!

أخبار سارة! {{ referee_name }} انضم فقط إلى برنامج الولاء الخاص بنا من خلال إحالتك، وحصلت على نقاط مكافآت إضافية!

YOU EARNED:
+{{ bonus_points }} نقطة
من خلال إحالة {{ referee_name }}

YOUR UPDATED BALANCE:
- رصيد النقاط: {{ total_points }} نقطة
- مكافأة الإحالة: +{{ bonus_points }} نقطة
- الزملاء المدعوين: {{ total_referrals }}

KEEP SHARING, KEEP EARNING!
اربح {{ points_per_referral }} نقطة لكل زميل ينضم. لا يوجد حد أقصى!

شارك رابط إحالتك: {{ referral_url }}
ابدأ بالتسوق: {{ shop_url }}