---
template_type: translation_job_completed
category: Translation Service
---

# Email Template: translation_job_completed

## Subject
✓ 翻訳完了: {{ content_type }} ({{ language_count }} 言語)

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          ✓ 翻訳完了！
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ご依頼の翻訳が完了しました
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          ご報告します！バッチ翻訳ジョブが正常に完了しました。
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              ジョブ概要：
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>ジョブID:</strong> {{ job_id }}<br/>
              <strong>コンテンツタイプ:</strong> {{ content_type }}<br/>
              <strong>言語:</strong> {{ target_languages }}<br/>
              <strong>翻訳済み項目:</strong> {{ items_translated }}<br/>
              <strong>合計文字数:</strong> {{ word_count }}<br/>
              <strong>完了日時:</strong> {{ completed_at }}<br/>
              <strong>所要時間:</strong> {{ job_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          翻訳品質：
        </mj-text>

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#065f46">
              <strong>平均品質スコア:</strong> {{ quality_score }}%<br/>
              <strong>高品質:</strong> {{ high_quality_count }} 件<br/>
              <strong>確認推奨:</strong> {{ review_needed_count }} 件
            </mj-text>
          </mj-column>
        </mj-section>

        {% if review_needed_count > 0 %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ 確認推奨
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ review_needed_count }} 件の翻訳が85％未満のスコアで、公開前に確認が必要です。
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          次の手順：
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. 管理パネルで翻訳を確認<br/>
          2. 精査が必要な翻訳を編集<br/>
          3. 翻訳を公開してライブにします<br/>
          4. あなたの多言語コンテンツは顧客に利用可能になります
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ review_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          翻訳を確認する
        </mj-button>

        {% if can_publish_all %}
        <mj-spacer height="10px" />
        <mj-button href="{{ publish_all_url }}" background-color="#059669" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          すべてを公開
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ 翻訳完了！

ご依頼の翻訳が完了しました

ご報告します！バッチ翻訳ジョブが正常に完了しました。

ジョブ概要：
- ジョブID: {{ job_id }}
- コンテンツタイプ: {{ content_type }}
- 言語: {{ target_languages }}
- 翻訳済み項目: {{ items_translated }}
- 合計文字数: {{ word_count }}
- 完了日時: {{ completed_at }}
- 所要時間: {{ job_duration }}

翻訳品質：
- 平均品質スコア: {{ quality_score }}%
- 高品質: {{ high_quality_count }} 件
- 確認推奨: {{ review_needed_count }} 件

{% if review_needed_count > 0 %}
⚠️ 確認推奨：
{{ review_needed_count }} 件の翻訳が85％未満のスコアで、公開前に確認が必要です。
{% endif %}

次の手順：
1. 管理パネルで翻訳を確認
2. 精査が必要な翻訳を編集
3. 翻訳を公開してライブにします
4. あなたの多言語コンテンツは顧客に利用可能になります

翻訳を確認する: {{ review_url }}
{% if can_publish_all %}すべてを公開: {{ publish_all_url }}{% endif %}