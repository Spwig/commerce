---
template_type: dev_account_suspended
category: Developer Portal
---

# Email Template: dev_account_suspended

## Subject
تم تعليق حساب مطورك في Spwig

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header with Warning Accent -->
    <mj-section background-color="{{ theme.color.warning|default:'#f59e0b' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          تم تعليق الحساب
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-top="10px">
          تحديث مهم حول حسابك كمطور
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          مرحبًا {{ developer_name }},
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="20px">
          تم تعليق حسابك كمطور في Spwig. خلال هذه الفترة، يظل المكونات التي نشرتها متاحة، ولكن لا يمكنك إرسال مكونات جديدة أو تحديثات.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reason Section (if provided) -->
    {% if suspension_reason %}
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="14px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="10px">
          السبب:
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="15px" background-color="{{ theme.color.background|default:'#ffffff' }}" border-left="3px solid {{ theme.color.warning|default:'#f59e0b' }}">
          {{ suspension_reason }}
        </mj-text>
      </mj-column>
    </mj-section>
    {% endif %}

    <!-- Support Section -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          إذا كنت تعتقد أن هذا تم اتخاذه بالخطأ، يرجى التواصل معنا عبر <a href="mailto:{{ support_email }}" style="color: {{ theme.color.primary|default:'#2563eb' }}; text-decoration: none;">{{ support_email }}</a>.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" padding-bottom="20px"></mj-divider>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          <strong>بوابة مطور Spwig</strong>
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          لديك أسئلة؟ تواصل مع دعم المطورين
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
مرحبًا {{ developer_name }},

تم تعليق حسابك كمطور في Spwig. خلال هذه الفترة، يظل المكونات التي نشرتها متاحة، ولكن لا يمكنك إرسال مكونات جديدة أو تحديثات.

{% if suspension_reason %}السبب: {{ suspension_reason }}{% endif %}

إذا كنت تعتقد أن هذا تم اتخاذه بالخطأ، يرجى التواصل معنا عبر {{ support_email }}.

---
بوابة مطور Spwig