---
template_type: affiliate_account_approved
category: Affiliate Program
---

# Email Template: affiliate_account_approved

## Subject
🎉 {{ shop_name }} 아フィリエイト 프로그램에 오신 것을 환영합니다!

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
          🎉 Application Approved!
        </mj-text>
        <mj-text font-size="18px" color="#6c757d" align="center">
          Welcome to our affiliate program
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Success Banner -->
    <mj-section background-color="#28a745" padding="40px 20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#ffffff" align="center">
          You're Now an Affiliate!
        </mj-text>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-top="10px">
          Start earning commissions today
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          Hi {{ affiliate_name }},
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Congratulations! Your application to join the {{ shop_name }} affiliate program has been approved.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          You can now start promoting our products and earning commissions on every sale you generate.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- How it Works -->
    <mj-section background-color="#f8f9fa" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="#212529" align="center" padding-bottom="10px">
          How It Works
        </mj-text>
        <mj-text font-size="14px" color="#6c757d">
          1. Get your unique affiliate links from the dashboard<br/>
          2. Share these links with your audience<br/>
          3. Earn commissions when people buy through your links<br/>
          4. Receive payouts according to your payment schedule
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          Access Affiliate Dashboard
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          Questions? <a href="mailto:{{ support_email }}" style="color: #007bff;">Contact Support</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 {{ shop_name }} 아フィ리エイト 프로그램에 오신 것을 환영합니다!

{{ affiliate_name }}님,

축하합니다! {{ shop_name }} 아フィ리에이트 프로그램에 가입 신청이 승인되었습니다.

이제 저희 제품을 홍보하여 판매를 통해 수수료를 받을 수 있습니다.

사용 방법:
1. 대시보드에서 고유한 아フィ리에이트 링크를 받으세요
2. 이 링크를 대중과 공유하세요
3. 사람들이 링크를 통해 구매할 때 수수료를 받으세요
4. 지급 일정에 따라 수수료를 받으세요

대시보드에 접속: {{ portal_url }}

{{ shop_name }}
문의 사항이 있으면 {{ support_email }}으로 연락주세요.