---
template_type: affiliate_commission_earned
category: Affiliate Program
---

# Email Template: affiliate_commission_earned

## Subject
您赚取了 {{ commission_amount }} 的佣金！

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
          💰 佣金赚取成功！
        </mj-text>
        <mj-text font-size="18px" color="#6c757d" align="center">
          来自 {{ shop_name }} 的好消息
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Commission Display -->
    <mj-section background-color="#28a745" padding="40px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-bottom="10px">
          💵 您的佣金
        </mj-text>
        <mj-text font-size="48px" font-weight="bold" color="#ffffff" align="center" line-height="1">
          {{ commission_amount }}
        </mj-text>
        <mj-text font-size="14px" color="rgba(255, 255, 255, 0.9)" align="center" padding-top="10px">
          来自订单 #{{ order_number }}
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
          恭喜！您已从订单 #{{ order_number }} 赚取了 {{ commission_amount }} 的佣金。
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          继续推广 {{ shop_name }} 以赚取更多佣金。您产生的销售越多，赚取的佣金就越多！
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Commission Details -->
    <mj-section background-color="#f8f9fa" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          <strong>订单号：</strong>#{{ order_number }}<br/>
          <strong>佣金金额：</strong>{{ commission_amount }}<br/>
          <strong>佣金比例：</strong>{{ commission_rate }}%
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          查看联盟会员仪表板
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          有问题？<a href="mailto:{{ support_email }}" style="color: #007bff;">联系支持</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
您赚取了 {{ commission_amount }} 的佣金！

你好 {{ affiliate_name }}，

恭喜！您已从订单 #{{ order_number }} 赚取了 {{ commission_amount }} 的佣金。

佣金详情：
- 订单号：#{{ order_number }}
- 佣金金额：{{ commission_amount }}
- 佣金比例：{{ commission_rate }}%

继续推广 {{ shop_name }} 以赚取更多佣金。

查看仪表板：{{ portal_url }}

{{ shop_name }}
有问题？联系 {{ support_email }}