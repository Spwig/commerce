---
template_type: refund_notification
category: Core E-commerce
---

# Email Template: refund_notification

## Subject
वापसी प्रक्रिया पूर्ण - आदेश #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          वापसी प्रक्रिया पूर्ण
        </mj-text>
        <mj-text>
          आदेश #{{ order_number }} के लिए वापसी प्रक्रिया पूर्ण कर दी गई है।
        </mj-text>
        <mj-text>
          <strong>वापसी राशि:</strong> {{ refund_amount }}
        </mj-text>
        <mj-text>
          वापसी आपके खाते में {{ refund_days }} व्यावसायिक दिनों के भीतर दिखाई देगी।
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
वापसी प्रक्रिया पूर्ण

आदेश #{{ order_number }} के लिए वापसी प्रक्रिया पूर्ण कर दी गई है।

वापसी राशि: {{ refund_amount }}

वापसी आपके खाते में {{ refund_days }} व्यावसायिक दिनों के भीतर दिखाई देगी।

