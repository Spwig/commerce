---
template_type: shipping_delayed
category: Shipping
---

# Email Template: shipping_delayed

## Subject
Cập nhật đơn hàng #{{ order_number }} - Giao hàng chậm

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Cập nhật đơn hàng của bạn
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Chào {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Chúng tôi muốn thông báo về sự chậm trễ trong đơn hàng của bạn. Chúng tôi xin lỗi vì sự bất tiện này và cảm ơn bạn đã kiên nhẫn.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Chi tiết đơn hàng:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Số đơn hàng:</strong> {{ order_number }}<br/>
              <strong>Thời gian giao hàng ban đầu:</strong> {{ original_delivery_date }}<br/>
              <strong>Thời gian giao hàng mới:</strong> {{ new_delivery_date }}<br/>
              <strong>Số theo dõi:</strong> {{ tracking_number }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Lý do chậm trễ:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ delay_reason }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Theo dõi đơn hàng của bạn
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          Chúng tôi đang nỗ lực hết sức để giao đơn hàng đến bạn càng sớm càng tốt. Bạn sẽ nhận được cập nhật thêm khi gói hàng của bạn đang trên đường.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Có câu hỏi? <a href="{{ support_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Liên hệ với nhóm dịch vụ khách hàng của chúng tôi</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Cập nhật đơn hàng #{{ order_number }}

Chào {{ customer_name }},

Chúng tôi muốn thông báo về sự chậm trễ trong đơn hàng của bạn. Chúng tôi xin lỗi vì sự bất tiện này và cảm ơn bạn đã kiên nhẫn.

CHI TIẾT ĐƠN HÀNG:
- Số đơn hàng: {{ order_number }}
- Thời gian giao hàng ban đầu: {{ original_delivery_date }}
- Thời gian giao hàng mới: {{ new_delivery_date }}
- Số theo dõi: {{ tracking_number }}

LÝ DO CHẬM TRỄ:
{{ delay_reason }}

Theo dõi đơn hàng của bạn: {{ tracking_url }}

Chúng tôi đang nỗ lực hết sức để giao đơn hàng đến bạn càng sớm càng tốt. Bạn sẽ nhận được cập nhật thêm khi gói hàng của bạn đang trên đường.

Có câu hỏi? Liên hệ với nhóm dịch vụ khách hàng của chúng tôi: {{ support_url }}

---
Cập nhật này dành cho đơn hàng #{{ order_number }} tại {{ shop_name }}.