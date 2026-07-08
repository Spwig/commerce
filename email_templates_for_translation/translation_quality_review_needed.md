---
template_type: translation_quality_review_needed
category: Translation Service
---

# Email Template: translation_quality_review_needed

## Subject
⚠️ Low quality translations detected: {{ content_type }} - {{ low_quality_count }} items need review

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Translation Quality Alert
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Review Recommended
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Your translation job completed, but {{ low_quality_count }} translations scored below the quality threshold and should be reviewed before publishing.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Job Summary:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Job ID:</strong> {{ job_id }}<br/>
              <strong>Content Type:</strong> {{ content_type }}<br/>
              <strong>Total Items:</strong> {{ total_items }}<br/>
              <strong>Average Quality:</strong> {{ average_quality }}%<br/>
              <strong>Low Quality:</strong> {{ low_quality_count }} items ({{ low_quality_percentage }}%)
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Quality Breakdown:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Excellent (95-100%):</strong> {{ excellent_count }} items<br/>
              <strong>Good (85-94%):</strong> {{ good_count }} items<br/>
              <strong>Fair (70-84%):</strong> {{ fair_count }} items<br/>
              <strong>Poor (&lt;70%):</strong> <span style="color: #dc2626; font-weight: bold;">{{ poor_count }} items</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Common Quality Issues:
        </mj-text>

        {% for issue in quality_issues %}
        <mj-section background-color="#fef3c7" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e">
              <strong>{{ issue.type }}:</strong> {{ issue.count }} occurrences
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Recommended Actions:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Review flagged translations in the admin panel<br/>
          2. Edit low-quality translations manually<br/>
          3. Consider re-translating poor quality items<br/>
          4. Publish only after review is complete
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ review_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Review Translations
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ low_quality_url }}" background-color="#dc2626" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          View Low Quality Items
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              💡 Tip: Quality scores below 85% indicate potential issues with grammar, context, or accuracy. Human review is strongly recommended before publishing.
            </mj-text>
          </mj-column>
        </mj-section>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ TRANSLATION QUALITY ALERT

Review Recommended

Your translation job completed, but {{ low_quality_count }} translations scored below the quality threshold and should be reviewed before publishing.

JOB SUMMARY:
- Job ID: {{ job_id }}
- Content Type: {{ content_type }}
- Total Items: {{ total_items }}
- Average Quality: {{ average_quality }}%
- Low Quality: {{ low_quality_count }} items ({{ low_quality_percentage }}%)

QUALITY BREAKDOWN:
- Excellent (95-100%): {{ excellent_count }} items
- Good (85-94%): {{ good_count }} items
- Fair (70-84%): {{ fair_count }} items
- Poor (<70%): {{ poor_count }} items

COMMON QUALITY ISSUES:
{% for issue in quality_issues %}
{{ issue.type }}: {{ issue.count }} occurrences
{% endfor %}

RECOMMENDED ACTIONS:
1. Review flagged translations in the admin panel
2. Edit low-quality translations manually
3. Consider re-translating poor quality items
4. Publish only after review is complete

Review translations: {{ review_url }}
View low quality items: {{ low_quality_url }}

💡 Tip: Quality scores below 85% indicate potential issues with grammar, context, or accuracy. Human review is strongly recommended before publishing.

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| job_id | Unique job identifier | TJ-2026-001234 |
| content_type | What was translated | Product Descriptions |
| total_items | Total translated items | 247 |
| average_quality | Average quality score | 87 |
| low_quality_count | Items below threshold | 32 |
| low_quality_percentage | Percentage low quality | 13 |
| excellent_count | Excellent quality items | 158 |
| good_count | Good quality items | 57 |
| fair_count | Fair quality items | 20 |
| poor_count | Poor quality items | 12 |
| quality_issues | Common issue types | [{type: 'Grammar errors', count: 18}, {type: 'Missing context', count: 14}] |
| review_url | Translation review page | https://shop.com/en/admin/translations/review/12345 |
| low_quality_url | Filtered low quality view | https://shop.com/en/admin/translations/review/12345?quality=low |

## Notes

- Admin notification - quality alert
- Sent when translation job completes with low quality scores
- Flags specific items needing review
- Provides quality score breakdown
- Lists common quality issues
- Prevents publishing of poor translations
- Actionable recommendations
- Medium priority
