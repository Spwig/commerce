---
template_type: affiliate_commission_reversed
category: Affiliate Program
---

# Email Template: affiliate_commission_reversed

## Subject
佣金撤销 - 订单 #{{ order_number }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="#f8f9fa">
    <!-- Header -->
    <mj-section background-color="#ffffff" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="#212529" align="center">
          佣金撤销
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          你好 {{ affiliate_name }}，
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          由于客户退款，订单 #{{ order_number }} ({{ commission_amount }}) 的佣金已被撤销。
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          当客户请求退款时，任何相关佣金都会自动撤销，以确保会计准确。
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          这是联盟流程的正常部分。继续推广 {{ shop_name }} 以赚取新佣金！
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          查看联盟仪表板
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          有问题？ <a href="mailto:{{ support_email }}" style="color: #007bff;">联系支持</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
佣金撤销 - 订单 #{{ order_number }}

你好 {{ affiliate_name }}，

由于客户退款，订单 #{{ order_number }} ({{ commission_amount }}) 的佣金已被撤销。

当客户请求退款时，任何相关佣金都会自动撤销，以确保会计准确。

这是联盟流程的正常部分。继续推广 {{ shop_name }} 以赚取新佣金！

查看你的仪表板：{{ portal_url }}

{{ shop_name }}
有问题？联系 {{ support_email }}

