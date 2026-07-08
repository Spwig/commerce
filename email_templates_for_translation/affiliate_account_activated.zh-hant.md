---
template_type: affiliate_account_activated
category: Affiliate Program
---

# Email Template: affiliate_account_activated

## Subject
歡迎回來！帳號已重新啟用

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
          🎉 帳號重新啟用！
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Success Banner -->
    <mj-section background-color="#28a745" padding="40px 20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#ffffff" align="center">
          歡迎回來！
        </mj-text>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-top="10px">
          您的聯營帳號已重新啟用
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          親愛的 {{ affiliate_name }}，
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          好消息！您的 {{ shop_name }} 聯營帳號已重新啟用。
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          您可以立即恢復推廣我們的產品並賺取佣金。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          進入聯營儀表板
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          問題？<a href="mailto:{{ support_email }}" style="color: #007bff;">聯繫支援</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
歡迎回來！帳號已重新啟用

親愛的 {{ affiliate_name }}，

好消息！您的 {{ shop_name }} 聯營帳號已重新啟用。

您可以立即恢復推廣我們的產品並賺取佣金。

進入您的儀表板：{{ portal_url }}

{{ shop_name }}
問題？聯繫 {{ support_email }}