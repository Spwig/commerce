---
template_type: backup_storage_quota_alert
category: Backups
---

# Email Template: backup_storage_quota_alert

## Subject
🚨 存储配额关键 - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef2f2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#dc2626" align="center">
          🚨 存储配额关键
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          你好 {{ admin_name }}，
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>紧急:</strong> 您的备份存储空间即将耗尽。如果未释放存储空间，未来的备份可能会失败。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              存储状态:
            </mj-text>
            <mj-text color="#7f1d1d">
              <strong>已使用:</strong> {{ storage_used }} of {{ storage_total }}<br/>
              <strong>使用率:</strong> {{ storage_percentage }}%<br/>
              <strong>可用空间:</strong> {{ storage_available }}<br/>
              <strong>状态:</strong> <span style="color: #dc2626; font-weight: bold;">{{ storage_status }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#92400e">
              需立即采取的措施:
            </mj-text>
            <mj-text color="#92400e">
              1. 删除不再需要的旧备份<br/>
              2. 将备份归档到外部存储
              3. 增加存储配额/容量
              4. 审查备份保留策略
              5. 在问题解决前每天监控存储空间
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          立即管理存储空间
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 存储配额关键

你好 {{ admin_name }}，

紧急: 您的备份存储空间即将耗尽。如果未释放存储空间，未来的备份可能会失败。

存储状态:
- 已使用: {{ storage_used }} of {{ storage_total }}
- 使用率: {{ storage_percentage }}%
- 可用空间: {{ storage_available }}
- 状态: {{ storage_status }}

需立即采取的措施:
1. 删除不再需要的旧备份
2. 将备份归档到外部存储
3. 增加存储配额/容量
4. 审查备份保留策略
5. 在问题解决前每天监控存储空间

立即管理存储空间: {{ admin_backup_url }}