---
template_type: loyalty_anniversary_bonus
category: Loyalty Program
---

# Email Template: loyalty_anniversary_bonus

## Subject
🎉 {{ years_as_member }} سنة مع {{ shop_name }} - شكرًا لك!

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="28px" align="center">🎉</mj-text>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          {{ years_as_member }} سنة معًا!
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          اليوم يُمثل {{ years_as_member }} سنة {{ years_as_member|pluralize }} منذ انضمامك إلى برنامج ولاءنا. شكرًا لك لأنك عضو مميز!
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="18px" font-weight="bold" color="#065f46" align="center">
              مكافأة الذكرى
            </mj-text>
            <mj-text font-size="36px" font-weight="bold" color="#047857" align="center">
              {{ bonus_points }} نقاط
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              تم إضافتها للاحتفاء بـ {{ years_as_member }} سنة {{ years_as_member|pluralize }}!
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          رحلتك لمدة {{ years_as_member }} سنة:
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
          اعرض لوحة معلومات الولاء الخاصة بك
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          شكرًا لك على {{ years_as_member }} سنة رائعة {{ years_as_member|pluralize }}!<br/>
          هنا يكمن المزيد من السنين القادمة 🥂
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 {{ years_as_member }} سنة معًا!

مرحباً {{ customer_name }},

اليوم يُمثل {{ years_as_member }} سنة {{ years_as_member|pluralize }} منذ انضمامك إلى برنامج ولاءنا. شكرًا لك لأنك عضو مميز!

مكافأة الذكرى:
{{ bonus_points }} نقاط
تم إضافتها للاحتفاء بـ {{ years_as_member }} سنة {{ years_as_member|pluralize }}!

رحلتك لمدة {{ years_as_member }} سنة:
- Member Since: {{ member_since }}
- Total Orders: {{ total_orders }}
- Points Earned: {{ lifetime_points }} points
- Current Tier: {{ loyalty_tier }}
- Total Savings: {{ total_savings }}

View your loyalty dashboard: {{ loyalty_dashboard_url }}

شكرًا لك على {{ years_as_member }} سنة رائعة {{ years_as_member|pluralize }}!
هنا يكمن المزيد من السنين القادمة 🥂