---
template_type: return_request_rejected
category: Returns
---

# Email Template: return_request_rejected

## Subject
Cập nhật yêu cầu trả hàng - Đơn hàng #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#fffbeb' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#92400e' }}">
          Cập nhật yêu cầu trả hàng
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#92400e' }}">
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
          Chúng tôi đã xem xét yêu cầu trả hàng của bạn cho đơn hàng <strong>#{{ order_number }}</strong> và hiện tại không thể chấp thuận nó.
        </mj-text>

        {% if rejection_reason %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Lý do:</strong> {{ rejection_reason }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Nếu bạn có câu hỏi về quyết định này hoặc cho rằng đã có lỗi, vui lòng liên hệ với nhóm hỗ trợ của chúng tôi.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Cập nhật yêu cầu trả hàng - Đơn hàng #{{ order_number }}

Chào {{ customer_name }},

Chúng tôi đã xem xét yêu cầu trả hàng của bạn cho đơn hàng #{{ order_number }} và hiện tại không thể chấp thuận nó.

{% if rejection_reason %}Lý do: {{ rejection_reason }}{% endif %}

Nếu bạn có câu hỏi về quyết định này hoặc cho rằng đã có lỗi, vui lòng liên hệ với nhóm hỗ trợ của chúng tôi.