---
template_type: hosted_onboarding_tips
category: License
---

# Email Template: hosted_onboarding_tips

## Subject
نصائح للحصول على أقصى استفادة من {{ store_name }}

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
          نصائح البدء
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          استفد بأقصى طريقة من متجرك على Spwig
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          مرحبًا {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          الآن بعد أن أصبح <strong>{{ store_name }}</strong> نشطًا، إليك بعض النصائح لمساعدتك على الاستفادة القصوى من متجرك.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 1: Theme -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          قم بتخصيص مظهرك
        </mj-text>
        <mj-text font-size="14px">
          انتقل إلى <strong>التصميم > إعدادات القالب</strong> لاختيار قالب، رفع شعارك، وتحديد ألوان علامتك التجارية. يتم تحديث متجرك فورًا بحيث يمكنك معاينة التغييرات في الوقت الفعلي.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 2: Products -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          أضف منتجاتك
        </mj-text>
        <mj-text font-size="14px">
          انتقل إلى <strong>المحفظة > المنتجات</strong> لبدء إضافة منتجاتك. يمكنك إنشاء متغيرات المنتج (الحجم، اللون)، تحديد الأسعار، إدارة المخزون، ورفع صور عالية الجودة.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 3: Payments -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          قم بإعداد الدفع
        </mj-text>
        <mj-text font-size="14px">
          انتقل إلى <strong>الإعدادات > مزودي الدفع</strong> لربط Stripe أو PayPal أو طريقة دفع أخرى. يمكنك تمكين مزودين متعددين بحيث يمكن للعملاء الدفع بأي طريقة يفضلونها.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 4: Shipping -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          قم بتكوين الشحن
        </mj-text>
        <mj-text font-size="14px">
          تحت <strong>الإعدادات > الشحن</strong>، قم بإعداد مناطق الشحن ورسومها. يمكنك إنشاء قواعد شحن ثابتة أو بناءً على الوزن أو شحن مجاني لمناطق مختلفة.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 5: SEO -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          ارفع من SEO
        </mj-text>
        <mj-text font-size="14px">
          يقوم Spwig بإنشاء خرائط المواقع وعلامات التبويب تلقائيًا. انتقل إلى <strong>الإعدادات > SEO</strong> لتخصيص عناوين صفحاتك، الوصفات، وصور المشاركة الاجتماعية لمساعدتك على إيجاد متجرك.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Go to Admin Panel" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
نصائح البدء - {{ store_name }}

مرحبًا {{ name|default:'there' }},

الآن بعد أن أصبح {{ store_name }} نشطًا، إليك بعض النصائح لمساعدتك على الاستفادة القصوى من متجرك.

1. قم بتخصيص مظهرك
اذهب إلى التصميم > إعدادات القالب لاختيار قالب، رفع شعارك، وتحديد ألوان علامتك التجارية.

2. أضف منتجاتك
اذهب إلى المحفظة > المنتجات لبدء إضافة منتجاتك مع المتغيرات، الأسعار، والصور.

3. قم بإعداد الدفع
اذهب إلى الإعدادات > مزودي الدفع لربط Stripe أو PayPal أو طريقة دفع أخرى.

4. قم بتكوين الشحن
تحت الإعدادات > الشحن، قم بإعداد مناطق الشحن ورسومها لمناطق مختلفة.

5. ارفع من SEO
اذهب إلى الإعدادات > SEO لتخصيص عناوين صفحاتك، الوصفات، وصور المشاركة الاجتماعية.

اذهب إلى لوحة التحكم: {{ admin_url }}

تحتاج إلى مساعدة؟ تواصل مع {{ support_email }}