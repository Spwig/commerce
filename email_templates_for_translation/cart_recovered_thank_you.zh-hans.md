---
template_type: cart_recovered_thank_you
category: Cart Recovery
---

# Email Template: cart_recovered_thank_you

## Subject
感谢您的订单 #{{ order_number }}！- {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          🎉 感谢您的订单！
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          你好 {{ customer_name }}，
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          很高兴您完成了购买！您的订单已确认，我们正在为您准备发货。
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              订单摘要
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>订单编号：</strong> {{ order_number }}<br/>
              <strong>订单日期：</strong> {{ order_date }}<br/>
              <strong>总计：</strong> {{ order_total }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ order_tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          跟踪您的订单
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          接下来会发生什么？
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. 我们将准备您的订单（通常在1-2个工作日内）<br/>
          2. 您将收到带有跟踪信息的发货确认信息<br/>
          3. 您的订单将被送到：{{ shipping_address }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              💡 <strong>您知道吗？</strong><br/>
              您可以随时在账户仪表板上跟踪您的订单。
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          有问题？<a href="{{ support_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">联系我们的支持团队</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 感谢您的订单！

你好 {{ customer_name }}，

很高兴您完成了购买！您的订单已确认，我们正在为您准备发货。

订单摘要：
- 订单编号：{{ order_number }}
- 订单日期：{{ order_date }}
- 总计：{{ order_total }}

跟踪您的订单：{{ order_tracking_url }}

接下来会发生什么？
1. 我们将准备您的订单（通常在1-2个工作日内）
2. 您将收到带有跟踪信息的发货确认信息
3. 您的订单将被送到：{{ shipping_address }}

💡 您知道吗？
您可以随时在账户仪表板上跟踪您的订单。

有问题？联系我们的支持团队：{{ support_url }}

---
订单 #{{ order_number }} 在 {{ shop_name }}