---
template_type: hosted_termination_warning
category: License
---

# Email Template: hosted_termination_warning

## Subject
重要: 7日以内にデータが削除されます - {{ store_name }}

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
          データ削除の警告
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
          あなたのストア <strong>{{ store_name }}</strong> および関連するすべてのデータは <strong>{{ termination_date }}</strong> に永久に削除されます。この操作は取り消すことができません。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What You Can Do -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          あなたが行えること
        </mj-text>
        <mj-text font-size="14px">
          データを保持したい場合は、この日までにデータをエクスポートするか、サブスクリプションを再アクティベートして削除を防ぐことができます。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="サブスクリプションを再アクティベート" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
データ削除の警告 - {{ store_name }}

こんにちは {{ name|default:'there' }},

あなたのストア {{ store_name }} およびすべての関連データは {{ termination_date }} に永久に削除されます。この操作は取り消すことができません。

あなたが行えること:
データを保持したい場合は、この日までにデータをエクスポートするか、サブスクリプションを再アクティベートして削除を防ぐことができます。

サブスクリプションを再アクティベート: https://spwig.com/account

お手伝いが必要ですか？ {{ support_email }} にご連絡ください