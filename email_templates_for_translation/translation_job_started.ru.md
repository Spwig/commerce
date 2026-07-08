---
template_type: translation_job_started
category: Translation Service
---

# Email Template: translation_job_started

## Subject
🌐 Началась работа по переводу: {{ content_type }} ({{ source_language }} → {{ target_languages }})

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          🌐 Началась работа по переводу
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Перевод в режиме "пакета" обрабатывается
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Ваша работа по переводу в режиме "пакета" началась и сейчас обрабатывается.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Детали работы:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Job ID:</strong> {{ job_id }}<br/>
              <strong>Content Type:</strong> {{ content_type }}<br/>
              <strong>Source Language:</strong> {{ source_language }}<br/>
              <strong>Target Languages:</strong> {{ target_languages }}<br/>
              <strong>Items to Translate:</strong> {{ item_count }}<br/>
              <strong>Started:</strong> {{ started_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Оценочное время завершения:
        </mj-text>

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#065f46" font-weight="bold" align="center">
              {{ estimated_completion }}
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              (Based on {{ word_count }} words)
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Что будет дальше:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Услуга AI-перевода обрабатывает ваш контент<br/>
          2. Переводы сохраняются как черновики для проверки<br/>
          3. Вы получите электронное письмо, когда работа будет завершена<br/>
          4. Проверьте и опубликуйте переводы в своем админ-панели
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ job_status_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Просмотреть статус работы
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Вы можете закрыть это письмо. Мы уведомим вас, когда перевод будет завершен.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🌐 РАБОТА ПО ПЕРЕВОДУ НАЧАЛАСЬ

Перевод в режиме "пакета" обрабатывается

Ваша работа по переводу в режиме "пакета" началась и сейчас обрабатывается.

ДЕТАЛИ РАБОТЫ:
- Job ID: {{ job_id }}
- Content Type: {{ content_type }}
- Source Language: {{ source_language }}
- Target Languages: {{ target_languages }}
- Items to Translate: {{ item_count }}
- Started: {{ started_at }}

ОЦЕНКА ВРЕМЕНИ ЗАВЕРШЕНИЯ:
{{ estimated_completion }}
(Based on {{ word_count }} words)

ЧТО БУДЕТ ДАЛЬШЕ:
1. Услуга AI-перевода обрабатывает ваш контент
2. Переводы сохраняются как черновики для проверки
3. Вы получите электронное письмо, когда работа будет завершена
4. Проверьте и опубликуйте переводы в своем админ-панели

Просмотреть статус работы: {{ job_status_url }}

Вы можете закрыть это письмо. Мы уведомим вас, когда перевод будет завершен.