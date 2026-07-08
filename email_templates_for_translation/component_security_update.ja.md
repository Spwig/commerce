---
template_type: component_security_update
category: Component Updates
---

# Email Template: component_security_update

## Subject
🔒 緊急: {{ component_name }} 用のセキュリティアップデートが利用可能です

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#991b1b" align="center">
          🔒 セキュリティアップデートが必要です
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          重大なセキュリティパッチ
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ component_name }} でセキュリティ上の脆弱性が発見されました。店舗を保護するためにすぐに更新してください。
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b" font-size="16px">
              ⚠️ セキュリティ情報
            </mj-text>
            <mj-text color="#991b1b">
              <strong>コンポーネント:</strong> {{ component_name }}<br/>
              <strong>現在のバージョン:</strong> {{ current_version }}<br/>
              <strong>パッチされたバージョン:</strong> {{ patched_version }}<br/>
              <strong>深刻度:</strong> {{ severity_level }}<br/>
              <strong>CVE ID:</strong> {{ cve_id }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          脆弱性の詳細:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ vulnerability_description }}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          潜在的な影響:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ impact_description }}
        </mj-text>

        {% if mitigation_steps %}
        <mj-spacer height="30px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              一時的な緩和策
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ mitigation_steps }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          行動が必要: すぐにアップデートをインストールしてください
        </mj-text>

        <mj-spacer height="20px" />

        <mj-button href="{{ update_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          セキュリティパッチをインストール
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ advisory_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          セキュリティアドバイザリを読む
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          支援が必要な場合は、すぐにSpwigサポートに連絡してください。
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🔒 セキュリティアップデートが必要です

重大なセキュリティパッチ

{{ component_name }} でセキュリティ上の脆弱性が発見されました。店舗を保護するためにすぐに更新してください。

⚠️ セキュリティ情報:
- コンポーネント: {{ component_name }}
- 現在のバージョン: {{ current_version }}
- パッチされたバージョン: {{ patched_version }}
- 緊急度: {{ severity_level }}
- CVE ID: {{ cve_id }}

脆弱性の詳細:
{{ vulnerability_description }}

潜在的な影響:
{{ impact_description }}

{% if mitigation_steps %}
一時的な緩和策:
{{ mitigation_steps }}
{% endif %}

行動が必要: すぐにアップデートをインストールしてください

セキュリティパッチをインストール: {{ update_url }}
セキュリティアドバイザリを読む: {{ advisory_url }}

支援が必要な場合は、すぐにSpwigサポートに連絡してください。