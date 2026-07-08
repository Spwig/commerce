---
template_type: pos_license_expiration_warning
category: POS
---

# Email Template: pos_license_expiration_warning

## Subject
{% if is_grace_period %}[Thời gian ân hạn] Giấy phép POS - {{ days_remaining }} ngày còn lại{% else %}[Sắp hết hạn] Giấy phép POS - {{ days_remaining }} ngày còn lại{% endif %}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{% if is_grace_period %}#fef2f2{% else %}#fffbeb{% endif %}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{% if is_grace_period %}#991b1b{% else %}#92400e{% endif %}" align="center">
          {% if is_grace_period %}Thời gian ân hạn giấy phép POS{% else %}Giấy phép POS sắp hết hạn{% endif %}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {% if is_grace_period %}Thời gian ân hạn giấy phép POS của bạn sẽ hết hạn sau <strong>{{ days_remaining }} ngày{{ days_remaining|pluralize }}</strong>. Sau khi thời gian ân hạn kết thúc, quyền truy cập API POS sẽ bị chặn.{% else %}Giấy phép POS của bạn sẽ hết hạn sau <strong>{{ days_remaining }} ngày{{ days_remaining|pluralize }}</strong>.{% endif %}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Chi tiết giấy phép:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Giấy phép:</strong> {{ license_key_masked }}<br/>
              <strong>Hết hạn:</strong> {{ expires_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ renewal_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Gia hạn giấy phép POS
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
{% if is_grace_period %}THỜI GIAN ÂN HẠN GIẤY PHÉP POS{% else %}GIẤY PHÉP POS SẮP HẾT HẠN{% endif %}

{% if is_grace_period %}Thời gian ân hạn giấy phép POS của bạn sẽ hết hạn sau {{ days_remaining }} ngày{{ days_remaining|pluralize }}. Sau khi thời gian ân hạn kết thúc, quyền truy cập API POS sẽ bị chặn.{% else %}Giấy phép POS của bạn sẽ hết hạn sau {{ days_remaining }} ngày{{ days_remaining|pluralize }}.{% endif %}

CHI TIẾT GIẤY PHÉP:
- Giấy phép: {{ license_key_masked }}
- Hết hạn: {{ expires_at }}

Gia hạn giấy phép POS: {{ renewal_url }}