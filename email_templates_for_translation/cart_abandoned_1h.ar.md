---
template_type: cart_abandoned_1h
category: Cart Recovery
---

# Email Template: cart_abandoned_1h

## Subject
إنضمّ سلة التسوق الخاصة بك! أكمل طلبك - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          لقد تركت {{ cart_item_count }} عنصرًا {{ cart_item_count|pluralize }} في سلة التسوق الخاصة بك
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          مرحباً {{ customer_name }},
        </mj-text>

        <mj:text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          لاحظنا أنك لم تكمل شراءك. فإن العناصر ما زالت تنتظر في سلة التسوق الخاصة بك!
        </mj-text>

        <mj-spacer height="20px" />

        {% for item in cart_items %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column width="30%">
            <mj-image src="{{ item.product_image }}" alt="{{ item.product_name }}" border-radius="4px" />
          </mj-column>
          <mj-column width="70%">
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ item.product_name }}
            </mj-text>
            <mj-text color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              Qty: {{ item.quantity }} × {{ item.price }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="20px" />

        <mj-text font-size="18px" font-weight="bold" align="right" color="{{ theme.color.text|default:'#1f2937' }}">
          المجموع: {{ cart_total }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ cart_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          أكمل طلبك
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          تحتاج إلى مساعدة؟ <a href="{{ support_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">اتصل بفريق الدعم الخاص بنا</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
لقد تركت {{ cart_item_count }} عنصرًا {{ cart_item_count|pluralize }} في سلة التسوق الخاصة بك

مرحباً {{ customer_name }},

لاحظنا أنك لم تكمل شراءك. فإن العناصر ما زالت تنتظر في سلة التسوق الخاصة بك!

سلة التسوق الخاصة بك:
{% for item in cart_items %}
- {{ item.product_name }}
  Qty: {{ item.quantity }} × {{ item.price }}
{% endfor %}

المجموع: {{ cart_total }}

أكمل طلبك: {{ cart_url }}

تحتاج إلى مساعدة؟ اتصل بفريق الدعم الخاص بنا: {{ support_url }}

---

تتلقى هذا البريد الإلكتروني لأنك أضفت عناصر إلى سلة التسوق الخاصة بك في {{ shop_name }}.
لوقف استلام تنبيهات سلة التسوق، قم بزيارة: {{ preferences_url }}