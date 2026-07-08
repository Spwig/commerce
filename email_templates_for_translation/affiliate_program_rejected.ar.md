---
template_type: affiliate_program_rejected
category: Affiliate Program
---

# Email Template: affiliate_program_rejected

## Subject
تحديث تطبيق البرنامج

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
         شكرًا لتقديم طلبك لترويج {{ program_name }}.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          بعد مراجعة طلبك، قررنا عدم الموافقة عليه في الوقت الحالي.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          يمكنك مازالت ترويج برامج أخرى في شبكة شركائنا.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#6c757d" color="#ffffff" href="{{ portal_url }}">
          عرض البرامج الأخرى
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
تحديث تطبيق البرنامج

مرحبًا {{ affiliate_name }},

شكرًا لتقديم طلبك لترويج {{ program_name }}.

بعد مراجعة طلبك، قررنا عدم الموافقة عليه في الوقت الحالي.

يمكنك مازالت ترويج برامج أخرى في شبكة شركائنا.

عرض البرامج الأخرى: {{ portal_url }}

{{ shop_name }}
هل لديك أسئلة؟ اتصل {{ support_email }}