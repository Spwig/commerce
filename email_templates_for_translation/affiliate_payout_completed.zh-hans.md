---
template_type: affiliate_payout_completed
category: Affiliate Program
---

# Email Template: affiliate_payout_completed

## Subject
✓ 提款完成：{{ payout_amount }}

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
          🎉 提款完成！
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Payout Display -->
    <mj-section background-color="#28a745" padding="40px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-bottom="10px">
          ✓ 已成功付款
        </mj-text>
        <mj-text font-size="48px" font-weight="bold" color="#ffffff" align="center" line-height="1">
          {{ payout_amount }}
        </mj-text>
        <mj-text font-size="14px" color="rgba(255, 255, 255, 0.9)" align="center" padding-top="10px">
          提款 ID：{{ payout_id }}
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
          你的 {{ payout_amount }} 提款已成功完成！
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          资金已发送至你的付款方式。根据你的银行或付款处理器，可能需要 1-2 个工作日才能出现在你的账户中。
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          感谢你推广 {{ shop_name }}。继续加油！
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          查看提款详情
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          有问题？<a href="mailto:{{ support_email }}" style="color: #007bff;">
            联系支持
          </a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ 提款完成：{{ payout_amount }}

你好 {{ affiliate_name }}，

你的 {{ payout_amount }} 提款已成功完成！

提款详情：
- 提款 ID：{{ payout_id }}
- 金额：{{ payout_amount }}
- 付款方式：{{ payout_method }}

资金已发送至你的付款方式。根据你的银行或付款处理器，可能需要 1-2 个工作日才能出现在你的账户中。

感谢你推广 {{ shop_name }}。继续加油！

查看提款详情：{{ portal_url }}

{{ shop_name }}
有问题？联系 {{ support_email }}