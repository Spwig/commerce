---
template_type: affiliate_program_rejected
category: Affiliate Program
---

# Email Template: affiliate_program_rejected

## Subject
計畫申請更新

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
          應用程式更新
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          請問 {{ affiliate_name }}，
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          感謝您申請推廣 {{ program_name }}。
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          在審核您的申請後，我們決定目前不批准它。
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          您仍然可以推廣我們聯盟網絡中的其他計劃。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#6c757d" color="#ffffff" href="{{ portal_url }}">
          查看其他計劃
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          問題？ <a href="mailto:{{ support_email }}" style="color: #007bff;">聯繫支援</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
計畫申請更新

請問 {{ affiliate_name }}，

感謝您申請推廣 {{ program_name }}。

在審核您的申請後，我們決定目前不批准它。

您仍然可以推廣我們聯盟網絡中的其他計劃。

查看其他計劃：{{ portal_url }}

{{ shop_name }}
問題？聯繫 {{ support_email }}