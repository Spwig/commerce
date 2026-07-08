---
template_type: translation_job_started
category: Translation Service
---

# Email Template: translation_job_started

## Subject
🌐 バッチ翻訳ジョブが開始されました: {{ content_type }} ({{ source_language }} → {{ target_languages }})

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          🌐 バッチ翻訳ジョブが開始されました
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          バッチ翻訳が進行中です
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          ご依頼のバッチ翻訳ジョブが開始され、現在処理中です。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              ジョブの詳細:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>ジョブID:</strong> {{ job_id }}<br/>
              <strong>コンテンツタイプ:</strong> {{ content_type }}<br/>
              <strong>ソース言語:</strong> {{ source_language }}<br/>
              <strong>ターゲット言語:</strong> {{ target_languages }}<br/>
              <strong>翻訳対象アイテム数:</strong> {{ item_count }}<br/>
              <strong>開始時間:</strong> {{ started_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          予定完了時刻:
        </mj-text>

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#065f46" font-weight="bold" align="center">
              {{ estimated_completion }}
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              ({{ word_count }}語に基づく)
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          次の手順:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. AI翻訳サービスがコンテンツを処理します<br/>
          2. 翻訳内容はドラフトとして保存され、確認待ちになります<br/>
          3. ジョブが完了すると、メールでお知らせします<br/>
          4. 管理パネルから翻訳内容を確認し、公開してください
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ job_status_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          ジョブステータスを確認する
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          このメールを閉じてもかまいません。翻訳が完了すると通知します。
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🌐 バッチ翻訳ジョブが開始されました

バッチ翻訳が進行中です

ご依頼のバッチ翻訳ジョブが開始され、現在処理中です。

ジョブの詳細:
- ジョブID: {{ job_id }}
- コンテンツタイプ: {{ content_type }}
- ソース言語: {{ source_language }}
- ターゲット言語: {{ target_languages }}
- 翻訳対象アイテム数: {{ item_count }}
- 開始時間: {{ started_at }}

予定完了時刻:
{{ estimated_completion }}
({{ word_count }}語に基づく)

次の手順:
1. AI翻訳サービスがコンテンツを処理します
2. 翻訳内容はドラフトとして保存され、確認待ちになります
3. ジョブが完了すると、メールでお知らせします
4. 管理パネルから翻訳内容を確認し、公開してください

ジョブステータスを確認する: {{ job_status_url }}

このメールを閉じてもかまいません。翻訳が完了すると通知します。