---
template_type: loyalty_tier_demotion_warning
category: Loyalty Program
---

# Email Template: loyalty_tier_demotion_warning

## Subject
⚠️ Trạng thái {{ current_tier }} của bạn sắp hết hạn - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Trạng thái cấp bậc sắp hết hạn
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Đừng đánh mất lợi ích {{ current_tier }} của bạn!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Chào {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Trạng thái cấp bậc {{ current_tier }} của bạn sẽ hết hạn vào {{ expiry_date }} nếu bạn không duy trì mức độ hoạt động.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              Trạng thái hiện tại:
            </mj-text>
            <mj-text color="#7f1d1d">
              <strong>Current Tier:</strong> {{ current_tier }}<br/>
              <strong>Expires:</strong> {{ expiry_date }} ({{ days_remaining }} days)<br/>
              <strong>Next Tier:</strong> {{ next_tier }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Cách duy trì trạng thái {{ current_tier }} của bạn:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          Bạn cần {{ requirement_type }} trước {{ expiry_date }}:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
              {{ requirement_description }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
              Hiện tại: {{ current_progress }} | Cần: {{ required_amount }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Lợi ích bạn sẽ mất:
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {% for benefit in tier_benefits %}
          • {{ benefit }}<br/>
          {% endfor %}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ shop_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Mua sắm ngay & duy trì trạng thái của bạn
        </mj-button>

        <mj-spacer height="20px" />

        <mj-button href="{{ loyalty_dashboard_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Xem đầy đủ thông tin
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ TRẠNG THÁI CẤP BẬC SẮP HẾT HẠN

Đừng đánh mất lợi ích {{ current_tier }} của bạn!

Chào {{ customer_name }},

Trạng thái cấp bậc {{ current_tier }} của bạn sẽ hết hạn vào {{ expiry_date }} nếu bạn không duy trì mức độ hoạt động.

TRẠNG THÁI HIỆN TẠI:
- Cấp bậc hiện tại: {{ current_tier }}
- Hết hạn: {{ expiry_date }} ({{ days_remaining }} ngày)
- Cấp bậc tiếp theo: {{ next_tier }}

CÁCH DUY TRÌ TRẠNG THÁI {{ current_tier }} CỦA BẠN:
Bạn cần {{ requirement_type }} trước {{ expiry_date }}:

{{ requirement_description }}
Hiện tại: {{ current_progress }} | Cần: {{ required_amount }}

LỢI ÍCH BẠN SẼ MẤT:
{% for benefit in tier_benefits %}
• {{ benefit }}
{% endfor %}

Mua sắm ngay & duy trì trạng thái của bạn: {{ shop_url }}
Xem đầy đủ thông tin: {{ loyalty_dashboard_url }}

