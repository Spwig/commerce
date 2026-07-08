---
template_type: license_maintenance_renewal
category: License
---

# Email Template: license_maintenance_renewal

## Subject
تم تجديد الصيانة - طلب #{{ order_number }}

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
    <mj-section background-color="{{ theme.color.success|default:'#10b981' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          تم تجديد الصيانة!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          طلب #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          أهلاً {{ customer_name }},
        </mj-text>
        <mj-text>
          تم تجديد اشتراك صيانة Spwig بنجاح. ستستمر في استلام تحديثات المنصة، والإصلاحات الأمنية، والميزات الجديدة.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Renewal Summary -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          ملخص التجديد
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          مفتاح الترخيص: {{ license_key }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          صلاحية الصيانة حتى: {{ renewal_expires_at }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          رقم الطلب: {{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What's Included -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          ما يشمله
        </mj-text>
        <mj-text font-size="14px">
          يمنحك الاشتراك النشط في الصيانة الوصول إلى:
        </mj-text>
        <mj-text font-size="14px" padding-top="5px">
          - تحديثات ميزات المنصة والتحسينات
        </mj-text>
        <mj-text font-size="14px">
          - إصلاحات الأمان وتصحيح الأخطاء
        </mj-text>
        <mj-text font-size="14px">
          - إصدارات مكونات جديدة عبر خادم الترقية
        </mj-text>
        <mj-text font-size="14px">
          - الدعم الفني
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Next Steps -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          لا يتطلب أي إجراء من جانبك. سيظل التحديث متاحًا عبر نظام تحديث المكونات في لوحة إدارةك.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
تم تجديد الصيانة!

طلب #{{ order_number }}

أهلاً {{ customer_name }},

تم تجديد اشتراك صيانة Spwig بنجاح. ستستمر في استلام تحديثات المنصة، والإصلاحات الأمنية، والميزات الجديدة.

ملخص التجديد:
- مفتاح الترخيص: {{ license_key }}
- صلاحية الصيانة حتى: {{ renewal_expires_at }}
- رقم الطلب: {{ order_number }}

ما يشمله:
- تحديثات ميزات المنصة والتحسينات
- إصلاحات الأمان وتصحيح الأخطاء
- إصدارات مكونات جديدة عبر خادم الترقية
- الدعم الفني

لا يتطلب أي إجراء من جانبك. سيظل التحديث متاحًا عبر نظام تحديث المكونات في لوحة إدارةك.

هل تحتاج إلى مساعدة؟ تواصل مع {{ support_email }}