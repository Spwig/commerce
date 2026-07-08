---
template_type: hosted_onboarding_day14
category: License
---

# Email Template: hosted_onboarding_day14

## Subject
ابدأ بالخطوة التالية - {{ store_name }}

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
          البدء: الميزات المتقدمة
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          استغل كامل إمكانات {{ store_name }}
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
          لقد قمت بتشغيل <strong>{{ store_name }}</strong> منذ بضعة أسابيع. إليك بعض الميزات المتقدمة التي ستساعدك على رفع متجرك إلى المستوى التالي.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 1 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          أنشئ سير عمل بريد إلكتروني تلقائي
        </mj-text>
        <mj-text font-size="14px">
          أتمتِّ بريدك الإلكتروني مع سير العمل. أنشئ سلسلة ترحيب، متابعة بعد الشراء، وحملات إعادة التفاعل تحت <strong>التسويق > سير العمل البريدي</strong>.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 2 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          ضع قواعد الضرائب لمناطقك
        </mj-text>
        <mj-text font-size="14px">
          تأكد من أنك تفرض معدلات الضرائب الصحيحة. انتقل إلى <strong>الإعدادات > الضرائب</strong> لتكوين قواعد الضرائب لكل منطقة تبيع إليها. يمكنك إعداد الأسعار شاملة الضرائب أو بدونها.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 3 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          استكشف واجهة برمجة التطبيقات للتكاملات
        </mj-text>
        <mj-text font-size="14px">
          إذا تضمن خطةك الوصول إلى واجهة برمجة التطبيقات، يمكنك دمج متجرك مع أدوات وخدمات خارجية. انتقل إلى <strong>الإعدادات > واجهة برمجة التطبيقات</strong> لإنشاء مفاتيح واجهة برمجة التطبيقات واستكشاف الوثائق.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 4 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          تحقق من لوحة التحليلات الخاصة بك
        </mj-text>
        <mj-text font-size="14px">
          ابقَ على اطلاع على أداء متجرك. تُظهر لوحة <strong>الرئيسية</strong> مؤشرات رئيسية تشمل الإيرادات، الطلبات، المنتجات الأعلى مبيعًا، وتحليلات العملاء لمساعدتك في اتخاذ قرارات مبنية على البيانات.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 5 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          فكِّر في إضافة نقطة بيع لبيع المنتجات داخل المتجر
        </mj-text>
        <mj-text font-size="14px">
          هل تبيع أيضًا في المتجر؟ تتيح ميزة نقطة بيع Spwig معالجة المعاملات داخل المتجر التي تتم تزامنها مع المخزون والطلب عبر الإنترنت. تحقق من <strong>الإعدادات > نقطة البيع</strong> لمعرفة المزيد.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="استكشف لوحتك" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
البدء: الميزات المتقدمة - {{ store_name }}

أهلاً {{ name|default:'there' }},

لقد قمت بتشغيل {{ store_name }} منذ بضعة أسابيع. إليك بعض الميزات المتقدمة التي ستساعدك على رفع متجرك إلى المستوى التالي.

1. أنشئ سير عمل بريد إلكتروني تلقائي
أتمتِّ بريدك الإلكتروني مع سلسلة ترحيب، متابعة بعد الشراء، وحملات إعادة التفاعل.

2. ضع قواعد الضرائب لمناطقك
تأكد من أنك تفرض معدلات الضرائب الصحيحة. انتقل إلى الإعدادات > الضرائب لتكوين قواعد الضرائب لكل منطقة.

3. استكشف واجهة برمجة التطبيقات للتكاملات
إذا تضمن خطةك الوصول إلى واجهة برمجة التطبيقات، يمكنك دمج متجرك مع أدوات خارجية. انتقل إلى الإعدادات > واجهة برمجة التطبيقات للبدء.

4. تحقق من لوحة التحليلات الخاصة بك
تُظهر لوحة الرئيسية مؤشرات رئيسية تشمل الإيرادات، الطلبات، المنتجات الأعلى مبيعًا، وتحليلات العملاء.

5. فكِّر في إضافة نقطة بيع لبيع المنتجات داخل المتجر
هل تبيع أيضًا في المتجر؟ تتيح ميزة نقطة بيع Spwig معالجة المعاملات داخل المتجر التي تتم تزامنها مع المخزون عبر الإنترنت.

استكشف لوحتك: {{ admin_url }}

هل تحتاج إلى مساعدة؟ تواصل مع {{ support_email }}