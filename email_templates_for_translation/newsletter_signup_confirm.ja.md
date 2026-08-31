---
template_type: newsletter_signup_confirm
category: Newsletter
---

# Email Template: newsletter_signup_confirm

## Subject
{{ store_name }}への登録を確認してください

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          登録を確認してください
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ store_name }}からのお知らせを登録していただきありがとうございます! 今後、当社のアップデートや特典を受け取るには、メールアドレスの確認をお願いします。
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ confirmation_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          登録を確認
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              ボタンがクリックできない場合、このリンクをブラウザに貼り付けてください:<br/>
              <span style="color: {{ theme.color.primary|default:'#2563eb' }}; font-family: 'Courier New', monospace;">{{ confirmation_url }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>確認が必要な理由</strong><br/>
          メールアドレスの確認により、本当に当社のアップデートを受けたいかを確認し、受信箱をスパムフリーに保つお手伝いをしています。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          ご登録いただいていない場合は、このメールを無視してかまいません。
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
{{ store_name }}への登録を確認してください

{{ store_name }}からのお知らせを登録していただきありがとうございます! 今後、当社のアップデートや特典を受け取るには、メールアドレスの確認をお願いします。

{{ confirmation_url }}

メールアドレスの確認により、本当に当社のアップデートを受けたいかを確認し、受信箱をスパムフリーに保つお手伝いをしています。

ご登録いただいていない場合は、このメールを無視してかまいません。