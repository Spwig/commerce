---
template_type: hosted_suspended
category: License
---

# Email Template: hosted_suspended

## Subject
ストアの一時停止 - {{ store_name }}

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
    <mj-section background-color="#dc2626" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          アカウントの一時停止
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }}
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
          未払いの請求書のため、あなたのストア <strong>{{ store_name }}</strong> が一時停止されました。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What This Means -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          これはどういうことか
        </mj-text>
        <mj-text font-size="14px">
          あなたのストアは今、読み取り専用モードになっています。顧客は閲覧できますが、注文は無効になっています。あなたのデータは安全で、30日間保存されます。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reactivate -->
    <mj-section>
      <mj-column>
        <mj-text>
          全アクセスを復元するには、支払い方法を更新し、未払いの残高を清算してください。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="ストアの再開" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
アカウントの一時停止 - {{ store_name }}

こんにちは {{ name|default:'there' }},

未払いの請求書のため、あなたのストア {{ store_name }} が一時停止されました。

これはどういうことか:
あなたのストアは今、読み取り専用モードになっています。顧客は閲覧できますが、注文は無効になっています。あなたのデータは安全で、30日間保存されます。

全アクセスを復元するには、支払い方法を更新し、未払いの残高を清算してください。

ストアの再開: https://spwig.com/account

お手伝いが必要ですか？ {{ support_email }} にご連絡ください。