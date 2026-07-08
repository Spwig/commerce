---
template_type: backup_restore_failed
category: Backups
---

# Email Template: backup_restore_failed

## Subject
🚨 严重：{{ shop_name }} 备份还原失败

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef2f2">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#dc2626" align="center">
          🚨 严重：备份还原失败
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#1f2937' }}" font-weight="bold">
          你好 {{ admin_name }}，
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          一个关键的备份还原操作失败了。您的商店可能处于不一致的状态，需要立即处理。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              还原详情：
            </mj-text>
            <mj-text color="#7f1d1d">
              <strong>备份文件：</strong>{{ backup_filename }}<br/>
              <strong>开始时间：</strong>{{ restore_started_at }}<br/>
              <strong>失败时间：</strong>{{ restore_failed_at }}<br/>
              <strong>持续时间：</strong>{{ restore_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          错误详情：
        </mj-text>

        <mj-section background-color="#f9fafb" border-radius="4px" padding="15px">
          <mj-column>
            <mj-text font-family="'Courier New', monospace" font-size="13px" color="#dc2626">
              {{ error_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#92400e">
              🚨 立即行动所需：
            </mj-text>
            <mj-text color="#92400e">
              1. <strong>不要</strong>对商店进行任何更改<br/>
              2. 检查数据库连接和完整性<br/>
              3. 查看错误日志以获取详细的堆栈跟踪<br/>
              4. 立即联系技术支持<br/>
              5. 考虑回滚到已知良好的状态
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          查看还原日志
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ support_url }}" background-color="#92400e" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          联系紧急支持
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 严重：备份还原失败

你好 {{ admin_name }}，

一个关键的备份还原操作失败了。您的商店可能处于不一致的状态，需要立即处理。

还原详情：
- 备份文件：{{ backup_filename }}
- 开始时间：{{ restore_started_at }}
- 失败时间：{{ restore_failed_at }}
- 持续时间：{{ restore_duration }}

错误详情：
{{ error_message }}

🚨 立即行动所需：
1. 不要对商店进行任何更改
2. 检查数据库连接和完整性
3. 查看错误日志以获取详细的堆栈跟踪
4. 立即联系技术支持
5. 考虑回滚到已知良好的状态

查看还原日志：{{ admin_backup_url }}
联系紧急支持：{{ support_url }}