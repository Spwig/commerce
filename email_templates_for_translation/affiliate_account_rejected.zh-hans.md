---
template_type: affiliate_account_rejected
category: Affiliate Program
---

# Email Template: affiliate_account_rejected

## Subject
联盟申请更新

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
          申请更新
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
          感谢你有兴趣加入 {{ shop_name }} 联盟计划。
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          在审核了你的申请后，我们决定目前不继续推进。
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          这个决定是基于我们当前的联盟计划要求，可能并不反映你的资格或潜力。
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          如果你的情况发生变化，欢迎在未来重新申请。
        </mj-text>
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
联盟申请更新

你好 {{ affiliate_name }}，

感谢你有兴趣加入 {{ shop_name }} 联盟计划。

在审核了你的申请后，我们决定目前不继续推进。

这个决定是基于我们当前的联盟计划要求，可能并不反映你的资格或潜力。

如果你的情况发生变化，欢迎在未来重新申请。

{{ shop_name }}
有问题？ 联系 {{ support_email }}