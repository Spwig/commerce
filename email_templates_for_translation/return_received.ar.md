---
template_type: return_received
category: Returns
---

# Email Template: return_received

## Subject
لقد تلقينا إرجاعك - طلب #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#eff6ff' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.primary|default:'#1d4ed8' }}">
          إرجاع تلقينا
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.primary|default:'#1d4ed8' }}">
          طلب #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          أهلاً {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          لقد تلقينا إرجاع البضائع الخاصة بك لطلب <strong>#{{ order_number }}</strong>.
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>ما الذي سيحدث بعد ذلك:</strong>
        </mj-text>

        <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          1. فريقنا سيقوم بفحص البضائع المرتجعة خلال 2-3 أيام عمل<br/>
          2. سنتحقق من أن البضائع في حالتها الأصلية<br/>
          3. بمجرد انتهاء الفحص، سنقوم بمعالجة استرجاعك<br/>
          4. سترسل لك بريدًا إلكترونيًا تأكيدًا بمجرد معالجة الاسترجاع
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          سيتم إيداع الاسترجاع في وسيلة الدفع الأصلية الخاصة بك، وقد يستغرق من 5 إلى 10 أيام عمل لظهوره في حسابك.
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          شكرًا لصبرك!
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
إرجاع تلقينا - طلب #{{ order_number }}

أهلاً {{ customer_name }},

لقد تلقينا إرجاع البضائع الخاصة بك لطلب #{{ order_number }}.

ما الذي سيحدث بعد ذلك:
1. فريقنا سيقوم بفحص البضائع المرتجعة خلال 2-3 أيام عمل
2. سنتحقق من أن البضائع في حالتها الأصلية
3. بمجرد انتهاء الفحص، سنقوم بمعالجة استرجاعك
4. سترسل لك بريدًا إلكترونيًا تأكيدًا بمجرد معالجة الاسترجاع

سيتم إيداع الاسترجاع في وسيلة الدفع الأصلية الخاصة بك، وقد يستغرق من 5 إلى 10 أيام عمل لظهوره في حسابك.

شكرًا لصبرك!