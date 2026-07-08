---
template_type: hosted_payment_recovered
category: License
---

# Email Template: hosted_payment_recovered

## Subject
الدفع ناجح - {{ store_name }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="#16a34a" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          الدفع ناجح
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          أهلاً {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          أخبار سعيدة! تم معالجة دفعتك البالغة <strong>{{ currency }}{{ amount }}</strong> لـ <strong>{{ plan_name }}</strong> بنجاح. يستمر الاشتراك دون انقطاع.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Go to Your Store" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
الدفع ناجح - {{ store_name }}

أهلاً {{ name|default:'there' }},

أخبار سعيدة! تم معالجة دفعتك البالغة {{ currency }}{{ amount }} لـ {{ plan_name }} بنجاح. يستمر الاشتراك دون انقطاع.

الذهاب إلى متجرك: {{ admin_url }}

هل تحتاج إلى مساعدة؟ تواصل مع {{ support_email }}