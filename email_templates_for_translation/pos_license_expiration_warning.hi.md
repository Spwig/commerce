---
template_type: pos_license_expiration_warning
category: POS
---

# Email Template: pos_license_expiration_warning

## Subject
{% if is_grace_period %}[अवधि] POS लाइसेंस - {{ days_remaining }} दिन बाकी है{% else %}[जल्दी खत्म हो रहा है] POS लाइसेंस - {{ days_remaining }} दिन बाकी है{% endif %}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{% if is_grace_period %}#fef2f2{% else %}#fffbeb{% endif %}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{% if is_grace_period %}#991b1b{% else %}#92400e{% endif %}" align="center">
          {% if is_grace_period %}POS लाइसेंस अवधि{% else %}POS लाइसेंस जल्दी खत्म हो रहा है{% endif %}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {% if is_grace_period %}आपका Spwig POS लाइसेंस अवधि {{ days_remaining }} दिन{{ days_remaining|pluralize }} में समाप्त हो जाएगा। अवधि समाप्त हो जाने के बाद, POS API पहुँच बंद कर दी जाएगी।{% else %}आपका Spwig POS लाइसेंस {{ days_remaining }} दिन{{ days_remaining|pluralize }} में समाप्त हो जाएगा।{% endif %}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              लाइसेंस विवरण:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>लाइसेंस:</strong> {{ license_key_masked }}<br/>
              <strong>समाप्त होता है:</strong> {{ expires_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ renewal_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          POS लाइसेंस नवीनीकरण करें
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
{% if is_grace_period %}POS लाइसेंस अवधि{% else %}POS लाइसेंस जल्दी खत्म हो रहा है{% endif %}

{% if is_grace_period %}आपका Spwig POS लाइसेंस अवधि {{ days_remaining }} दिन{{ days_remaining|pluralize }} में समाप्त हो जाएगा। अवधि समाप्त हो जाने के बाद, POS API पहुँच बंद कर दी जाएगी।{% else %}आपका Spwig POS लाइसेंस {{ days_remaining }} दिन{{ days_remaining|pluralize }} में समाप्त हो जाएगा।{% endif %}

लाइसेंस विवरण:
- लाइसेंस: {{ license_key_masked }}
- समाप्त होता है: {{ expires_at }}

POS लाइसेंस नवीनीकरण करें: {{ renewal_url }}