---
template_type: backup_storage_quota_alert
category: Backups
---

# Email Template: backup_storage_quota_alert

## Subject
🚨 儅存儲空間配額臨界 - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef2f2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#dc2626" align="center">
          🚨 儅存儲空間配額臨界
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>緊急：</strong>您的備份存儲空間極度不足。如果未釋放空間，將來的備份可能會失敗。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              存儲狀態：
            </mj-text>
            <mj-text color="#7f1d1d">
              <strong>已使用：</strong> {{ storage_used }} of {{ storage_total }}<br/>
              <strong>使用率：</strong> {{ storage_percentage }}%<br/>
              <strong>可用空間：</strong> {{ storage_available }}<br/>
              <strong>狀態：</strong> <span style="color: #dc2626; font-weight: bold;">{{ storage_status }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#92400e">
              需立即採取的措施：
            </mj-text>
            <mj-text color="#92400e">
              1. 刪除不再需要的舊備份<br/>
              2. 將備份歸檔至外部存儲<br/>
              3. 增加存儲配額/容量<br/>
              4. 檢查備份保留政策<br/>
              5. 直到問題解決，請每天監控存儲空間
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          立即管理存儲空間
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 儅存儲空間配額臨界

Hi {{ admin_name }},

緊急：您的備份存儲空間極度不足。如果未釋放空間，將來的備份可能會失敗。

存儲狀態：
- 已使用：{{ storage_used }} of {{ storage_total }}
- 使用率：{{ storage_percentage }}%
- 可用空間：{{ storage_available }}
- 狀態：{{ storage_status }}

需立即採取的措施：
1. 刪除不再需要的舊備份
2. 將備份歸檔至外部存儲
3. 增加存儲配額/容量
4. 檢查備份保留政策
5. 直到問題解決，請每天監控存儲空間

立即管理存儲空間：{{ admin_backup_url }}