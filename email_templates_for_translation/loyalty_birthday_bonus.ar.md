---
template_type: loyalty_birthday_bonus
category: Loyalty Program
---

# Email Template: loyalty_birthday_bonus

## Subject
🎂 عيد ميلاد سعيد {{ customer_name }}! إليك هدية خاصة من {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="32px" align="center">🎂🎉🎁</mj-text>
        <mj-text font-size="26px" font-weight="bold" color="#92400e" align="center">
          عيد ميلاد سعيد!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          عيد ميلاد سعيد، {{ customer_name }}!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          للاحتفال بيومك الخاص، أضفنا {{ bonus_points }} نقطة مكافأة إلى حساب الولاء الخاص بك!
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#dcfce7" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="18px" font-weight="bold" color="#065f46" align="center">
              هدية عيد ميلادك
            </mj-text>
            <mj-text font-size="36px" font-weight="bold" color="#047857" align="center">
              {{ bonus_points }} نقطة
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              تم إضافتها إلى حسابك!
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          حساب الولاء الخاص بك:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>رصيد النقاط:</strong> {{ total_points }} نقطة<br/>
          <strong>الدرجة الحالية:</strong> {{ loyalty_tier }}<br/>
          <strong>المكافأة الخاصة بعيد الميلاد:</strong> +{{ bonus_points }} نقطة
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ shop_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          ابدأ الشراء واستخدم نقاطك
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          عيد ميلاد ممتع! 🎉<br/>
          - فريق {{ shop_name }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎂🎉🎁 عيد ميلاد سعيد!

عيد ميلاد سعيد، {{ customer_name }}!

للاحتفال بيومك الخاص، أضفنا {{ bonus_points }} نقطة مكافأة إلى حساب الولاء الخاص بك!

هدية عيد ميلادك:
{{ bonus_points }} نقطة
تم إضافتها إلى حسابك!

حساب الولاء الخاص بك:
- رصيد النقاط: {{ total_points }} نقطة
- الدرجة الحالية: {{ loyalty_tier }}
- المكافأة الخاصة بعيد الميلاد: +{{ bonus_points }} نقطة

ابدأ الشراء واستخدم نقاطك: {{ shop_url }}

عيد ميلاد ممتع! 🎉
- فريق {{ shop_name }}