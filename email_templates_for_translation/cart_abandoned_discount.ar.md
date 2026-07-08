---
template_type: cart_abandoned_discount
category: Cart Recovery
---

# Email Template: cart_abandoned_discount

## Subject
خصم {{ discount_percentage }}% خاص بك! - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          🎉 عرض خاص فقط لك!
        </mj-text>
        <mj-text font-size="18px" color="#047857" align="center">
          {{ discount_percentage }}% خصم على عربتك
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          نريد أن تجعل هذا سهلاً، {{ customer_name }}
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          اكمل شراءك الآن واحفظ {{ discount_percentage }}% مع الكود <strong>{{ discount_code }}</strong>
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="20px" border="2px dashed #059669">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              كودك الحصري
            </mj-text>
            <mj-text font-size="28px" font-weight="bold" color="#047857" align="center" font-family="'Courier New', monospace">
              {{ discount_code }}
            </mj-text>
            <mj-text font-size="13px" color="#065f46" align="center">
              ينتهي في: {{ discount_expiry }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

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

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text align="right">
              <span style="color: {{ theme.color.text_secondary|default:'#6b7280' }};">المجموع الفرعي:</span> <span style="text-decoration: line-through; color: #9ca3af;">{{ cart_total }}</span>
            </mj-text>
            <mj-text align="right">
              <span style="color: {{ theme.color.text_secondary|default:'#6b7280' }};">الخصم ({{ discount_percentage }}%):</span> <span style="color: #059669; font-weight: bold;">-{{ discount_amount }}</span>
            </mj-text>
            <mj-text font-size="20px" font-weight="bold" align="right" color="{{ theme.color.text|default:'#1f2937' }}">
              المجموع الجديد: {{ discounted_total }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ cart_url }}" background-color="#059669" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          احصل على خصمك {{ discount_percentage }}%
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="#dc2626" align="center" font-style="italic">
          العرض ينتهي {{ discount_expiry }} - لا تفوت الفرصة!
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 عرض خاص فقط لك!
{{ discount_percentage }}% خصم على عربتك

نريد أن تجعل هذا سهلاً، {{ customer_name }}

اكمل شراءك الآن واحفظ {{ discount_percentage }}% مع الكود {{ discount_code }}

═══════════════════════════
كودك الحصري
{{ discount_code }}
ينتهي في: {{ discount_expiry }}
═══════════════════════════

عربتك:
{% for item in cart_items %}
- {{ item.product_name }}
  {{ item.quantity }} × {{ item.price }}
{% endfor %}

المجموع الفرعي: {{ cart_total }}
الخصم ({{ discount_percentage }}%): -{{ discount_amount }}
المجموع الجديد: {{ discounted_total }}

احصل على خصمك {{ discount_percentage }}%: {{ cart_url }}

العرض ينتهي {{ discount_expiry }} - لا تفوت الفرصة!