---
template_type: affiliate_account_approved
category: Affiliate Program
---

# Email Template: affiliate_account_approved

## Subject
🎉 {{ shop_name }} アフィリエイトプログラムへようこそ！

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
          🎉 アプリケーションが承認されました！
        </mj-text>
        <mj-text font-size="18px" color="#6c757d" align="center">
          会社のアフィリエイトプログラムへようこそ
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Success Banner -->
    <mj-section background-color="#28a745" padding="40px 20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#ffffff" align="center">
          今やアフィリエイターとして活動できます！
        </mj-text>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-top="10px">
          今日から収益化を開始してください
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
          おめでとうございます！{{ shop_name }} アフィリエイトプログラムへのご申請が承認されました。
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          今や、弊社の製品を宣伝し、ご提供されたすべての販売で手数料を獲得できます。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- How it Works -->
    <mj-section background-color="#f8f9fa" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="#212529" align="center" padding-bottom="10px">
          仕組み
        </mj-text>
        <mj-text font-size="14px" color="#6c757d">
          1. ダッシュボードから独自のアフィリエイトリンクを取得<br/>
          2. これらのリンクをあなたのオーディエンスと共有<br/>
          3. 人々がリンクを通じて購入するときに手数料を獲得<br/>
          4. 支払い日程に応じて手数料を受領
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          アフィリエイトダッシュボードへアクセス
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          質問は？ <a href="mailto:{{ support_email }}" style="color: #007bff;">サポートへお問い合わせ</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 {{ shop_name }} アフィリエイトプログラムへようこそ！

こんにちは {{ affiliate_name }}、

おめでとうございます！{{ shop_name }} アフィリエイトプログラムへのご申請が承認されました。

今や、弊社の製品を宣伝し、ご提供されたすべての販売で手数料を獲得できます。

仕組み：
1. ダッシュボードから独自のアフィリエイトリンクを取得
2. これらのリンクをあなたのオーディエンスと共有
3. 人々がリンクを通じて購入するときに手数料を獲得
4. 支払い日程に応じて手数料を受領

ダッシュボードへアクセス：{{ portal_url }}

{{ shop_name }}
質問は？{{ support_email }} へお問い合わせください。