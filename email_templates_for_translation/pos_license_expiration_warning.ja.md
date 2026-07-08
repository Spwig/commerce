---
template_type: pos_license_expiration_warning
category: POS
---

# Email Template: pos_license_expiration_warning

## Subject
{% if is_grace_period %}[Grace Period] POS License - {{ days_remaining }} days remaining{% else %}[Expiring Soon] POS License - {{ days_remaining }} days remaining{% endif %}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{% if is_grace_period %}#fef2f2{% else %}#fffbeb{% endif %}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{% if is_grace_period %}#991b1b{% else %}#92400e{% endif %}" align="center">
          {% if is_grace_period %}POS License Grace Period{% else %}POS License Expiring Soon{% endif %}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {% if is_grace_period %}Your Spwig POS license grace period expires in <strong>{{ days_remaining }} day{{ days_remaining|pluralize }}</strong>. Once the grace period ends, POS API access will be blocked.{% else %}Your Spwig POS license expires in <strong>{{ days_remaining }} day{{ days_remaining|pluralize }}</strong>.{% endif %}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              License Details:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>License:</strong> {{ license_key_masked }}<br/>
              <strong>Expires:</strong> {{ expires_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ renewal_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Renew POS License
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
{% if is_grace_period %}POS LICENSE GRACE PERIOD{% else %}POS LICENSE EXPIRING SOON{% endif %}

{% if is_grace_period %}Your Spwig POS license grace period expires in {{ days_remaining }} day{{ days_remaining|pluralize }}. Once the grace period ends, POS API access will be blocked.{% else %}Your Spwig POS license expires in {{ days_remaining }} day{{ days_remaining|pluralize }}.{% endif %}

LICENSE DETAILS:
- License: {{ license_key_masked }}
- Expires: {{ expires_at }}

Renew your POS license: {{ renewal_url }}