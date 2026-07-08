---
template_type: account_invitation
category: Core E-commerce
---

# Email Template: account_invitation

## Subject
{{ site_name }}でアカウントを作成してください

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
          インビテーションを受けました！
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ site_name }}でアカウントを作成してください
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          こんにちは {{ customer_name }}、
        </mj-text>
        <mj-text>
          以前はゲストとしてお買い物いただいていました。アカウントを作成すると、注文履歴の確認、より速いチェックアウト、限定特典など、さまざまなメリットが得られます。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Order History Summary -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          あなたの購入履歴
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          注文数: {{ total_orders }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          総購入額: {{ total_spent }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Benefits -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          アカウントを作成する理由
        </mj-text>
        <mj-text font-size="14px">
          - 注文を追跡し、注文履歴を確認
        </mj-text>
        <mj-text font-size="14px">
          - 保存された詳細でより速いチェックアウト
        </mj-text>
        <mj-text font-size="14px">
          - 住所や設定を管理
        </mj-text>
        <mj-text font-size="14px">
          - 限定特典やプロモーションにアクセス
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=activation_url text="Create Your Account" %}

    <!-- Note -->
    <mj-section>
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          このリンクは、アカウントのパスワードを設定するために使用されます。既存の注文履歴は保持されます。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
アカウントを作成するようご招待いたします！

こんにちは {{ customer_name }}、

以前はゲストとしてお買い物いただいていました。アカウントを作成すると、注文履歴の確認、より速いチェックアウト、限定特典など、さまざまなメリットが得られます。

あなたの購入履歴:
- 注文数: {{ total_orders }}
- 総購入額: {{ total_spent }}

アカウントを作成する理由:
- 注文を追跡し、注文履歴を確認
- 保存された詳細でより速いチェックアウト
- 住所や設定を管理
- 限定特典やプロモーションにアクセス

アカウントを作成: {{ activation_url }}

このリンクは、アカウントのパスワードを設定するために使用されます。既存の注文履歴は保持されます。

お手伝いが必要ですか？ {{ support_email }}にご連絡ください。