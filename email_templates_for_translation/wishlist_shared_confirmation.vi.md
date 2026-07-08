---
template_type: wishlist_shared_confirmation
category: Wishlist
---

# Email Template: wishlist_shared_confirmation

## Subject
✓ Danh sách yêu thích của bạn đã được chia sẻ - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ✓ Danh sách yêu thích đã được chia sẻ thành công!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Chào {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Danh sách yêu thích của bạn với {{ wishlist_item_count }} mục đã được chia sẻ thành công. Người khác hiện có thể xem danh sách yêu thích của bạn bằng liên kết dưới đây.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Liên kết chia sẻ:
            </mj-text>
            <mj-text font-family="'Courier New', monospace" font-size="14px" color="{{ theme.color.primary|default:'#2563eb' }}">
              {{ share_url }}
            </mj-text>
            <mj-spacer height="15px" />
            <mj-button href="{{ share_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
              Sao chép liên kết
            </mj-button>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Nội dung được chia sẻ:
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
          • Tên danh sách yêu thích của bạn (nếu đã đặt tên)<br/>
          • {{ wishlist_item_count }} sản phẩm<br/>
          • Tên sản phẩm, hình ảnh và giá<br/>
          • Liên kết mua hàng cho từng mục
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              💡 Lý tưởng để chia sẻ với bạn bè và gia đình cho các món quà và dịp đặc biệt!
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ wishlist_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          Quản lý danh sách yêu thích của tôi
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Bạn muốn dừng chia sẻ? Bạn có thể tắt liên kết chia sẻ bất kỳ lúc nào trong <a href="{{ wishlist_settings_url }}">cài đặt danh sách yêu thích</a> của bạn.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ DANH SÁCH YÊU THÍCH ĐÃ ĐƯỢC CHIA SẺ THÀNH CÔNG!

Chào {{ customer_name }},

Danh sách yêu thích của bạn với {{ wishlist_item_count }} mục đã được chia sẻ thành công. Người khác hiện có thể xem danh sách yêu thích của bạn bằng liên kết dưới đây.

LIÊN KẾT CHIA SẺ:
{{ share_url }}

NỘI DUNG ĐƯỢC CHIA SẺ:
• Tên danh sách yêu thích của bạn (nếu đã đặt tên)
• {{ wishlist_item_count }} sản phẩm
• Tên sản phẩm, hình ảnh và giá
• Liên kết mua hàng cho từng mục

💡 Lý tưởng để chia sẻ với bạn bè và gia đình cho các món quà và dịp đặc biệt!

Quản lý danh sách yêu thích của tôi: {{ wishlist_url }}

Bạn muốn dừng chia sẻ? Bạn có thể tắt liên kết chia sẻ bất kỳ lúc nào trong cài đặt danh sách yêu thích của bạn: {{ wishlist_settings_url }}