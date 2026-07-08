---
template_type: hosted_onboarding_tips
category: License
---

# Email Template: hosted_onboarding_tips

## Subject
Mẹo để tận dụng tối đa {{ store_name }}

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
          Mẹo bắt đầu
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Tận dụng tối đa cửa hàng Spwig của bạn
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
          Bây giờ khi <strong>{{ store_name }}</strong> đã hoạt động, đây là một số mẹo giúp bạn tận dụng tối đa cửa hàng của bạn.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 1: Theme -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Tùy chỉnh giao diện
        </mj-text>
        <mj-text font-size="14px">
          Truy cập <strong>Thiết kế > Cài đặt chủ đề</strong> để chọn chủ đề, tải lên logo của bạn và thiết lập màu sắc thương hiệu. Cửa hàng của bạn sẽ được cập nhật ngay lập tức để bạn có thể xem trước các thay đổi theo thời gian thực.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 2: Products -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Thêm sản phẩm của bạn
        </mj-text>
        <mj-text font-size="14px">
          Truy cập <strong>Kho > Sản phẩm</strong> để bắt đầu thêm các mặt hàng của bạn. Bạn có thể tạo các biến thể sản phẩm (kích thước, màu sắc), thiết lập giá cả, quản lý tồn kho và tải lên hình ảnh chất lượng cao.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 3: Payments -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Thiết lập thanh toán
        </mj-text>
        <mj-text font-size="14px">
          Truy cập <strong>Cài đặt > Nhà cung cấp thanh toán</strong> để kết nối Stripe, PayPal hoặc phương thức thanh toán khác. Bạn có thể bật nhiều nhà cung cấp để khách hàng có thể thanh toán theo cách họ mong muốn.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 4: Shipping -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Cấu hình vận chuyển
        </mj-text>
        <mj-text font-size="14px">
          Tại <strong>Cài đặt > Vận chuyển</strong>, thiết lập các khu vực vận chuyển và mức giá. Bạn có thể tạo các quy tắc vận chuyển theo mức cố định, theo trọng lượng hoặc miễn phí cho các khu vực khác nhau.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 5: SEO -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Nâng cao SEO
        </mj-text>
        <mj-text font-size="14px">
          Spwig tự động tạo bản đồ trang web và thẻ meta. Truy cập <strong>Cài đặt > SEO</strong> để tùy chỉnh tiêu đề trang, mô tả và hình ảnh chia sẻ mạng xã hội giúp khách hàng dễ dàng tìm thấy cửa hàng của bạn.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Đi đến bảng điều khiển" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Mẹo bắt đầu - {{ store_name }}

Chào {{ name|default:'there' }},

Bây giờ khi {{ store_name }} đã hoạt động, đây là một số mẹo giúp bạn tận dụng tối đa cửa hàng của bạn.

1. Tùy chỉnh giao diện
Truy cập Thiết kế > Cài đặt chủ đề để chọn chủ đề, tải lên logo của bạn và thiết lập màu sắc thương hiệu.

2. Thêm sản phẩm của bạn
Truy cập Kho > Sản phẩm để bắt đầu thêm các mặt hàng của bạn với các biến thể, giá cả và hình ảnh.

3. Thiết lập thanh toán
Truy cập Cài đặt > Nhà cung cấp thanh toán để kết nối Stripe, PayPal hoặc phương thức thanh toán khác.

4. Cấu hình vận chuyển
Tại Cài đặt > Vận chuyển, thiết lập các khu vực vận chuyển và mức giá cho các khu vực khác nhau.

5. Nâng cao SEO
Truy cập Cài đặt > SEO để tùy chỉnh tiêu đề trang, mô tả và hình ảnh chia sẻ mạng xã hội giúp khách hàng dễ dàng tìm thấy cửa hàng của bạn.

Đi đến bảng điều khiển: {{ admin_url }}

Cần hỗ trợ? Liên hệ {{ support_email }}