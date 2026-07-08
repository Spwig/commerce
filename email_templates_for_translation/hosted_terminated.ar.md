---
template_type: hosted_terminated
category: License
---

# Email Template: hosted_terminated

## Subject
تم إزالة المتجر - {{ store_name }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="#374151" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          تم إزالة المتجر
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          أهلاً {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          تم إزالة متجرك <strong>{{ store_name }}</strong> بشكل دائم.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Data Backup Info -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          نسخة احتياطية للبيانات
        </mj-text>
        <mj-text font-size="14px">
          سيتم توفير نسخة احتياطية من بياناتك لمدة 90 يومًا عند الطلب. تواصل مع <strong>support@spwig.com</strong> إذا كنت بحاجة إلى تصدير البيانات.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Thank You -->
    <mj-section>
      <mj-column>
        <mj-text>
          شكرًا لكونك عميلًا في Spwig. نتمنى أن نراك مرة أخرى في المستقبل.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
تم إزالة المتجر - {{ store_name }}

أهلاً {{ name|default:'there' }},

تم إزالة متجرك {{ store_name }} بشكل دائم.

نسخة احتياطية للبيانات:
سيتم توفير نسخة احتياطية من بياناتك لمدة 90 يومًا عند الطلب. تواصل مع support@spwig.com إذا كنت بحاجة إلى تصدير البيانات.

شكرًا لكونك عميلًا في Spwig. نتمنى أن نراك مرة أخرى في المستقبل.

هل تحتاج إلى مساعدة؟ تواصل مع {{ support_email }}