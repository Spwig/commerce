---
template_type: blog_subscription_confirmed
category: Blog
---

# Email Template: blog_subscription_confirmed

## Subject
ブログ「{{ blog_name }}」への登録を確認してください

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          登録の確認
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          こんにちは、{{ subscriber_name }}さん、
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ blog_name }}への登録ありがとうございます！登録を完了し、更新情報を開始してもらうには、メールアドレスを確認してください。
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ confirmation_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          登録を確認する
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              ボタンがクリックできない場合は、このリンクをブラウザにコピーして貼り付けてください：<br/>
              <span style="color: {{ theme.color.primary|default:'#2563eb' }}; font-family: 'Courier New', monospace;">{{ confirmation_url }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>なぜ確認が必要ですか？</strong><br/>
          メール確認は、あなたが更新情報を受信したいことを確認し、スパムを防ぐのに役立ちます。あなたのプライバシーとメールボックスは私たちにとって重要です。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          登録していない場合は、このメールを無視しても問題ありません。
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
登録の確認

こんにちは、{{ subscriber_name }}さん、

{{ blog_name }}への登録ありがとうございます！登録を完了し、更新情報を開始してもらうには、メールアドレスを確認してください。

登録を確認する: {{ confirmation_url }}

なぜ確認が必要ですか？
メール確認は、あなたが更新情報を受信したいことを確認し、スパムを防ぐのに役立ちます。あなたのプライバシーとメールボックスは私たちにとって重要です。

登録していない場合は、このメールを無視しても問題ありません。