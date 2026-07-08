---
template_type: return_received
category: Returns
---

# Email Template: return_received

## Subject
我们已收到您的退货 - 订单 #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#eff6ff' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.primary|default:'#1d4ed8' }}">
          退货已收到
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.primary|default:'#1d4ed8' }}">
          订单 #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          你好 {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          我们已收到您退回的订单 <strong>#{{ order_number }}</strong> 的商品。
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>接下来会发生什么：</strong>
        </mj-text>

        <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          1. 我们的团队将在 2-3 个工作日内检查退回的商品<br/>
          2. 我们将验证商品是否处于原始状态<br/>
          3. 检查完成后，我们将处理您的退款<br/>
          4. 退款处理完成后，您将收到一封确认邮件
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          退款将记入您原来的支付方式，可能需要 5-10 个工作日才会出现在您的账户中。
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          感谢您的耐心等待！
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
退货已收到 - 订单 #{{ order_number }}

你好 {{ customer_name }},

我们已收到您退回的订单 #{{ order_number }} 的商品。

接下来会发生什么：
1. 我们的团队将在 2-3 个工作日内检查退回的商品
2. 我们将验证商品是否处于原始状态
3. 检查完成后，我们将处理您的退款
4. 退款处理完成后，您将收到一封确认邮件

退款将记入您原来的支付方式，可能需要 5-10 个工作日才会出现在您的账户中。

感谢您的耐心等待！