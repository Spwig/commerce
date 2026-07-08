---
template_type: pos_license_expiration_warning
category: POS
---

# Email Template: pos_license_expiration_warning

## Subject
{% if is_grace_period %}[寬限期] POS 授權 - 剩餘 {{ days_remaining }} 天{% else %}[即將到期] POS 授權 - 剩餘 {{ days_remaining }} 天{% endif %}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{% if is_grace_period %}#fef2f2{% else %}#fffbeb{% endif %}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{% if is_grace_period %}#991b1b{% else %}#92400e{% endif %}" align="center">
          {% if is_grace_period %}POS 授權寬限期{% else %}POS 授權即將到期{% endif %}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {% if is_grace_period %}您的 Spwig POS 授權寬限期將在 <strong>{{ days_remaining }} 天{{ days_remaining|pluralize }}</strong> 後結束。一旦寬限期結束，POS API 的存取將被限制。{% else %}您的 Spwig POS 授權將在 <strong>{{ days_remaining }} 天{{ days_remaining|pluralize }}</strong> 後到期。{% endif %}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              授權細節：
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>授權：</strong> {{ license_key_masked }}<br/>
              <strong>到期日：</strong> {{ expires_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ renewal_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          繼續 POS 授權
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
{% if is_grace_period %}POS 授權寬限期{% else %}POS 授權即將到期{% endif %}

{% if is_grace_period %}您的 Spwig POS 授權寬限期將在 {{ days_remaining }} 天{{ days_remaining|pluralize }} 後結束。一旦寬限期結束，POS API 的存取將被限制。{% else %}您的 Spwig POS 授權將在 {{ days_remaining }} 天{{ days_remaining|pluralize }} 後到期。{% endif %}

LICENSE DETAILS:
- License: {{ license_key_masked }}
- Expires: {{ expires_at }}

Renew your POS license: {{ renewal_url }}