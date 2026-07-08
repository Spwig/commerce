---
template_type: backup_storage_quota_alert
category: Backups
---

# Email Template: backup_storage_quota_alert

## Subject
🚨 バックアップストレージ容量が限界に達しました - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef2f2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#dc2626" align="center">
          🚨 ストレージ容量が限界に達しました
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          こんにちは {{ admin_name }}、
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>緊急:</strong> バックアップストレージの容量が極めて低くなっています。ストレージ容量を解放しない場合、将来的なバックアップが失敗する可能性があります。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              ストレージの状態:
            </mj-text>
            <mj-text color="#7f1d1d">
              <strong>使用量:</strong> {{ storage_used }} of {{ storage_total }}<br/>
              <strong>利用率:</strong> {{ storage_percentage }}%<br/>
              <strong>空き容量:</strong> {{ storage_available }}<br/>
              <strong>状態:</strong> <span style="color: #dc2626; font-weight: bold;">{{ storage_status }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#92400e">
              即時対応が必要です:
            </mj-text>
            <mj-text color="#92400e">
              1. 必要のない古いバックアップを削除<br/>
              2. バックアップを外部ストレージにアーカイブ<br/>
              3. ストレージのクォータ/容量を拡張<br/>
              4. バックアップ保持ポリシーを確認<br/>
              5. 解決するまで毎日のストレージのモニタリング
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          今すぐストレージを管理
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 ストレージ容量が限界に達しました

こんにちは {{ admin_name }}、

緊急: バックアップストレージの容量が極めて低くなっています。ストレージ容量を解放しない場合、将来的なバックアップが失敗する可能性があります。

ストレージの状態:
- 使用量: {{ storage_used }} of {{ storage_total }}
- 利用率: {{ storage_percentage }}%
- 空き容量: {{ storage_available }}
- 状態: {{ storage_status }}

即時対応が必要です:
1. 必要のない古いバックアップを削除
2. バックアップを外部ストレージにアーカイブ
3. ストレージのクォータ/容量を拡張
4. バックアップ保持ポリシーを確認
5. 解決するまで毎日のストレージのモニタリング

ストレージを今すぐ管理: {{ admin_backup_url }}