---
template_type: subscription_plan_downgraded
category: Subscriptions
---

# Email Template: subscription_plan_downgraded

## Subject
Gói đăng ký của bạn đã được thay đổi thành {{ new_plan_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          Gói Đã Thay Đổi
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Gói Đăng Ký Đã Được Cập Nhật
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Chào {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Gói đăng ký của bạn đã được thay đổi thành {{ new_plan_name }}.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Chi Tiết Thay Đổi Gói:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Gói Trước:</strong> {{ old_plan_name }}<br/>
              <strong>Gói Mới:</strong> {{ new_plan_name }}<br/>
              <strong>Thay Đổi Vào:</strong> {{ downgrade_date }}<br/>
              <strong>Áp Dụng:</strong> {{ effective_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Những Thay Đổi Gì:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ plan_changes }}
        </mj-text>

        {% if features_lost %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              Các Tính Năng Không Còn Có Thể Sử Dụng:
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ features_lost }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Thông Tin Hóa Đơn:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Giá Mới:</strong> {{ new_price }} / {{ billing_period }}<br/>
              <strong>Ngày Áp Dụng:</strong> {{ effective_date }}<br/>
              <strong>Ngày Hóa Đơn Tiếp Theo:</strong> {{ next_billing_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if credit_applied %}
        <mj-spacer height="20px" />
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              💰 Một khoản tín dụng {{ credit_amount }} đã được áp dụng vào tài khoản của bạn cho phần chưa sử dụng của gói trước.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Bạn Đã Thay Đổi Ý Kiến?
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color_secondary|default:'#6b7280' }}" align="center">
          Bạn có thể nâng cấp trở lại {{ old_plan_name }} bất kỳ lúc nào.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-button href="{{ upgrade_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Nâng Cấp Gói
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ account_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Xem Gói Đăng Ký Của Tôi
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
GÓI ĐÃ THAY ĐỔI

Gói Đăng Ký Đã Được Cập Nhật

Chào {{ customer_name }},

Gói đăng ký của bạn đã được thay đổi thành {{ new_plan_name }}.

CHI TIẾT THAY ĐỔI GÓI:
- Gói Trước: {{ old_plan_name }}
- Gói Mới: {{ new_plan_name }}
- Thay Đổi Vào: {{ downgrade_date }}
- Áp Dụng: {{ effective_date }}

NHỮNG THAY ĐỔI GÌ:
{{ plan_changes }}

{% if features_lost %}
TÍNH NĂNG KHÔNG CÒN CÓ THỂ SỬ DỤNG:
{{ features_lost }}
{% endif %}

THÔNG TIN HÓA ĐƠN:
- Giá Mới: {{ new_price }} / {{ billing_period }}
- Ngày Áp Dụng: {{ effective_date }}
- Ngày Hóa Đơn Tiếp Theo: {{ next_billing_date }}

{% if credit_applied %}
💰 Một khoản tín dụng {{ credit_amount }} đã được áp dụng vào tài khoản của bạn cho phần chưa sử dụng của gói trước.
{% endif %}

BẠN ĐÃ THAY ĐỔI Ý KIẾN?
Bạn có thể nâng cấp trở lại {{ old_plan_name }} bất kỳ lúc nào.

Nâng cấp gói: {{ upgrade_url }}
Xem gói đăng ký của tôi: {{ account_url }}