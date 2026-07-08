---
template_type: return_received
category: Returns
---

# Email Template: return_received

## Subject
Chúng tôi đã nhận được đơn hoàn trả của bạn - Đơn hàng #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#eff6ff' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.primary|default:'#1d4ed8' }}">
          Đơn hoàn trả đã nhận
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.primary|default:'#1d4ed8' }}">
          Đơn hàng #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Chào {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Chúng tôi đã nhận được các mặt hàng hoàn trả của bạn cho đơn hàng <strong>#{{ order_number }}</strong>.
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>Điều gì sẽ xảy ra tiếp theo:</strong>
        </mj-text>

        <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          1. Nhóm của chúng tôi sẽ kiểm tra các mặt hàng hoàn trả trong vòng 2-3 ngày làm việc<br/>
          2. Chúng tôi sẽ xác minh các mặt hàng vẫn ở trong tình trạng ban đầu<br/>
          3. Sau khi kiểm tra hoàn tất, chúng tôi sẽ xử lý hoàn tiền của bạn<br/>
          4. Bạn sẽ nhận được email xác nhận khi hoàn tiền được xử lý
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Số tiền hoàn lại sẽ được ghi lại vào phương thức thanh toán ban đầu của bạn và có thể mất 5-10 ngày làm việc để hiển thị trên tài khoản của bạn.
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Cảm ơn bạn đã kiên nhẫn!
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Đơn hoàn trả đã nhận - Đơn hàng #{{ order_number }}

Chào {{ customer_name }},

Chúng tôi đã nhận được các mặt hàng hoàn trả của bạn cho đơn hàng #{{ order_number }}.

Điều gì sẽ xảy ra tiếp theo:
1. Nhóm của chúng tôi sẽ kiểm tra các mặt hàng hoàn trả trong vòng 2-3 ngày làm việc
2. Chúng tôi sẽ xác minh các mặt hàng vẫn ở trong tình trạng ban đầu
3. Sau khi kiểm tra hoàn tất, chúng tôi sẽ xử lý hoàn tiền của bạn
4. Bạn sẽ nhận được email xác nhận khi hoàn tiền được xử lý

Số tiền hoàn lại sẽ được ghi lại vào phương thức thanh toán ban đầu của bạn và có thể mất 5-10 ngày làm việc để hiển thị trên tài khoản của bạn.

Cảm ơn bạn đã kiên nhẫn!