---
template_type: pos_license_expiration_warning
category: POS
---

# Email Template: pos_license_expiration_warning

## Subject
{% if is_grace_period %}[Грейс-период] Лицензия POS - осталось {{ days_remaining }} дней{% else %}[Скоро истечет] Лицензия POS - осталось {{ days_remaining }} дней{% endif %}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{% if is_grace_period %}#fef2f2{% else %}#fffbeb{% endif %}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{% if is_grace_period %}#991b1b{% else %}#92400e{% endif %}" align="center">
          {% if is_grace_period %}Грейс-период лицензии POS{% else %}Скоро истечет лицензия POS{% endif %}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {% if is_grace_period %}Грейс-период вашей лицензии Spwig POS истечет через <strong>{{ days_remaining }} день{{ days_remaining|pluralize }}</strong>. После окончания грейс-периода доступ к API POS будет заблокирован.{% else %}Ваша лицензия Spwig POS истечет через <strong>{{ days_remaining }} день{{ days_remaining|pluralize }}</strong>.{% endif %}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Детали лицензии:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Лицензия:</strong> {{ license_key_masked }}<br/>
              <strong>Истекает:</strong> {{ expires_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ renewal_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Продлить лицензию POS
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
{% if is_grace_period %}ГРЕЙС-ПЕРИОД ЛИЦЕНЗИИ POS{% else %}ЛИЦЕНЗИЯ POS СКОРО ИСТИЧЕТ{% endif %}

{% if is_grace_period %}Грейс-период вашей лицензии Spwig POS истечет через {{ days_remaining }} день{{ days_remaining|pluralize }}. После окончания грейс-периода доступ к API POS будет заблокирован.{% else %}Ваша лицензия Spwig POS истечет через {{ days_remaining }} день{{ days_remaining|pluralize }}.{% endif %}

ДЕТАЛИ ЛИЦЕНЗИИ:
- Лицензия: {{ license_key_masked }}
- Истекает: {{ expires_at }}

Продлите свою лицензию POS: {{ renewal_url }}