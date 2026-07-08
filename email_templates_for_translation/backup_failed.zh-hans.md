---
template_type: backup_failed
category: Backups
---

# Email Template: backup_failed

## Subject
🚨 紧急：备份失败 - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef2f2">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#dc2626" align="center">
          ⚠️ 备份失败
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#1f2937' }}">
          你好 {{ admin_name }}，
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          你的 {{ shop_name }} 商店的一个关键备份操作失败了。需要立即采取行动以确保数据保护。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              备份详情：
            </mj-text>
            <mj-text color="#7f1d1d">
              <strong>备份类型：</strong> {{ backup_type }}<br/>
              <strong>开始时间：</strong> {{ backup_started_at }}<br/>
              <strong>失败时间：</strong> {{ backup_failed_at }}<br/>
              <strong>持续时间：</strong> {{ backup_duration }}
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

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          建议操作：
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          1. 检查服务器上的可用磁盘空间<br/>
          2. 验证数据库连接性<br/>
          3. 查看错误日志以获取详细的堆栈跟踪<br/>
          4. 手动重试备份或等待下一次计划运行<br/>
          5. 如果问题仍然存在，请联系支持
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          查看备份日志
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ retry_backup_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          现在重试备份
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>最后一次成功备份：</strong> {{ last_successful_backup }}<br/>
          <strong>下次计划备份：</strong> {{ next_scheduled_backup }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 紧急：备份失败

你好 {{ admin_name }}，

你的 {{ shop_name }} 商店的一个关键备份操作失败了。需要立即采取行动以确保数据保护。

备份详情：
- 备份类型：{{ backup_type }}
- 开始时间：{{ backup_started_at }}
- 失败时间：{{ backup_failed_at }}
- 持续时间：{{ backup_duration }}

错误详情：
{{ error_message }}

建议操作：
1. 检查服务器上的可用磁盘空间
2. 验证数据库连接性
3. 查看错误日志以获取详细的堆栈跟踪
4. 手动重试备份或等待下一次计划运行
5. 如果问题仍然存在，请联系支持

查看备份日志：{{ admin_backup_url }}
现在重试备份：{{ retry_backup_url }}

最后一次成功备份：{{ last_successful_backup }}
下次计划备份：{{ next_scheduled_backup }}

---
这是针对 {{ shop_name }} 管理员的重要系统警报。