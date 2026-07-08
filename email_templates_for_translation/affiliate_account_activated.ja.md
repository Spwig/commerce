---
template_type: affiliate_account_activated
category: Affiliate Program
---

# Email Template: affiliate_account_activated

## Subject
ようこそ戻ってきて! アフィリエイトアカウントが再アクティベートされました

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
          🎉 アフィリエイトアカウントが再アクティベートされました!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Success Banner -->
    <mj-section background-color="#28a745" padding="40px 20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#ffffff" align="center">
          ようこそ戻ってきて!
        </mj-text>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-top="10px">
          あなたのアフィリエイトアカウントは再び有効になりました
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          こんにちは {{ affiliate_name }}、
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          良いニュースです! {{ shop_name }} とのアフィリエイトアカウントが再アクティベートされました。
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          すぐに弊社製品のプロモーションを再開し、手数料を獲得できます。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          アフィリエイトダッシュボードにアクセス
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          質問は? <a href="mailto:{{ support_email }}" style="color: #007bff;">サポートに連絡</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
ようこそ戻ってきて! アフィリエイトアカウントが再アクティベートされました

こんにちは {{ affiliate_name }}、

良いニュースです! {{ shop_name }} とのアフィリエイトアカウントが再アクティベートされました。

すぐに弊社製品のプロモーションを再開し、手数料を獲得できます。

アクセスしてください: {{ portal_url }}

{{ shop_name }}
質問は? {{ support_email }} に連絡してください