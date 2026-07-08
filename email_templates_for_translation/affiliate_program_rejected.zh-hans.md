---
template_type: affiliate_program_rejected
category: Affiliate Program
---

# Email Template: affiliate_program_rejected

## Subject
申请程序更新

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
          申请程序更新
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
          感谢你申请推广 {{ program_name }}。
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          在审核了你的申请后，我们决定目前不予批准。
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          你仍然可以推广我们联盟网络中的其他计划。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#6c757d" color="#ffffff" href="{{ portal_url }}">
          查看其他计划
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
申请程序更新

你好 {{ affiliate_name }}，

感谢你申请推广 {{ program_name }}。

在审核了你的申请后，我们决定目前不予批准。

你仍然可以推广我们联盟网络中的其他计划。

查看其他计划：{{ portal_url }}

{{ shop_name }}
有问题？联系 {{ support_email }}