---
template_type: affiliate_account_rejected
category: Affiliate Program
---

# Email Template: affiliate_account_rejected

## Subject
تحديث تطبيق الشريك

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
          تحديث التطبيق
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
          شكرًا لاهتمامك بالانضمام إلى برنامج شركاء {{ shop_name }}.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          بعد مراجعة طلبك، قررنا عدم المتابعة في الوقت الحالي.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          هذا القرار يعتمد على متطلبات برنامج الشركاء الحالي لدينا، وقد لا يعكس مؤهلاتك أو إمكاناتك.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          نرحب بك للتقديم مرة أخرى في المستقبل إذا تغيرت ظروفك.
        </mj-text>
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
تحديث تطبيق الشريك

مرحبًا {{ affiliate_name }},

شكرًا لاهتمامك بالانضمام إلى برنامج شركاء {{ shop_name }}.

بعد مراجعة طلبك، قررنا عدم المتابعة في الوقت الحالي.

هذا القرار يعتمد على متطلبات برنامج الشركاء الحالي لدينا، وقد لا يعكس مؤهلاتك أو إمكاناتك.

نرحب بك للتقديم مرة أخرى في المستقبل إذا تغيرت ظروفك.

{{ shop_name }}
هل لديك أسئلة؟ اتصل بـ {{ support_email }}