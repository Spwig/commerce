---
template_type: hosted_provision_failed
category: License
---

# Email Template: hosted_provision_failed

## Subject
アクションが必要 - {{ store_name }}のストア設定の問題

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
    <mj-section background-color="{{ theme.color.error|default:'#dc2626' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          ストア設定の問題
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
          ストア {{ store_name }} の設定中に問題が発生しました。弊社のチームが通知され、対応中です。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Error Details -->
    <mj-section background-color="#fef2f2" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="14px" font-weight="bold" color="#991b1b" padding-bottom="10px">
          何が起こったか
        </mj-text>
        <mj-text font-size="14px" color="#7f1d1d">
          {{ provision_error }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What's Next -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          次に何が起こるか？
        </mj-text>
        <mj-text font-size="14px">
          この問題について、弊社のサポートチームが自動的に通知されています。ご対応は必要ありません。問題が解決した後、弊社からご連絡いたします。
        </mj-text>
        <mj-text font-size="14px" padding-top="10px">
          その間、ご質問があれば、どうぞお気軽にお問い合わせください。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
ストア設定の問題 - {{ store_name }}

こんにちは {{ name|default:'there' }}、

ストア {{ store_name }} の設定中に問題が発生しました。弊社のチームが通知され、対応中です。

何が起こったか:
{{ provision_error }}

次に何が起こるか？
この問題について、弊社のサポートチームが自動的に通知されています。ご対応は必要ありません。問題が解決した後、弊社からご連絡いたします。

その間、ご質問があれば、どうぞお気軽にお問い合わせください。

お手伝いが必要ですか？ {{ support_email }} にご連絡ください。