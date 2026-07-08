---
template_type: hosted_onboarding_day14
category: License
---

# Email Template: hosted_onboarding_day14

## Subject
さらに詳しく - {{ store_name }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          初心者向け: 高度な機能
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }} の最大限の可能性を引き出しましょう
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          こんにちは {{ name|default:'there' }}、
        </mj-text>
        <mj-text>
          すでに {{ store_name }} を運用しているのは数週間経ちました。以下は、店舗を次のレベルに引き上げるために役立つ高度な機能です。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 1 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          自動化されたメールワークフローの設定
        </mj-text>
        <mj-text font-size="14px">
          メールワークフローで顧客とのコミュニケーションを自動化しましょう。"Marketing > Email Workflows" で、ウェルカムシーケンス、購入後のフォローアップ、リエンゲージメントキャンペーンを設定できます。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 2 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          売り場の地域ごとの税金ルールの設定
        </mj-text>
        <mj-text font-size="14px">
          正しい税率が課されているか確認してください。"Settings > Tax" にアクセスして、販売地域ごとに税金ルールを設定できます。税込価格または税抜価格の設定も可能です。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 3 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          インテグレーション用のAPIの探索
        </mj-text>
        <mj-text font-size="14px">
          ご契約プランにAPIアクセスが含まれている場合、外部ツールやサービスとストアを統合できます。"Settings > API" にアクセスして、APIキーを生成し、ドキュメントを確認してください。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 4 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          あなたの分析ダッシュボードを確認しましょう
        </mj-text>
        <mj-text font-size="14px">
          店舗のパフォーマンスを常に確認してください。"Dashboard" は、収益、注文、人気商品、顧客の洞察などの主要なメトリクスを表示し、データ駆動型の意思決定をサポートします。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 5 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          店舗での販売用にPOSを追加するか検討しましょう
        </mj-text>
        <mj-text font-size="14px">
          店舗での販売も行う場合は、SpwigのPOS機能でオンライン在庫と注文管理と同期した店舗での取引を処理できます。"Settings > Point of Sale" にアクセスして、詳しく確認してください。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="ダッシュボードを確認" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
初心者向け: 高度な機能 - {{ store_name }}

こんにちは {{ name|default:'there' }},

すでに {{ store_name }} を運用しているのは数週間経ちました。以下は、店舗を次のレベルに引き上げるために役立つ高度な機能です。

1. 自動化されたメールワークフローの設定
ウェルカムシーケンス、購入後のフォローアップ、リエンゲージメントキャンペーンで顧客とのコミュニケーションを自動化しましょう。

2. 売り場の地域ごとの税金ルールの設定
正しい税率が課されているか確認してください。"Settings > Tax" にアクセスして、販売地域ごとに税金ルールを設定できます。

3. インテグレーション用のAPIの探索
ご契約プランにAPIアクセスが含まれている場合、外部ツールとストアを統合できます。"Settings > API" にアクセスして、開始してください。

4. あなたの分析ダッシュボードを確認しましょう
"Dashboard" は、収益、注文、人気商品、顧客の洞察などの主要なメトリクスを表示し、データ駆動型の意思決定をサポートします。

5. 店舗での販売用にPOSを追加するか検討しましょう
店舗での販売も行う場合は、SpwigのPOS機能でオンライン在庫と同期した店舗での取引を処理できます。

ダッシュボードを確認: {{ admin_url }}

お手伝いが必要ですか？ {{ support_email }} にご連絡ください。