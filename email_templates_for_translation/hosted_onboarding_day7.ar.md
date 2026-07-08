---
template_type: hosted_onboarding_day7
category: License
---

# Email Template: hosted_onboarding_day7

## Subject
زيادة مبيعاتك - {{ store_name }}

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
          البدء: التسويق والنمو
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          قم بجذب الزوار والمبيعات إلى {{ store_name }}
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
          الآن بعد أن بدأت {{ store_name }} في التشكل، حان الوقت لتركيز جهودك على جذب الزوار وزيادة مبيعاتك. إليك خمس نصائح تسويقية لمساعدتك في البدء.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 1 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          أنشئ أول كود خصم لك
        </mj-text>
        <mj-text font-size="14px">
          قدم خصمًا لجذب عملائك الأوائل. انتقل إلى <strong>التسويق > كودات الخصم</strong> لإنشاء خصومات نسبية أو ثابتة مع حدود استخدام اختيارية وتواريخ انتهاء الصلاحية.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 2 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          أنشئ نظام استعادة عربات التسوق المهجورة
        </mj-text>
        <mj-text font-size="14px">
          استعد لاستعادة المبيعات المفقودة تلقائيًا. قم بتفعيل رسائل استعادة عربات التسوق المهجورة تحت <strong>التسويق > عربات التسوق المهجورة</strong> لتذكير العملاء بالعناصر التي تركوها.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 3 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          ربط حسابات وسائل التواصل الاجتماعي
        </mj-text>
        <mj-text font-size="14px">
          ربط ملفاتك الشخصية على وسائل التواصل الاجتماعي مع متجرك بحيث يمكن للعملاء العثور عليك والاتباع. أضف روابط وسائل التواصل الاجتماعي تحت <strong>الإعدادات > وسائل التواصل الاجتماعي</strong> لعرضها في قاعدة متجرك.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 4 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          أنشئ تتبع Google Analytics
        </mj-text>
        <mj-text font-size="14px">
          فهم من أين يأتي زوارك وكيف يتفاعلون مع متجرك. أضف معرف تتبع Google Analytics الخاص بك تحت <strong>الإعدادات > التحليلات</strong> لبدء جمع البيانات.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 5 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          أنشئ نموذج الاشتراك في النشرة الإخبارية
        </mj-text>
        <mj-text font-size="14px">
          ابدأ ببناء قوائم بريدك الإلكتروني من اليوم الأول. أضف نموذج الاشتراك في النشرة الإخبارية إلى متجرك لجمع بريد الزوار. استخدم هذه الاتصالات للترويج واطلاق المنتجات والتفاعل مع العملاء.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Go to Marketing" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
البدء: التسويق والنمو - {{ store_name }}

أهلاً {{ name|default:'there' }},

الآن بعد أن بدأت {{ store_name }} في التشكل، حان الوقت لتركيز جهودك على جذب الزوار وزيادة مبيعاتك. إليك خمس نصائح تسويقية لمساعدتك في البدء.

1. أنشئ أول كود خصم لك
قدم خصمًا لجذب عملائك الأوائل. انتقل إلى التسويق > كودات الخصم لإنشاء خصومات مع حدود استخدام اختيارية وتواريخ انتهاء الصلاحية.

2. أنشئ نظام استعادة عربات التسوق المهجورة
استعد لاستعادة المبيعات المفقودة تلقائيًا. قم بتفعيل رسائل استعادة عربات التسوق المهجورة تحت التسويق > عربات التسوق المهجورة.

3. ربط حسابات وسائل التواصل الاجتماعي
ربط ملفاتك الشخصية على وسائل التواصل الاجتماعي مع متجرك. أضف روابط وسائل التواصل الاجتماعي تحت الإعدادات > وسائل التواصل الاجتماعي.

4. أنشئ تتبع Google Analytics
فهم من أين يأتي زوارك. أضف معرف تتبع Google Analytics الخاص بك تحت الإعدادات > التحليلات.

5. أنشئ نموذج الاشتراك في النشرة الإخبارية
ابدأ ببناء قوائم بريدك الإلكتروني من اليوم الأول. أضف نموذج الاشتراك في النشرة الإخبارية إلى متجرك لجمع بريد الزوار للاستخدام في الترويج والتفاعل.

اذهب إلى التسويق: {{ admin_url }}

تحتاج إلى مساعدة؟ تواصل مع {{ support_email }}