---
template_type: subscription_plan_upgraded
category: Subscriptions
---

# Email Template: subscription_plan_upgraded

## Subject
✓ Gói đăng ký của bạn đã được nâng cấp!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          ✓ Gói Đã Được Nâng Cấp!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Chào mừng bạn đến với {{ new_plan_name }}
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Chào {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Gói đăng ký của bạn đã được nâng cấp thành công. Bạn hiện đang có quyền truy cập vào tất cả các lợi ích của {{ new_plan_name }}!
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Chi tiết thay đổi gói:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Gói Trước:</strong> {{ old_plan_name }}<br/>
              <strong>Gói Mới:</strong> {{ new_plan_name }}<br/>
              <strong>Ngày Nâng Cấp:</strong> {{ upgrade_date }}<br/>
              <strong>Áp dụng ngay lập tức</strong>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Những thay đổi mới:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ new_features }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Thông tin thanh toán:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Giá mới:</strong> {{ new_price }} / {{ billing_period }}<br/>
              <strong>Ngày thanh toán tiếp theo:</strong> {{ next_billing_date }}<br/>
              {% if prorated_charge %}<strong>Phí tính theo tỷ lệ hôm nay:</strong> {{ prorated_charge }}{% endif %}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if prorated_charge %}
        <mj-spacer height="20px" />
        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              💡 Bạn đã được tính phí {{ prorated_charge }} hôm nay cho phần còn lại của chu kỳ thanh toán hiện tại của bạn.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ account_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Xem Gói Đăng Ký Của Tôi
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Có câu hỏi? <a href="{{ support_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Liên hệ hỗ trợ</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ GÓI ĐÃ ĐƯỢC NÂNG CẤP!

Chào mừng bạn đến với {{ new_plan_name }}

Chào {{ customer_name }},

Gói đăng ký của bạn đã được nâng cấp thành công. Bạn hiện đang có quyền truy cập vào tất cả các lợi ích của {{ new_plan_name }}!

CHI TIẾT THAY ĐỔI GÓI:
- Gói Trước: {{ old_plan_name }}
- Gói Mới: {{ new_plan_name }}
- Ngày Nâng Cấp: {{ upgrade_date }}
- Áp dụng ngay lập tức

NHỮNG THAY ĐỔI MỚI:
{{ new_features }}

THÔNG TIN THANH TOÁN:
- Giá mới: {{ new_price }} / {{ billing_period }}
- Ngày thanh toán tiếp theo: {{ next_billing_date }}
{% if prorated_charge %}- Phí tính theo tỷ lệ hôm nay: {{ prorated_charge }}{% endif %}

{% if prorated_charge %}
💡 Bạn đã được tính phí {{ prorated_charge }} hôm nay cho phần còn lại của chu kỳ thanh toán hiện tại của bạn.
{% endif %}

Xem gói đăng ký của tôi: {{ account_url }}
Có câu hỏi? Liên hệ hỗ trợ: {{ support_url }}

