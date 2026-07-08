---
template_type: affiliate_account_approved
category: Affiliate Program
---

# Email Template: affiliate_account_approved

## Subject
🎉 مرحبا بك في برنامج الإحالة لـ {{ shop_name }}!

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="#f8f9fa">
    <!-- Header -->
    <mj-section background-color="#ffffff" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="#212529" align="center">
          🎉 تم قبول طلبك!
        </mj-text>
        <mj-text font-size="18px" color="#6c757d" align="center">
          مرحبًا بكم في برنامج الإحالة الخاص بنا
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Success Banner -->
    <mj-section background-color="#28a745" padding="40px 20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#ffffff" align="center">
          أنت الآن مُحيل!
        </mj-text>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-top="10px">
          ابدأ بربح عمولة اليوم
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          مرحبًا {{ affiliate_name }},
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          تهانينا! تم قبول طلبك للانضمام إلى برنامج الإحالة لـ {{ shop_name }}.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          يمكنك الآن البدء في الترويج لمنتجاتنا وربح عمولة على كل بيع تنتجه.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- How it Works -->
    <mj-section background-color="#f8f9fa" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="#212529" align="center" padding-bottom="10px">
          كيف تعمل هذه الخدمة
        </mj-text>
        <mj-text font-size="14px" color="#6c757d">
          1. احصل على روابط الإحالة الخاصة بك من لوحة التحكم<br/>
          2. شارك هذه الروابط مع جمهورك<br/>
          3. اربح عمولة عند شراء الأشخاص من خلال روابطك<br/>
          4. استلم الدفعات وفقًا لجدول الدفع الخاص بك
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          الوصول إلى لوحة التحكم
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          هل لديك أسئلة؟ <a href="mailto:{{ support_email }}" style="color: #007bff;">اتصل بالدعم</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 مرحبا بك في برنامج الإحالة لـ {{ shop_name }}!

مرحبًا {{ affiliate_name }},

تهانينا! تم قبول طلبك للانضمام إلى برنامج الإحالة لـ {{ shop_name }}.

يمكنك الآن البدء في الترويج لمنتجاتنا وربح عمولة على كل بيع تنتجه.

كيف تعمل هذه الخدمة:
1. احصل على روابط الإحالة الخاصة بك من لوحة التحكم
2. شارك هذه الروابط مع جمهورك
3. اربح عمولة عند شراء الأشخاص من خلال روابطك
4. استلم الدفعات وفقًا لجدول الدفع الخاص بك

الوصول إلى لوحة التحكم: {{ portal_url }}

{{ shop_name }}
هل لديك أسئلة؟ اتصل بـ {{ support_email }}