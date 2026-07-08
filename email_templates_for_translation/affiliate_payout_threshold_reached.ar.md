---
template_type: affiliate_payout_threshold_reached
category: Affiliate Program
---

# Email Template: affiliate_payout_threshold_reached

## Subject
💰 لقد وصلت إلى حد سحب الأرباح المطلوب!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          💰 تم الوصول إلى حد سحب الأرباح!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          أخبار سارة!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          مرحباً {{ affiliate_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          تهانينا! لقد وصل رصيدك كشريك تسويق إلى الحد الأدنى لسحب الأرباح. يمكنك الآن طلب سحب الأرباح.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              رصيدك:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>الرصيد المتوفر:</strong> <span style="font-size: 24px; font-weight: bold; color: #059669;">{{ available_balance }}</span><br/>
              <strong>الحد الأدنى لسحب الأرباح:</strong> {{ minimum_payout }}<br/>
              <strong>المجاملات المعلقة:</strong> {{ pending_balance }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ماذا بعد:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • اطلب سحب الأرباح من لوحة التحكم الخاصة بك كشريك تسويق<br/>
          • تتم معالجة الدفعات {{ payout_schedule }}<br/>
          • سيتم إرسال الأموال عبر {{ payment_method }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ request_payout_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          اطلب سحب الأرباح
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ portal_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          اعرض لوحة التحكم
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
💰 تم الوصول إلى حد سحب الأرباح!

أخبار سارة!

مرحباً {{ affiliate_name }},

تهانينا! لقد وصل رصيدك كشريك تسويق إلى الحد الأدنى لسحب الأرباح. يمكنك الآن طلب سحب الأرباح.

رصيدك:
- الرصيد المتوفر: {{ available_balance }}
- الحد الأدنى لسحب الأرباح: {{ minimum_payout }}
- المجاملات المعلقة: {{ pending_balance }}

ماذا بعد:
• اطلب سحب الأرباح من لوحة التحكم الخاصة بك كشريك تسويق
• تتم معالجة الدفعات {{ payout_schedule }}
• سيتم إرسال الأموال عبر {{ payment_method }}

طلب سحب الأرباح: {{ request_payout_url }}
عرض لوحة التحكم: {{ portal_url }}