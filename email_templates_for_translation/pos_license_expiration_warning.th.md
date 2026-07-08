---
template_type: pos_license_expiration_warning
category: POS
---

# Email Template: pos_license_expiration_warning

## Subject
{% if is_grace_period %}[ช่วงเวลาอภัยโทษ] ใบอนุญาต POS - เหลือ {{ days_remaining }} วัน{% else %}[ใกล้หมดอายุ] ใบอนุญาต POS - เหลือ {{ days_remaining }} วัน{% endif %}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{% if is_grace_period %}#fef2f2{% else %}#fffbeb{% endif %}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{% if is_grace_period %}#991b1b{% else %}#92400e{% endif %}" align="center">
          {% if is_grace_period %}ช่วงเวลาอภัยโทษของใบอนุญาต POS{% else %}ใบอนุญาต POS ใกล้หมดอายุ{% endif %}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {% if is_grace_period %}ช่วงเวลาอภัยโทษของใบอนุญาต Spwig POS ของคุณจะหมดใน <strong>{{ days_remaining }} วัน{{ days_remaining|pluralize }}</strong>. เมื่อช่วงเวลาอภัยโทษสิ้นสุด ระบบจะบล็อกการเข้าถึง API POS.{% else %}ใบอนุญาต Spwig POS ของคุณจะหมดใน <strong>{{ days_remaining }} วัน{{ days_remaining|pluralize }}</strong>.{% endif %}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              รายละเอียดใบอนุญาต:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>License:</strong> {{ license_key_masked }}<br/>
              <strong>Expires:</strong> {{ expires_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ renewal_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          ต่ออายุใบอนุญาต POS
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
{% if is_grace_period %}ช่วงเวลาอภัยโทษของใบอนุญาต POS{% else %}ใบอนุญาต POS ใกล้หมดอายุ{% endif %}

{% if is_grace_period %}ช่วงเวลาอภัยโทษของใบอนุญาต Spwig POS ของคุณจะหมดใน {{ days_remaining }} วัน{{ days_remaining|pluralize }}. เมื่อช่วงเวลาอภัยโทษสิ้นสุด ระบบจะบล็อกการเข้าถึง API POS.{% else %}ใบอนุญาต Spwig POS ของคุณจะหมดใน {{ days_remaining }} วัน{{ days_remaining|pluralize }}.{% endif %}

รายละเอียดใบอนุญาต:
- License: {{ license_key_masked }}
- Expires: {{ expires_at }}

ต่ออายุใบอนุญาต POS: {{ renewal_url }}