---
template_type: digital_product_download_expired
category: Digital Products
---

# Email Template: digital_product_download_expired

## Subject
ダウンロードリンクが期限切れになりました - 注文 #{{ order_number }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.error|default:'#ef4444' }}" padding="20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          ダウンロードリンクが期限切れになりました
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Main Content -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          こんにちは {{ customer_name }}、
        </mj-text>
        <mj-text>
          注文 #{{ order_number }} から {{ product_name }} のダウンロードリンクが期限切れになりました。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Expired Information -->
    <mj-section background-color="#fef2f2" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="14px" color="#991b1b">
          セキュリティ上の理由で、購入後 {{ expiration_days }} 日後にダウンロードリンクが期限切れになります。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Request New Link -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold">
          新しいダウンロードリンクが必要ですか？
        </mj-text>
        <mj-text>
          アカウントにログインして、またはサポートチームに連絡して新しいダウンロードリンクをリクエストできます。
        </mj-text>
        <mj-button href="{{ account_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" padding="15px 30px" border-radius="6px">
          マイアカウントへ
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Support -->
    <mj-section>
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          質問はありますか？ {{ support_email }} までご連絡ください
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
ダウンロードリンクが期限切れになりました

こんにちは {{ customer_name }}、

注文 #{{ order_number }} から {{ product_name }} のダウンロードリンクが期限切れになりました。

ダウンロードリンクは購入後 {{ expiration_days }} 日後に期限切れになります（セキュリティ上の理由）。

新しいダウンロードリンクが必要ですか？
アカウントにログインして、またはサポートチームに連絡して新しいダウンロードリンクをリクエストできます。

マイアカウントへ: {{ account_url }}

質問はありますか？ {{ support_email }} までご連絡ください