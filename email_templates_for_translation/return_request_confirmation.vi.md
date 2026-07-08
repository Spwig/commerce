---
template_type: return_request_confirmation
category: Returns
---

# Email Template: return_request_confirmation

## Subject
Yêu cầu hoàn trả đã nhận - Đơn hàng #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#eff6ff' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1e40af' }}">
          Yêu cầu hoàn trả đã nhận
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1e40af' }}">
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
          Chúng tôi đã nhận được yêu cầu hoàn trả của bạn cho đơn hàng <strong>#{{ order_number }}</strong>.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Chi tiết hoàn trả:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Lý do:</strong> {{ return_reason }}<br/>
              <strong>Sản phẩm:</strong> {{ items_count }} sản phẩm<br/>
              <strong>Trạng thái:</strong> {{ return_status }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Điều gì sẽ xảy ra tiếp theo?
        </mj-text>

        <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          1. Đội ngũ của chúng tôi sẽ xem xét yêu cầu hoàn trả của bạn trong vòng 24-48 giờ<br/>
          2. Sau khi được phê duyệt, chúng tôi sẽ gửi cho bạn nhãn vận chuyển hoàn trả qua email<br/>
          3. Đóng gói các sản phẩm cẩn thận và dán nhãn hoàn trả<br/>
          4. Giao hàng tại điểm giao nhận gần nhất<br/>
          5. Hoàn tiền của bạn sẽ được xử lý sau khi chúng tôi nhận và kiểm tra các sản phẩm
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Nếu bạn có bất kỳ câu hỏi nào, vui lòng không ngần ngại liên hệ với chúng tôi.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
YÊU CẦU HOÀN TRẢ ĐÃ NHẬN
Đơn hàng #{{ order_number }}

Chào {{ customer_name }},

Chúng tôi đã nhận được yêu cầu hoàn trả của bạn cho đơn hàng #{{ order_number }}.

CHI TIẾT HOÀN TRẢ:
- Lý do: {{ return_reason }}
- Sản phẩm: {{ items_count }} sản phẩm
- Trạng thái: {{ return_status }}

ĐIỀU GÌ SẼ XẢY RA TIẾP THEO?
1. Đội ngũ của chúng tôi sẽ xem xét yêu cầu hoàn trả của bạn trong vòng 24-48 giờ
2. Sau khi được phê duyệt, chúng tôi sẽ gửi cho bạn nhãn vận chuyển hoàn trả qua email
3. Đóng gói các sản phẩm cẩn thận và dán nhãn hoàn trả
4. Giao hàng tại điểm giao nhận gần nhất
5. Hoàn tiền của bạn sẽ được xử lý sau khi chúng tôi nhận và kiểm tra các sản phẩm

Nếu bạn có bất kỳ câu hỏi nào, vui lòng không ngần ngại liên hệ với chúng tôi.