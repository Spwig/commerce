---
template_type: translation_job_completed
category: Translation Service
---

# Email Template: translation_job_completed

## Subject
✓ Перевод завершён: {{ content_type }} ({{ language_count }} языков)

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          ✓ Перевод завершён!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Ваши переводы готовы
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Отличные новости! Ваша работа по пакетному переводу выполнена успешно.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Обзор задания:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Job ID:</strong> {{ job_id }}<br/>
              <strong>Content Type:</strong> {{ content_type }}<br/>
              <strong>Languages:</strong> {{ target_languages }}<br/>
              <strong>Items Translated:</strong> {{ items_translated }}<br/>
              <strong>Total Words:</strong> {{ word_count }}<br/>
              <strong>Completed:</strong> {{ completed_at }}<br/>
              <strong>Duration:</strong> {{ job_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Качество перевода:
        </mj-text>

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#065f46">
              <strong>Средний балл качества:</strong> {{ quality_score }}%<br/>
              <strong>Высокое качество:</strong> {{ high_quality_count }} элементов<br/>
              <strong>Рекомендуется проверить:</strong> {{ review_needed_count }} элементов
            </mj-text>
          </mj-column>
        </mj-section>

        {% if review_needed_count > 0 %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ Рекомендуется проверить
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ review_needed_count }} переводов получили оценку ниже 85% и должны быть проверены перед публикацией.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Дальнейшие действия:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Проверьте переводы в панели администратора<br/>
          2. Отредактируйте переводы, которые требуют доработки<br/>
          3. Опубликуйте переводы, чтобы они стали доступны<br/>
          4. Многоязычный контент станет доступен для клиентов
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ review_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Проверить переводы
        </mj-button>

        {% if can_publish_all %}
        <mj-spacer height="10px" />
        <mj-button href="{{ publish_all_url }}" background-color="#059669" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Опубликовать всё
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ ПЕРЕВОД ЗАВЕРШЁН!

Ваши переводы готовы

Отличные новости! Ваша работа по пакетному переводу выполнена успешно.

ОБЗОР ЗАДАНИЯ:
- Job ID: {{ job_id }}
- Content Type: {{ content_type }}
- Languages: {{ target_languages }}
- Items Translated: {{ items_translated }}
- Total Words: {{ word_count }}
- Completed: {{ completed_at }}
- Duration: {{ job_duration }}

КАЧЕСТВО ПЕРЕВОДА:
- Средний балл качества: {{ quality_score }}%
- Высокое качество: {{ high_quality_count }} элементов
- Рекомендуется проверить: {{ review_needed_count }} элементов

{% if review_needed_count > 0 %}
⚠️ РЕКОМЕНДУЕТСЯ ПРОВЕРИТЬ:
{{ review_needed_count }} переводов получили оценку ниже 85% и должны быть проверены перед публикацией.
{% endif %}

ДАЛЬНЕЙШИЕ ДЕЙСТВИЯ:
1. Проверьте переводы в панели администратора
2. Отредактируйте переводы, которые требуют доработки
3. Опубликуйте переводы, чтобы они стали доступны
4. Многоязычный контент станет доступен для клиентов

Проверить переводы: {{ review_url }}
{% if can_publish_all %}Опубликовать всё: {{ publish_all_url }}{% endif %}