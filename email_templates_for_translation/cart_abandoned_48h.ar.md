---
template_type: cart_abandoned_48h
category: Cart Recovery
---

# Email Template: cart_abandoned_48h

## Subject
الفرصة الأخيرة! سينتهي سلة الشراء الخاصة بك في 24 ساعة - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="#92400e" align="center">
          ⏰ الفرصة الأخيرة - سلة الشراء ستنتهي في 24 ساعة
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          لا تفوت الفرصة، {{ customer_name }}!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          هذه هي مهلتك الأخيرة. سينتهي سلة الشراء الخاصة بك في 24 ساعة، ولا يمكننا الاحتفاظ بهذه السلع لفترة أطول.
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
              {{ item.quantity }} × {{ item.price }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="20px" />

        <mj-text font-size="20px" font-weight="bold" align="right" color="{{ theme.color.text|default:'#1f2937' }}">
          المجموع: {{ cart_total }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ cart_url }}" background-color="#dc2626" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          أكمل طلبك قبل فوات الأوان
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          لديك أسئلة؟ فريقنا هنا لمساعدتك: <a href="{{ support_url }}">اتصل بفريق الدعم</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⏰ الفرصة الأخيرة - سلة الشراء ستنتهي في 24 ساعة

لا تفوت الفرصة، {{ customer_name }}!

هذا هو آخر تذكير لك. سينتهي سلة الشراء الخاصة بك في 24 ساعة، ولا يمكننا الاحتفاظ بهذه السلع لفترة أطول.

سلة الشراء الخاصة بك:
{% for item in cart_items %}
- {{ item.product_name }}
  {{ item.quantity }} × {{ item.price }}
{% endfor %}

المجموع: {{ cart_total }}

أكمل طلبك قبل فوات الأوان: {{ cart_url }}

لديك أسئلة؟ فريقنا هنا لمساعدتك: {{ support_url }}

---

هذا هو آخر تذكير لسلة الشراء #{{ cart_id }}.