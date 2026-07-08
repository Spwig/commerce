---
template_type: hosted_cancellation_confirmation
category: License
---

# Email Template: hosted_cancellation_confirmation

## Subject
Xác nhận hủy - {{ store_name }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="#6b7280" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Xác nhận hủy
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Chào {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          Gói <strong>{{ plan_name }}</strong> của bạn đã bị hủy.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Điều gì sẽ xảy ra tiếp theo
        </mj-text>
        <mj-text font-size="14px">
          Bạn sẽ tiếp tục có quyền truy cập đầy đủ cho đến <strong>{{ access_until_date }}</strong>.
        </mj-text>
        <mj-text font-size="14px">
          Sau đó, dữ liệu cửa hàng của bạn sẽ được lưu giữ trong 30 ngày cho đến <strong>{{ termination_date }}</strong>.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Additional Info -->
    <mj-section>
      <mj-column>
        <mj-text>
          Nếu bạn muốn xuất dữ liệu trước khi quyền truy cập kết thúc, bạn có thể thực hiện từ bảng điều khiển quản trị của mình. Đổi ý rồi? Bạn có thể kích hoạt lại gói của mình bất kỳ lúc nào.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="Reactivate Subscription" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Xác nhận hủy - {{ store_name }}

Chào {{ name|default:'there' }},

Gói {{ plan_name }} của bạn đã bị hủy.

Điều gì sẽ xảy ra tiếp theo:
- Bạn sẽ tiếp tục có quyền truy cập đầy đủ cho đến {{ access_until_date }}.
- Sau đó, dữ liệu cửa hàng của bạn sẽ được lưu giữ trong 30 ngày cho đến {{ termination_date }}.

Nếu bạn muốn xuất dữ liệu trước khi quyền truy cập kết thúc, bạn có thể thực hiện từ bảng điều khiển quản trị của mình. Đổi ý rồi? Bạn có thể kích hoạt lại gói của mình bất kỳ lúc nào.

Reactivate Subscription: https://spwig.com/account

Cần hỗ trợ? Liên hệ {{ support_email }}