---
template_type: cart_abandoned_48h
category: Cart Recovery
---

# Email Template: cart_abandoned_48h

## Subject
अंतिम अवसर! आपका कार्ट 24 घंटे में बंद हो जाएगा - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="#92400e" align="center">
          ⏰ अंतिम अवसर - 24 घंटे में कार्ट समाप्त हो जाएगा
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          छोड़े नहीं दीजिए, {{ customer_name }}!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          यह आपकी अंतिम याददाश्त है। 24 घंटे में आपका कार्ट समाप्त हो जाएगा और हम इन आइटम को और नहीं रख सकते।
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
          कुल: {{ cart_total }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ cart_url }}" background-color="#dc2626" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          इससे पहले ऑर्डर पूरा करें जब यह देर न हो जाए
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          सवाल हैं? हमारी टीम आपकी मदद के लिए यहां है: <a href="{{ support_url }}">समर्थन से संपर्क करें</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⏰ अंतिम अवसर - 24 घंटे में कार्ट समाप्त हो जाएगा

छोड़े नहीं दीजिए, {{ customer_name }}!

यह आपकी अंतिम याददाश्त है। 24 घंटे में आपका कार्ट समाप्त हो जाएगा और हम इन आइटम को और नहीं रख सकते।

आपका कार्ट:
{% for item in cart_items %}
- {{ item.product_name }}
  {{ item.quantity }} × {{ item.price }}
{% endfor %}

कुल: {{ cart_total }}

अंतिम अवसर से पहले अपना ऑर्डर पूरा करें: {{ cart_url }}

सवाल हैं? हमारी टीम आपकी मदद के लिए यहां है: {{ support_url }}

---
यह कार्ट #{{ cart_id }} के लिए अंतिम याददाश्त है।
