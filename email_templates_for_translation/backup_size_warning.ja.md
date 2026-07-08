---
template_type: backup_size_warning
category: Backups
---

# Email Template: backup_size_warning

## Subject
⚠️ バックアップサイズ警告 - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ バックアップサイズ警告
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          こんにちは {{ admin_name }}、
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ shop_name }} の最近のバックアップは推奨されたサイズのしきい値を超過しています。これはデータストレージの需要が増加していることを示している可能性があります。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              バックアップ情報:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Current Size:</strong> {{ backup_size }}<br/>
              <strong>Warning Threshold:</strong> {{ size_threshold }}<br/>
              <strong>Growth Since Last Week:</strong> {{ size_increase }}<br/>
              <strong>Backup Date:</strong> {{ backup_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          推奨アクション:
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          1. バックアップ保持ポリシーを確認する<br/>
          2. 古いバックアップのアーカイブを検討する<br/>
          3. メディアライブラリに不要な大容量ファイルがあるか確認する<br/>
          4. ストレージ容量のニーズを評価する<br/>
          5. バックアップの成長傾向をモニタリングする
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          バックアップを管理する
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ BACKUP SIZE WARNING

こんにちは {{ admin_name }}、

{{ shop_name }} の最近のバックアップは推奨されたサイズのしきい値を超過しています。これはデータストレージの需要が増加していることを示している可能性があります。

BACKUP INFORMATION:
- Current Size: {{ backup_size }}
- Warning Threshold: {{ size_threshold }}
- Growth Since Last Week: {{ size_increase }}
- Backup Date: {{ backup_date }}

RECOMMENDED ACTIONS:
1. Review backup retention policy
2. Consider archiving old backups
3. Check for unnecessary large files in media library
4. Evaluate storage capacity needs
5. Monitor backup growth trend

Manage backups: {{ admin_backup_url }}