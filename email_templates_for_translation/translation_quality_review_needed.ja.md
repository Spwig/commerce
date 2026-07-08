---
template_type: translation_quality_review_needed
category: Translation Service
---

# Email Template: translation_quality_review_needed

## Subject
⚠️ 低品質な翻訳が検出されました: {{ content_type }} - {{ low_quality_count }} 件の確認が必要

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ 翻訳品質のアラート
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          確認が必要
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          ご翻訳の作業が完了しましたが、{{ low_quality_count }} 件の翻訳が品質の閾値を下回っており、公開前に確認が必要です。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              作業概要:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Job ID:</strong> {{ job_id }}<br/>
              <strong>Content Type:</strong> {{ content_type }}<br/>
              <strong>Total Items:</strong> {{ total_items }}<br/>
              <strong>Average Quality:</strong> {{ average_quality }}%<br/>
              <strong>Low Quality:</strong> {{ low_quality_count }} 件 ({{ low_quality_percentage }}%)
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          品質の概要:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Excellent (95-100%):</strong> {{ excellent_count }} 件<br/>
              <strong>Good (85-94%):</strong> {{ good_count }} 件<br/>
              <strong>Fair (70-84%):</strong> {{ fair_count }} 件<br/>
              <strong>Poor (&lt;70%):</strong> <span style="color: #dc2626; font-weight: bold;">{{ poor_count }} 件</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          一般的な品質の問題:
        </mj-text>

        {% for issue in quality_issues %}
        <mj-section background-color="#fef3c7" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e">
              <strong>{{ issue.type }}:</strong> {{ issue.count }} 回発生
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          おすすめのアクション:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. 管理パネルでフラグを立てた翻訳を確認する<br/>
          2. 品質が低い翻訳を手動で編集する<br/>
          3. 品質が非常に低い項目を再翻訳を検討する<br/>
          4. 確認が完了するまで公開しない
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ review_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          翻訳の確認
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ low_quality_url }}" background-color="#dc2626" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          品質の低い項目の確認
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              💡 ヒント: 85%未満の品質スコアは、文法、文脈、正確性に潜在的な問題を示しています。公開する前に、人間による確認を強くお勧めします。
            </mj-text>
          </mj-column>
        </mj-section>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ 翻訳品質のアラート

確認が必要

ご翻訳の作業が完了しましたが、{{ low_quality_count }} 件の翻訳が品質の閾値を下回っており、公開前に確認が必要です。

JOB SUMMARY:
- Job ID: {{ job_id }}
- Content Type: {{ content_type }}
- Total Items: {{ total_items }}
- Average Quality: {{ average_quality }}%
- Low Quality: {{ low_quality_count }} 件 ({{ low_quality_percentage }}%)

QUALITY BREAKDOWN:
- Excellent (95-100%): {{ excellent_count }} 件
- Good (85-94%): {{ good_count }} 件
- Fair (70-84%): {{ fair_count }} 件
- Poor (<70%): {{ poor_count }} 件

COMMON QUALITY ISSUES:
{% for issue in quality_issues %}
{{ issue.type }}: {{ issue.count }} 回発生
{% endfor %}

RECOMMENDED ACTIONS:
1. 管理パネルでフラグを立てた翻訳を確認する
2. 品質が低い翻訳を手動で編集する
3. 品質が非常に低い項目を再翻訳を検討する
4. 確認が完了するまで公開しない

Review translations: {{ review_url }}
View low quality items: {{ low_quality_url }}

💡 ヒント: 85%未満の品質スコアは、文法、文脈、正確性に潜在的な問題を示しています。公開する前に、人間による確認を強くお勧めします。