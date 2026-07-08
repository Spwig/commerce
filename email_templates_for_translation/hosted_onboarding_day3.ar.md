---
template_type: hosted_onboarding_day3
category: License
---

# Email Template: hosted_onboarding_day3

## Subject
أنشئ دليلك - {{ store_name }}

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
          البدء: منتجاتك
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          أنشئ دليلًا متميزًا لـ {{ store_name }}
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
          متجرك <strong>{{ store_name }}</strong> جاهز بالكامل. الآن هو الوقت لبناء دليل منتجاتك. إليك خمس نصائح للبدء.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 1 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          استيراد المنتجات من ملف CSV
        </mj-text>
        <mj-text font-size="14px">
          هل لديك قائمة بالمنتجات بالفعل؟ انتقل إلى <strong>الإدارة > الدليل > الاستيراد</strong> لاستيراد منتجاتك بالجملة من ملف CSV. هذا هو أسرع طريقة لملء متجرك.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 2 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          تنظيم باستخدام التصنيفات والفلاتر
        </mj-text>
        <mj-text font-size="14px">
          أنشئ تصنيفات وفلاتر للسمات بحيث يمكن للعملاء تصفح وعثور على ما يبحثون عنه بسهولة. الدليل المنظم يؤدي إلى معدل تحويل أعلى.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 3 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          اكتب وصفًا مقنعًا للمنتجات
        </mj-text>
        <mj-text font-size="14px">
          الوصف الجيد يبيع المنتجات. ركز على الفوائد، وليس فقط الميزات. أخبر العملاء لماذا يحتاجون منتجك وكيف يحل مشكلتهم.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 4 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          رفع صور منتجات ذات جودة عالية
        </mj-text>
        <mj-text font-size="14px">
          الصور الواضحة والمهنية تحدث فرقًا كبيرًا. رفع زوايا متعددة واستخدام إضاءة متسقة. يقوم Spwig تلقائيًا بتحسين الصور لضمان سرعة التحميل.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 5 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          إعداد متغيرات المنتج
        </mj-text>
        <mj-text font-size="14px">
          إذا كانت منتجاتك تأتي بأحجام أو ألوان أو أشكال مختلفة، أنشئ متغيرات بحيث يمكن للعملاء اختيار ما يريدون بالضبط. يمكن لكل متغير أن يكون له سعر ومستوى مخزني وصور مختلفة.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="إدارة منتجاتك" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
البدء: منتجاتك - {{ store_name }}

أهلاً {{ name|default:'there' }},

متجرك {{ store_name }} جاهز بالكامل. الآن هو الوقت لبناء دليل منتجاتك. إليك خمس نصائح للبدء.

1. استيراد المنتجات من ملف CSV
هل لديك قائمة بالمنتجات بالفعل؟ انتقل إلى الإدارة > الدليل > الاستيراد لاستيراد منتجاتك بالجملة من ملف CSV.

2. تنظيم باستخدام التصنيفات والفلاتر
أنشئ تصنيفات وفلاتر للسمات بحيث يمكن للعملاء تصفح وعثور على ما يبحثون عنه بسهولة.

3. اكتب وصفًا مقنعًا للمنتجات
الوصف الجيد يبيع المنتجات. ركز على الفوائد، وليس فقط الميزات. أخبر العملاء لماذا يحتاجون منتجك.

4. رفع صور منتجات ذات جودة عالية
الصور الواضحة والمهنية تحدث فرقًا كبيرًا. رفع زوايا متعددة واستخدام إضاءة متسقة.

5. إعداد متغيرات المنتج
إذا كانت منتجاتك تأتي بأحجام أو ألوان أو أشكال مختلفة، أنشئ متغيرات بحيث يمكن للعملاء اختيار ما يريدون بالضبط.

إدارة منتجاتك: {{ admin_url }}

هل تحتاج إلى مساعدة؟ تواصل مع {{ support_email }}