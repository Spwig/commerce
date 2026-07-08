---
template_type: cart_abandoned_discount
category: Cart Recovery
---

# Email Template: cart_abandoned_discount

## Subject
आपकी कार्ट पर {{ discount_percentage }}% की विशेष छूट! - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          🎉 आपके लिए विशेष ऑफर!
        </mj-text>
        <mj-text font-size="18px" color="#047857" align="center">
          अपनी कार्ट पर {{ discount_percentage }}% छूट
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          हम इसे आसान बनाना चाहते हैं, {{ customer_name }}
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          अब अपनी खरीदारी पूरी करें और कोड के साथ {{ discount_percentage }}% बचाएं <strong>{{ discount_code }}</strong>
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="20px" border="2px dashed #059669">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              आपका विशेष कोड
            </mj-text>
            <mj-text font-size="28px" font-weight="bold" color="#047857" align="center" font-family="'Courier New', monospace">
              {{ discount_code }}
            </mj-text>
            <mj-text font-size="13px" color="#065f46" align="center">
              अवधि समाप्त: {{ discount_expiry }}
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
              <span style="color: {{ theme.color.text_secondary|default:'#6b7280' }};">उपभोग के बाद:</span> <span style="text-decoration: line-through; color: #9ca3af;">{{ cart_total }}</span>
            </mj-text>
            <mj-text align="right">
              <span style="color: {{ theme.color.text_secondary|default:'#6b7280' }};">छूट ({{ discount_percentage }}%):</span> <span style="color: #059669; font-weight: bold;">-{{ discount_amount }}</span>
            </mj-text>
            <mj-text font-size="20px" font-weight="bold" align="right" color="{{ theme.color.text|default:'#1f2937' }}">
              नया कुल: {{ discounted_total }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ cart_url }}" background-color="#059669" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          अपने {{ discount_percentage }}% छूट का दावा करें
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="#dc2626" align="center" font-style="italic">
          ऑफर अवधि समाप्त: {{ discount_expiry }} - ना छोड़ें!
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 आपके लिए विशेष ऑफर!
{{ discount_percentage }}% अपनी कार्ट पर छूट

हम इसे आसान बनाना चाहते हैं, {{ customer_name }}

अब अपनी खरीदारी पूरी करें और कोड के साथ {{ discount_percentage }}% बचाएं {{ discount_code }}

═══════════════════════════
आपका विशेष कोड
{{ discount_code }}
अवधि समाप्त: {{ discount_expiry }}
═══════════════════════════

आपकी कार्ट:
{% for item in cart_items %}
- {{ item.product_name }}
  {{ item.quantity }} × {{ item.price }}
{% endfor %}

उपभोग के बाद: {{ cart_total }}
छूट ({{ discount_percentage }}%): -{{ discount_amount }}
नया कुल: {{ discounted_total }}

अपने {{ discount_percentage }}% छूट का दावा करें: {{ cart_url }}

ऑफर अवधि समाप्त: {{ discount_expiry }} - ना छोड़ें!