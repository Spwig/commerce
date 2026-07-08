---
template_type: pos_license_expiration_warning
category: POS
---

# Email Template: pos_license_expiration_warning

## Subject
{% if is_grace_period %}[فترة السماح] رخصة POS - تبقى {{ days_remaining }} أيام{% else %}[تنتهي قريبًا] رخصة POS - تبقى {{ days_remaining }} أيام{% endif %}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{% if is_grace_period %}#fef2f2{% else %}#fffbeb{% endif %}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{% if is_grace_period %}#991b1b{% else %}#92400e{% endif %}" align="center">
          {% if is_grace_period %}فترة السماح لرخصة POS{% else %}تنتهي رخصة POS قريبًا{% endif %}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {% if is_grace_period %}تنتهي فترة السماح لرخصة Spwig POS بعد <strong>{{ days_remaining }} يوم{{ days_remaining|pluralize }}</strong>. بمجرد انتهاء فترة السماح، سيتم حظر الوصول إلى واجهة برمجة التطبيقات POS.{% else %}تنتهي رخصة Spwig POS بعد <strong>{{ days_remaining }} يوم{{ days_remaining|pluralize }}</strong>.{% endif %}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              تفاصيل الرخصة:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>رخصة:</strong> {{ license_key_masked }}<br/>
              <strong>تنتهي:</strong> {{ expires_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ renewal_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          تجديد رخصة POS
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
{% if is_grace_period %}فترة السماح لرخصة POS{% else %}تنتهي رخصة POS قريبًا{% endif %}

{% if is_grace_period %}تنتهي فترة السماح لرخصة Spwig POS بعد {{ days_remaining }} يوم{{ days_remaining|pluralize }}. بمجرد انتهاء فترة السماح، سيتم حظر الوصول إلى واجهة برمجة التطبيقات POS.{% else %}تنتهي رخصة Spwig POS بعد {{ days_remaining }} يوم{{ days_remaining|pluralize }}.{% endif %}

تفاصيل الرخصة:
- رخصة: {{ license_key_masked }}
- تنتهي: {{ expires_at }}

تجديد رخصة POS: {{ renewal_url }}