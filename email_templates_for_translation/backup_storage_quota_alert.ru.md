---
template_type: backup_storage_quota_alert
category: Backups
---

# Email Template: backup_storage_quota_alert

## Subject
🚨 Критический квота хранения резервных копий - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef2f2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#dc2626" align="center">
          🚨 Критический квота хранения резервных копий
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Здравствуйте, {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>СРОЧНО:</strong> Ваш объем хранения резервных копий критически низкий. Если не освободить место, будущие резервные копии могут завершиться неудачно.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              Статус хранения:
            </mj-text>
            <mj-text color="#7f1d1d">
              <strong>Использовано:</strong> {{ storage_used }} из {{ storage_total }}<br/>
              <strong>Использование:</strong> {{ storage_percentage }}%<br/>
              <strong>Доступно:</strong> {{ storage_available }}<br/>
              <strong>Статус:</strong> <span style="color: #dc2626; font-weight: bold;">{{ storage_status }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#92400e">
              Требуются немедленные действия:
            </mj-text>
            <mj-text color="#92400e">
              1. Удалить старые резервные копии, которые больше не нужны<br/>
              2. Архивировать резервные копии во внешнее хранилище<br/>
              3. Увеличить квоту/емкость хранения<br/>
              4. Проверить политику хранения резервных копий<br/>
              5. Ежедневно отслеживать хранение до тех пор, пока проблема не будет решена
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Управление хранилищем сейчас
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 КРИТИЧЕСКИЙ КВОТА ХРАНЕНИЯ

Здравствуйте, {{ admin_name }},

СРОЧНО: Ваш объем хранения резервных копий критически низкий. Если не освободить место, будущие резервные копии могут завершиться неудачно.

СТАТУС ХРАНЕНИЯ:
- Использовано: {{ storage_used }} из {{ storage_total }}
- Использование: {{ storage_percentage }}%
- Доступно: {{ storage_available }}
- Статус: {{ storage_status }}

ТРЕБУЮТСЯ НЕМЕДЛЕННЫЕ ДЕЙСТВИЯ:
1. Удалить старые резервные копии, которые больше не нужны
2. Архивировать резервные копии во внешнее хранилище
3. Увеличить квоту/емкость хранения
4. Проверить политику хранения резервных копий
5. Ежедневно отслеживать хранение до тех пор, пока проблема не будет решена

Управление хранилищем сейчас: {{ admin_backup_url }}