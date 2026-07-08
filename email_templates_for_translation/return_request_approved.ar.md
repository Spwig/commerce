---
template_type: return_request_approved
category: Returns
---

# Email Template: return_request_approved

## Subject
تمت الموافقة على استرجاعك - طلب #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f0fdf4' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#166534' }}">
          تمت الموافقة على الاسترجاع
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#166534' }}">
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
          تم الموافقة على طلب استرجاعك لطلبك <strong>#{{ order_number }}</strong>.
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>الخطوات التالية:</strong>
        </mj-text>

        <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          1. قم بتنزيل وطباعة وسم الاسترجاع أدناه<br/>
          2. حزم العناصر بأمان في عبواتها الأصلية إذا أمكن<br/>
          3. ربط وسم الاسترجاع على خارج العبوة<br/>
          4. تجاهلها في أقرب مكان لشحنك
        </mj-text>

        {% if return_label_url %}
        <mj-spacer height="20px" />
        <mj-button href="{{ return_label_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          تنزيل وسم الاسترجاع
        </mj-button>
        {% endif %}

        {% if return_tracking_number %}
        <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>رقم تتبع الاسترجاع:</strong> {{ return_tracking_number }}
        </mj-text>
        {% endif %}

        <mj-section background-color="{{ theme.color.surface|default:'#fffbeb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#92400e' }}">
              <strong>مهم:</strong> يرجى إرسال الاسترجاع خلال 7 أيام لضمان معالجة استرجاعك بسرعة.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          بمجرد استلامنا وفحص استرجاعك، سنقوم بمعالجة استرجاعك إلى وسيلة الدفع الأصلية.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
تمت الموافقة على الاسترجاع - طلب #{{ order_number }}

مرحباً {{ customer_name }},

تم الموافقة على طلب استرجاعك لطلب #{{ order_number }}.

الخطوات التالية:
1. قم بتنزيل وطباعة وسم الاسترجاع
2. حزم العناصر بأمان في عبواتها الأصلية إذا أمكن
3. ربط وسم الاسترجاع على خارج العبوة
4. تجاهلها في أقرب مكان لشحنك

{% if return_label_url %}تنزيل وسم الاسترجاع: {{ return_label_url }}{% endif %}
{% if return_tracking_number %}رقم تتبع الاسترجاع: {{ return_tracking_number }}{% endif %}

مهم: يرجى إرسال الاسترجاع خلال 7 أيام لضمان معالجة استرجاعك بسرعة.

بمجرد استلامنا وفحص استرجاعك، سنقوم بمعالجة استرجاعك إلى وسيلة الدفع الأصلية.