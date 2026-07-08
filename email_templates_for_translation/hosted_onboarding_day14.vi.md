---
template_type: hosted_onboarding_day14
category: License
---

# Email Template: hosted_onboarding_day14

## Subject
Tiến xa hơn - {{ store_name }}

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
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Bắt đầu: Tính năng nâng cao
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Khai thác đầy đủ tiềm năng của {{ store_name }}
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
          Bạn đã vận hành <strong>{{ store_name }}</strong> trong vài tuần nay. Dưới đây là một số tính năng nâng cao giúp bạn đưa cửa hàng của mình lên một tầm cao mới.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 1 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Thiết lập quy trình email tự động
        </mj-text>
        <mj-text font-size="14px">
          Tự động hóa giao tiếp với khách hàng thông qua các quy trình email. Thiết lập chuỗi chào mừng, theo dõi sau khi mua hàng và chiến dịch tái kết nối tại <strong>Marketing > Email Workflows</strong>.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 2 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Cấu hình quy tắc thuế cho các khu vực của bạn
        </mj-text>
        <mj-text font-size="14px">
          Đảm bảo bạn đang tính đúng thuế. Truy cập <strong>Settings > Tax</strong> để cấu hình quy tắc thuế cho mỗi khu vực bạn bán hàng. Bạn có thể thiết lập giá bao gồm thuế hoặc không bao gồm thuế.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 3 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Khám phá API để tích hợp
        </mj-text>
        <mj-text font-size="14px">
          Nếu gói của bạn bao gồm quyền truy cập API, bạn có thể tích hợp cửa hàng của mình với các công cụ và dịch vụ bên ngoài. Truy cập <strong>Settings > API</strong> để tạo khóa API và khám phá tài liệu.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 4 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Xem bảng điều khiển phân tích của bạn
        </mj-text>
        <mj-text font-size="14px">
          Theo dõi hiệu suất cửa hàng của bạn. <strong>Bảng điều khiển</strong> của bạn hiển thị các chỉ số quan trọng bao gồm doanh thu, đơn hàng, sản phẩm bán chạy và thông tin khách hàng để giúp bạn đưa ra quyết định dựa trên dữ liệu.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 5 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Xem xét thêm tính năng POS cho bán hàng tại cửa hàng
        </mj-text>
        <mj-text font-size="14px">
          Bạn cũng muốn bán hàng trực tiếp? Tính năng điểm bán hàng của Spwig cho phép bạn xử lý các giao dịch tại cửa hàng đồng bộ với kho hàng và quản lý đơn hàng trực tuyến. Truy cập <strong>Settings > Point of Sale</strong> để tìm hiểu thêm.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Explore Your Dashboard" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Bắt đầu: Tính năng nâng cao - {{ store_name }}

Chào {{ name|default:'there' }},

Bạn đã vận hành {{ store_name }} trong vài tuần nay. Dưới đây là một số tính năng nâng cao giúp bạn đưa cửa hàng của mình lên một tầm cao mới.

1. Thiết lập quy trình email tự động
Tự động hóa giao tiếp với khách hàng thông qua chuỗi chào mừng, theo dõi sau khi mua hàng và chiến dịch tái kết nối.

2. Cấu hình quy tắc thuế cho các khu vực của bạn
Đảm bảo bạn đang tính đúng thuế. Truy cập Settings > Tax để cấu hình quy tắc cho mỗi khu vực.

3. Khám phá API để tích hợp
Nếu gói của bạn bao gồm quyền truy cập API, tích hợp cửa hàng với các công cụ bên ngoài. Truy cập Settings > API để bắt đầu.

4. Xem bảng điều khiển phân tích của bạn
Bảng điều khiển hiển thị các chỉ số quan trọng bao gồm doanh thu, đơn hàng, sản phẩm bán chạy và thông tin khách hàng.

5. Xem xét thêm tính năng POS cho bán hàng tại cửa hàng
Bạn cũng muốn bán hàng trực tiếp? Tính năng điểm bán hàng của Spwig đồng bộ giao dịch tại cửa hàng với kho hàng trực tuyến.

Khám phá Bảng điều khiển của bạn: {{ admin_url }}

Cần hỗ trợ? Liên hệ {{ support_email }}