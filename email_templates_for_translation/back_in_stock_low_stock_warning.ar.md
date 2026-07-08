---
template_type: back_in_stock_low_stock_warning
category: Stock Notifications
---

# Email Template: back_in_stock_low_stock_warning

## Subject
⚠️ {{ product_name }} عاد ولكن بكميات محدودة! - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ مخزون محدود - اسرع!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          عاد {{ product_name }} إلى المخزون!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          مرحبًا {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          أخبار جيدة! المنتج الذي كنت تنتظره عاد إلى المخزون. ولكن عجلة - نحن فقط نملك {{ stock_remaining }} وحدة{{ stock_remaining|pluralize }} متبقية!
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column width="35%">
            <mj-image src="{{ product_image }}" alt="{{ product_name }}" border-radius="8px" />
          </mj-column>
          <mj-column width="65%">
            <mj-text font-weight="bold" font-size="18px" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ product_name }}
            </mj-text>
            <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
              {{ product_description }}
            </mj-text>
            <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}">
              {{ product_price }}
            </mj-text>
            {% if variant_name %}
            <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              المتغير: {{ variant_name }}
            </mj-text>
            {% endif %}
            <mj-spacer height="10px" />
            <mj-text font-size="14px" color="#dc2626" font-weight="bold">
              ⚠️ فقط {{ stock_remaining }} متبقية في المخزون!
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ product_url }}" background-color="#dc2626" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          اشترِ الآن قبل أن تنفد
        </mj-button>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#991b1b" align="center">
              🔥 <strong>تم بيع هذا المنتج {{ times_sold_out }} مرة{{ times_sold_out|pluralize }} في الشهر الماضي!</strong><br/>
              لا تفوت الفرصة مرة أخرى - اطلب الآن بينما لا يزال هناك مخزون.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          لم تعد ترغب فيه؟ <a href="{{ unsubscribe_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">الغاء الاشتراك من هذا الإشعار</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ مخزون محدود - اسرع!

{{ product_name }} عاد إلى المخزون!

مرحبًا {{ customer_name }},

أخبار جيدة! المنتج الذي كنت تنتظره عاد إلى المخزون. ولكن عجلة - نحن فقط نملك {{ stock_remaining }} وحدة{{ stock_remaining|pluralize }} متبقية!

PRODUCT:
{{ product_name }}
{{ product_description }}
السعر: {{ product_price }}
{% if variant_name %}المتغير: {{ variant_name }}{% endif %}

⚠️ فقط {{ stock_remaining }} متبقية في المخزون!

اشترِ الآن قبل أن تنفد: {{ product_url }}

🔥 تم بيع هذا المنتج {{ times_sold_out }} مرة{{ times_sold_out|pluralize }} في الشهر الماضي!
لا تفوت الفرصة مرة أخرى - اطلب الآن بينما لا يزال هناك مخزون.

لم تعد ترغب فيه؟ الغاء الاشتراك: {{ unsubscribe_url }}