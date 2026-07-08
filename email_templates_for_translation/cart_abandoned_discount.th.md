---
template_type: cart_abandoned_discount
category: Cart Recovery
---

# Email Template: cart_abandoned_discount

## Subject
ส่วนลดพิเศษ {{ discount_percentage }}% สำหรับตะกร้าสินค้าของคุณ! - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          🎉 ข้อเสนอพิเศษสำหรับคุณเท่านั้น!
        </mj-text>
        <mj-text font-size="18px" color="#047857" align="center">
          {{ discount_percentage }}% OFF Your Cart
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          เราอยากให้คุณได้รับสิทธิ์นี้อย่างง่ายดาย {{ customer_name }}
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          โปรดทำการซื้อสินค้าทันทีและประหยัด {{ discount_percentage }}% โดยใช้รหัส <strong>{{ discount_code }}</strong>
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="20px" border="2px dashed #059669">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              YOUR EXCLUSIVE CODE
            </mj-text>
            <mj-text font-size="28px" font-weight="bold" color="#047857" align="center" font-family="'Courier New', monospace">
              {{ discount_code }}
            </mj-text>
            <mj-text font-size="13px" color="#065f46" align="center">
              Expires: {{ discount_expiry }}
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
              <span style="color: {{ theme.color.text_secondary|default:'#6b7280' }};">Subtotal:</span> <span style="text-decoration: line-through; color: #9ca3af;">{{ cart_total }}</span>
            </mj-text>
            <mj-text align="right">
              <span style="color: {{ theme.color.text_secondary|default:'#6b7280' }};">Discount ({{ discount_percentage }}%):</span> <span style="color: #059669; font-weight: bold;">-{{ discount_amount }}</span>
            </mj-text>
            <mj-text font-size="20px" font-weight="bold" align="right" color="{{ theme.color.text|default:'#1f2937' }}">
              New Total: {{ discounted_total }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ cart_url }}" background-color="#059669" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Claim Your {{ discount_percentage }}% Discount
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="#dc2626" align="center" font-style="italic">
          Offer expires {{ discount_expiry }} - Don't miss out!
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 ข้อเสนอพิเศษสำหรับคุณเท่านั้น!
{{ discount_percentage }}% OFF YOUR CART

เราอยากให้คุณได้รับสิทธิ์นี้อย่างง่ายดาย {{ customer_name }}

โปรดทำการซื้อสินค้าทันทีและประหยัด {{ discount_percentage }}% โดยใช้รหัส {{ discount_code }}

═══════════════════════════
YOUR EXCLUSIVE CODE
{{ discount_code }}
Expires: {{ discount_expiry }}
═══════════════════════════

YOUR CART:
{% for item in cart_items %}
- {{ item.product_name }}
  {{ item.quantity }} × {{ item.price }}
{% endfor %}

Subtotal: {{ cart_total }}
Discount ({{ discount_percentage }}%): -{{ discount_amount }}
NEW TOTAL: {{ discounted_total }}

Claim your {{ discount_percentage }}% discount: {{ cart_url }}

Offer expires {{ discount_expiry }} - Don't miss out!