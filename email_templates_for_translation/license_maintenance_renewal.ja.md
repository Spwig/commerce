---
template_type: license_maintenance_renewal
category: License
---

# Email Template: license_maintenance_renewal

## Subject
メンテナンスの更新 - 注文番号 #{{ order_number }}

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
    <mj-section background-color="{{ theme.color.success|default:'#10b981' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          メンテナンスの更新！
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          注文番号 #{{ order_number }}
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
          あなたの Spwig メンテナンスサブスクリプションが正常に更新されました。今後もプラットフォームのアップデート、セキュリティパッチ、新機能を引き続き受けることができます。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Renewal Summary -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          更新概要
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          ライセンスキー: {{ license_key }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          メンテナンス有効期限: {{ renewal_expires_at }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          注文番号: {{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What's Included -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          含まれる内容
        </mj-text>
        <mj-text font-size="14px">
          有効なメンテナンスサブスクリプションにより、以下にアクセスできます:
        </mj-text>
        <mj-text font-size="14px" padding-top="5px">
          - プラットフォームの機能アップデートと改善
        </mj-text>
        <mj-text font-size="14px">
          - セキュリティパッチとバグ修正
        </mj-text>
        <mj-text font-size="14px">
          - アップグレードサーバー経由での新コンポーネントリリース
        </mj-text>
        <mj-text font-size="14px">
          - 技術サポート
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Next Steps -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          あなたの側で何かを行う必要はありません。アップデートは、管理パネルのコンポーネントアップデートシステムを通じて引き続き利用可能です。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
メンテナンスの更新！

注文番号 #{{ order_number }}

こんにちは {{ customer_name }}、

あなたの Spwig メンテナンスサブスクリプションが正常に更新されました。今後もプラットフォームのアップデート、セキュリティパッチ、新機能を引き続き受けることができます。

更新概要:
- ライセンスキー: {{ license_key }}
- メンテナンス有効期限: {{ renewal_expires_at }}
- 注文番号: {{ order_number }}

含まれる内容:
- プラットフォームの機能アップデートと改善
- セキュリティパッチとバグ修正
- アップグレードサーバー経由での新コンポーネントリリース
- 技術サポート

あなたの側で何かを行う必要はありません。アップデートは、管理パネルのコンポーネントアップデートシステムを通じて引き続き利用可能です。

お手伝いが必要ですか？ {{ support_email }} にご連絡ください。