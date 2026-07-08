---
template_type: hosted_terminated
category: License
---

# Email Template: hosted_terminated

## Subject
ストアが削除されました - {{ store_name }}

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
    <mj-section background-color="#374151" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          ストアが削除されました
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
          あなたのストア <strong>{{ store_name }}</strong> は永久に削除されました。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Data Backup Info -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          データバックアップ
        </mj-text>
        <mj-text font-size="14px">
          データのバックアップは、依頼に応じて90日間保持されます。データのエクスポートが必要な場合は、<strong>support@spwig.com</strong> までご連絡ください。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Thank You -->
    <mj-section>
      <mj-column>
        <mj-text>
          Spwigの顧客としてご利用いただきありがとうございます。今後ともよろしくお願いいたします。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
ストアが削除されました - {{ store_name }}

こんにちは {{ name|default:'there' }},

あなたのストア {{ store_name }} は永久に削除されました。

データバックアップ:
データのバックアップは、依頼に応じて90日間保持されます。データのエクスポートが必要な場合は、support@spwig.com までご連絡ください。

Spwigの顧客としてご利用いただきありがとうございます。今後ともよろしくお願いいたします。

お手伝いが必要ですか？ {{ support_email }} までご連絡ください。