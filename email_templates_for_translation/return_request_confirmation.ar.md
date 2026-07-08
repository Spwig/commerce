---
template_type: return_request_confirmation
category: Returns
---

# Email Template: return_request_confirmation

## Subject
تم استلام طلب الإرجاع - طلب #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#eff6ff' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1e40af' }}">
          تم استلام طلب الإرجاع
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1e40af' }}">
          طلب #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          مرحباً {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          تم استلام طلب إرجاعك لطلب <strong>#{{ order_number }}</strong>.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              تفاصيل الإرجاع:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>السبب:</strong> {{ return_reason }}<br/>
              <strong>العناصر:</strong> {{ items_count }} عنصر(عناصر)<br/>
              <strong>الحالة:</strong> {{ return_status }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ماذا يحدث بعد ذلك؟
        </mj-text>

        <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          1. فريقنا سيقوم بمراجعة طلب الإرجاع الخاص بك خلال 24-48 ساعة<br/>
          2. بمجرد الموافقة، سنرسل لك ورقة شحن الإرجاع عبر البريد الإلكتروني<br/>
          3. قم بتعبئة العناصر بشكل آمن وقم بربط ورقة الإرجاع<br/>
          4. قم بإيداع الحزمة في أقرب مكان لشحن البضائع<br/>
          5. سيتم معالجة استرجاعك بمجرد استلامنا وفحص العناصر
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          إذا كانت لديك أي أسئلة، يرجى عدم التردد في التواصل معنا.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
تم استلام طلب الإرجاع
طلب #{{ order_number }}

مرحباً {{ customer_name }},

تم استلام طلب إرجاعك لطلب #{{ order_number }}.

تفاصيل الإرجاع:
- السبب: {{ return_reason }}
- العناصر: {{ items_count }} عنصر(عناصر)
- الحالة: {{ return_status }}

ماذا يحدث بعد ذلك؟
1. فريقنا سيقوم بمراجعة طلب الإرجاع الخاص بك خلال 24-48 ساعة
2. بمجرد الموافقة، سنرسل لك ورقة شحن الإرجاع عبر البريد الإلكتروني
3. قم بتعبئة العناصر بشكل آمن وقم بربط ورقة الإرجاع
4. قم بإيداع الحزمة في أقرب مكان لشحن البضائع
5. سيتم معالجة استرجاعك بمجرد استلامنا وفحص العناصر

إذا كانت لديك أي أسئلة، يرجى عدم التردد في التواصل معنا.