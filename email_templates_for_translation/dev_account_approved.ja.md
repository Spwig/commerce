---
template_type: dev_account_approved
category: Developer Portal
---

# Email Template: dev_account_approved

## Subject
Spwig開発者プログラムへようこそ、{{ developer_name }}！

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header with Success Accent -->
    <mj-section background-color="{{ theme.color.success|default:'#10b981' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          Spwigへようこそ！
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-top="10px">
          開発者申請が承認されました
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          こんにちは {{ developer_name }}、
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="20px">
          おめでとうございます！あなたの開発者申請が承認されました。今後はSpwig開発者ポータルへのフルアクセスが可能になります。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Free License Section -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px 20px 0">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="10px">
          あなたの無料開発者ライセンスが待っています
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          承認された開発者として、永久更新付きの無料Spwig Shop + POSインストールが提供されます。ライセンスを取得し、あなたのサーバーにSpwigをインストールして、すぐにコンポーネントの構築を開始してください。
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="15px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.success|default:'#10b981' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ license_url }}" border-radius="6px" font-size="16px" font-weight="bold" padding="15px 30px">
          無料ライセンスを取得
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Get Started Section -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="15px">
          スタートする:
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="10px">
          <strong>1.</strong> 無料開発者ライセンスを取得
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="10px">
          <strong>2.</strong> あなたのサーバーにSpwigをインストール
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="10px">
          <strong>3.</strong> 我々のSDKを使用して最初のコンポーネントを構築
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>4.</strong> ダッシュボードから提出
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.success|default:'#10b981' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ dashboard_url }}" border-radius="6px" font-size="16px" font-weight="bold" padding="15px 30px">
          ダッシュボードへ
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" padding-bottom="20px"></mj-divider>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          <strong>Spwig開発者ポータル</strong>
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          質問は？開発者サポートにご連絡ください
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
こんにちは {{ developer_name }}、

おめでとうございます！あなたの開発者申請が承認されました。今後はSpwig開発者ポータルへのフルアクセスが可能になります。

YOUR FREE DEVELOPER LICENSE IS WAITING
承認された開発者として、永久更新付きの無料Spwig Shop + POSインストールが提供されます。ライセンスを取得し、あなたのサーバーにSpwigをインストールして、すぐにコンポーネントの構築を開始してください。

Claim your free license: {{ license_url }}

Get started:
1. Claim your free developer license: {{ license_url }}
2. Install Spwig on your server
3. Build your first component using our SDKs
4. Submit it from your dashboard

Go to Dashboard: {{ dashboard_url }}

---
Spwig Developer Portal