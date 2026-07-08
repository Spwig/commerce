---
template_type: subscription_trial_ending
category: Subscriptions
---

# Email Template: subscription_trial_ending

## Subject
⏰ Uji Coba {{ plan_name }} Anda Akan Berakhir dalam {{ days_remaining }} Hari - {{ shop_name }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          ⏰ Uji Coba Akan Segera Berakhir
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          Uji coba {{ plan_name }} Anda akan berakhir pada {{ trial_end_date|date:"F d, Y" }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Trial Info Card -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-wrapper background-color="#fff7ed" padding="30px" border="2px solid {{ theme.color.warning|default:'#f59e0b' }}" border-radius="12px">
          <mj-section background-color="transparent">
            <mj-column>
              <mj-text font-size="48px" font-weight="bold" color="#ea580c" align="center" padding-bottom="10px">
                {{ days_remaining }}
              </mj-text>
              <mj-text font-size="16px" color="#9a3412" align="center" text-transform="uppercase" letter-spacing="1px">
                Hari yang Tersisa
              </mj-text>

              <mj-divider border-color="#fed7aa" border-width="1px" padding="20px 0" />

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>Trial Ends:</strong> {{ trial_end_date|date:"F d, Y at g:i A" }}
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>First Charge:</strong> {{ subscription_amount }} pada {{ trial_end_date|date:"F d, Y" }}
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>Payment Method:</strong> {{ payment_method }}
              </mj-text>
            </mj-column>
          </mj-section>
        </mj-wrapper>
      </mj-column>
    </mj-section>

    <!-- What Happens Next -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="20px" font-weight="600" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="15px">
          Apa yang Terjadi Selanjutnya?
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.info|default:'#3b82f6' }}; font-size: 18px; margin-right: 8px;">•</span>
          Langganan Anda akan secara otomatis dilanjutkan setelah uji coba
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.info|default:'#3b82f6' }}; font-size: 18px; margin-right: 8px;">•</span>
          Kami akan membebankan {{ subscription_amount }} ke {{ payment_method }} Anda
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.info|default:'#3b82f6' }}; font-size: 18px; margin-right: 8px;">•</span>
          Anda dapat membatalkan kapan saja sebelum {{ trial_end_date|date:"F d, Y" }} tanpa biaya
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Buttons -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="10px 20px 30px 20px">
      <mj-column>
        <mj-button href="{{ manage_subscription_url }}" background-color="{{ theme.color.info|default:'#3b82f6' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" font-weight="600" border-radius="6px" padding="14px 32px">
          Kelola Langganan
        </mj-button>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="15px">
          <a href="{{ cancel_subscription_url }}" style="color: {{ theme.color.error|default:'#ef4444' }}; text-decoration: underline;">
            Batalkan Sebelum Uji Coba Berakhir
          </a>
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support Block -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          Membutuhkan bantuan? Hubungi kami di {{ support_email }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Spwig Branding Footer -->
    <mj-section padding="15px 0 10px 0" background-color="transparent">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" border-width="1px" padding="0 0 12px 0"></mj-divider>
        <mj-text align="center" padding="0" font-size="11px" color="#9ca3af" line-height="16px">
          <a href="https://spwig.com" style="color: #9ca3af; text-decoration: none; display: inline-flex; align-items: center; gap: 4px;" target="_blank">
            <img src="{{ shop_url }}/static/email_system/img/spwig-favicon.png" alt="Spwig" width="12" height="12" style="vertical-align: middle; display: inline-block;" />
            Powered by Spwig
          </a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⏰ Uji Coba Akan Segera Berakhir

Uji coba {{ plan_name }} Anda akan berakhir pada {{ trial_end_date|date:"F d, Y" }}

INFO UJI COBA:
{{ days_remaining }} Hari yang Tersisa

Trial Ends: {{ trial_end_date|date:"F d, Y at g:i A" }}
First Charge: {{ subscription_amount }} pada {{ trial_end_date|date:"F d, Y" }}
Payment Method: {{ payment_method }}

Apa yang Terjadi Selanjutnya?
• Langganan Anda akan secara otomatis dilanjutkan setelah uji coba
• Kami akan membebankan {{ subscription_amount }} ke {{ payment_method }} Anda
• Anda dapat membatalkan kapan saja sebelum {{ trial_end_date|date:"F d, Y" }} tanpa biaya

Kelola Langganan: {{ manage_subscription_url }}
Batalkan Sebelum Uji Coba Berakhir: {{ cancel_subscription_url }}

Membutuhkan bantuan? Hubungi kami di {{ support_email }}

---
Powered by Spwig - https://spwig.com