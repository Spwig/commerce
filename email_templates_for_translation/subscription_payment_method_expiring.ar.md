---
template_type: subscription_payment_method_expiring
category: Subscriptions
---

# Email Template: subscription_payment_method_expiring

## Subject
💳 التحديث المطلوب: وسيلة الدفع قريباً من الانتهاء - {{ shop_name }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          💳 وسيلة الدفع قريباً من الانتهاء
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          الإجراء المطلوب لتجنب انقطاع الاشتراك
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Warning Card -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-wrapper background-color="#fff7ed" padding="30px" border="2px solid {{ theme.color.warning|default:'#f59e0b' }}" border-radius="12px">
          <mj-section background-color="transparent">
            <mj-column>
              <mj-text font-size="20px" font-weight="600" color="#9a3412" align="center" padding-bottom="15px">
                وسيلة الدفع قريباً من الانتهاء
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>الاشتراك:</strong> {{ plan_name }}
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>وسيلة الدفع:</strong> {{ payment_method }}
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.warning|default:'#f59e0b' }}" padding="5px 0">
                <strong>تنتهي في:</strong> {{ expiration_date|date:"m/Y" }}
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>التاريخ التالي للسداد:</strong> {{ next_billing_date|date:"F d, Y" }}
              </mj-text>

              <mj-divider border-color="#fed7aa" border-width="1px" padding="15px 0" />

              <mj-text font-size="13px" color="{{ theme.color.error|default:'#ef4444' }}" padding="5px 0" font-weight="600">
                ⚠️ يرجى تحديث وسيلة الدفع الخاصة بك قبل {{ expiration_date|date:"m/Y" }} لتجنب انقطاع الخدمة.
              </mj-text>
            </mj-column>
          </mj-section>
        </mj-wrapper>
      </mj-column>
    </mj-section>

    <!-- What You Need to Do -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="20px" font-weight="600" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="15px">
          ما يجب عليك فعله
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.warning|default:'#f59e0b' }}; font-size: 18px; margin-right: 8px;">1.</span>
          أضف وسيلة دفع جديدة أو قم بتحديث البطاقة الحالية
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.warning|default:'#f59e0b' }}; font-size: 18px; margin-right: 8px;">2.</span>
          تأكد من تحديثها قبل تاريخ السداد التالي
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.warning|default:'#f59e0b' }}; font-size: 18px; margin-right: 8px;">3.</span>
          سيستمر الاشتراك دون انقطاع
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Buttons -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="10px 20px 30px 20px">
      <mj-column>
        <mj-button href="{{ update_payment_url }}" background-color="{{ theme.color.warning|default:'#f59e0b' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" font-weight="600" border-radius="6px" padding="14px 32px">
          تحديث وسيلة الدفع
        </mj-button>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="15px">
          <a href="{{ manage_subscription_url }}" style="color: {{ theme.color.info|default:'#3b82f6' }}; text-decoration: underline;">
            إدارة الاشتراك
          </a>
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support Block -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          تحتاج إلى مساعدة؟ تواصل معنا في {{ support_email }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Spwig Branding Footer -->
    <mj-section padding="15px 0 10px 0" background-color="transparent">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" border-width="1px" padding="0 0 12px 0"></mj-divider>
        <mj-text align="center" padding="0" font-size="11px" color="#9ca3af" line-height="16px">
          <a href="https://spwig.com" style="color: #9ca3af; text-decoration: none; display: inline-flex; align-items: center; gap: 4px;" target="_blank">
            <img src="{{ shop_url }}/static/email_system/img/spwig-favicon.png" alt="Spwig" width="12" height="12" style="vertical-align: middle; display: inline-block;" />
            مدعوم بواسطة Spwig
          </a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
💳 وسيلة الدفع قريباً من الانتهاء

الإجراء المطلوب لتجنب انقطاع الاشتراك

وسيلة الدفع قريباً من الانتهاء:
الاشتراك: {{ plan_name }}
وسيلة الدفع: {{ payment_method }}
تنتهي في: {{ expiration_date|date:"m/Y" }}
التاريخ التالي للسداد: {{ next_billing_date|date:"F d, Y" }}

⚠️ يرجى تحديث وسيلة الدفع الخاصة بك قبل {{ expiration_date|date:"m/Y" }} لتجنب انقطاع الخدمة.

ما يجب عليك فعله:
1. أضف وسيلة دفع جديدة أو قم بتحديث البطاقة الحالية
2. تأكد من تحديثها قبل تاريخ السداد التالي
3. سيستمر الاشتراك دون انقطاع

تحديث وسيلة الدفع: {{ update_payment_url }}
إدارة الاشتراك: {{ manage_subscription_url }}

تحتاج إلى مساعدة؟ تواصل معنا في {{ support_email }}

---
مدعم بواسطة Spwig - https://spwig.com