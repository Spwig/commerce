---
template_type: pos_license_expiration_warning
category: POS
---

# Email Template: pos_license_expiration_warning

## Subject
{% if is_grace_period %}[유예 기간] POS 라이선스 - {{ days_remaining }}일 남음{% else %}[곧 만료] POS 라이선스 - {{ days_remaining }}일 남음{% endif %}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{% if is_grace_period %}#fef2f2{% else %}#fffbeb{% endif %}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{% if is_grace_period %}#991b1b{% else %}#92400e{% endif %}" align="center">
          {% if is_grace_period %}POS 라이선스 유예 기간{% else %}POS 라이선스 곧 만료{% endif %}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {% if is_grace_period %}Spwig POS 라이선스 유예 기간이 <strong>{{ days_remaining }}일{{ days_remaining|pluralize }}</strong> 후에 만료됩니다. 유예 기간이 끝나면 POS API 접근이 차단됩니다.{% else %}Spwig POS 라이선스가 <strong>{{ days_remaining }}일{{ days_remaining|pluralize }}</strong> 후에 만료됩니다.{% endif %}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              라이선스 정보:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>라이선스:</strong> {{ license_key_masked }}<br/>
              <strong>만료일:</strong> {{ expires_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ renewal_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          POS 라이선스 갱신
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
{% if is_grace_period %}POS 라이선스 유예 기간{% else %}POS 라이선스 곧 만료{% endif %}

{% if is_grace_period %}Spwig POS 라이선스 유예 기간이 {{ days_remaining }}일{{ days_remaining|pluralize }} 후에 만료됩니다. 유예 기간이 끝나면 POS API 접근이 차단됩니다.{% else %}Spwig POS 라이선스가 {{ days_remaining }}일{{ days_remaining|pluralize }} 후에 만료됩니다.{% endif %}

라이선스 정보:
- 라이선스: {{ license_key_masked }}
- 만료일: {{ expires_at }}

POS 라이선스 갱신: {{ renewal_url }}