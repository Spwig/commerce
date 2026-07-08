---
template_type: hosted_interval_changed
category: License
---

# Email Template: hosted_interval_changed

## Subject
تم تحديث الفاتورة - {{ store_name }}

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
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          تم تحديث الفاتورة
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
          أهلاً بك،
        </mj-text>
        <mj-text>
          تم تحديث فترة الفاتورة الخاصة بخطة <strong>{{ plan_name }}</strong> الخاصة بك على <strong>{{ store_name }}</strong>.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Billing Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          تفاصيل الفاتورة
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          الخطة: {{ plan_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          فترة الفاتورة السابقة: {{ old_interval }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          فترة الفاتورة الجديدة: {{ new_interval }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          تاريخ الفاتورة القادم: {{ next_billing_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Additional Info -->
    <mj-section>
      <mj-column>
        <mj-text>
          تظل الاشتراك نشطًا. يمكنك إدارة تفضيلات الفاتورة في أي وقت من حسابك.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="إدارة الاشتراك" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
تم تحديث الفاتورة - {{ store_name }}

أهلاً بك،

تم تحديث فترة الفاتورة الخاصة بخطة {{ plan_name }} الخاصة بك على {{ store_name }}.

تفاصيل الفاتورة:
- الخطة: {{ plan_name }}
- فترة الفاتورة السابقة: {{ old_interval }}
- فترة الفاتورة الجديدة: {{ new_interval }}
- تاريخ الفاتورة القادم: {{ next_billing_date }}

تظل الاشتراك نشطًا. يمكنك إدارة تفضيلات الفاتورة في أي وقت من حسابك.

إدارة الاشتراك: https://spwig.com/account

هل تحتاج إلى مساعدة؟ تواصل مع {{ support_email }}