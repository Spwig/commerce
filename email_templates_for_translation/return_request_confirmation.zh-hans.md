---
template_type: return_request_confirmation
category: Returns
---

# Email Template: return_request_confirmation

## Subject
退货申请已收到 - 订单 #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#eff6ff' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1e40af' }}">
          退货申请已收到
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1e40af' }}">
          订单 #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          你好 {{ customer_name }}，
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          我们已收到你针对订单 <strong>#{{ order_number }}</strong> 的退货申请。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              退货详情：
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>原因：</strong> {{ return_reason }}<br/>
              <strong>商品：</strong> {{ items_count }} 件商品<br/>
              <strong>状态：</strong> {{ return_status }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          接下来会发生什么？
        </mj-text>

        <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          1. 我们的团队将在 24-48 小时内审核你的退货申请<br/>
          2. 一旦批准，我们会通过电子邮件将退货运输标签发送给你<br/>
          3. 将商品安全打包并附上退货标签<br/>
          4. 将包裹送到最近的快递点<br/>
          5. 一旦我们收到并检查商品，将处理你的退款
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          如果你有任何问题，请随时联系我们。
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
退货申请已收到
订单 #{{ order_number }}

你好 {{ customer_name }}，

我们已收到你针对订单 #{{ order_number }} 的退货申请。

退货详情：
- 原因：{{ return_reason }}
- 商品：{{ items_count }} 件商品
- 状态：{{ return_status }}

接下来会发生什么？
1. 我们的团队将在 24-48 小时内审核你的退货申请
2. 一旦批准，我们会通过电子邮件将退货运输标签发送给你
3. 将商品安全打包并附上退货标签
4. 将包裹送到最近的快递点
5. 一旦我们收到并检查商品，将处理你的退款

如果你有任何问题，请随时联系我们。