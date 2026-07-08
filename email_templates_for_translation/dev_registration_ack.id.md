---
template_type: dev_registration_ack
category: Developer Portal
---

# Email Template: dev_registration_ack

## Subject
Kami telah menerima aplikasi pengembang Anda, {{ developer_name }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Aplikasi Diterima!
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          Kami sedang meninjau aplikasi pengembang Anda
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Hai {{ developer_name }},
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="20px">
          Terima kasih telah mendaftar ke Program Pengembang Spwig. Kami telah menerima aplikasi Anda dan tim kami akan segera meninjau.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What's Next Section -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="15px">
          Apa yang terjadi selanjutnya?
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="10px">
          <strong>1.</strong> Tim kami meninjau aplikasi Anda (biasanya 2-3 hari kerja)
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="10px">
          <strong>2.</strong> Anda akan menerima email dengan keputusan kami
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>3.</strong> Setelah disetujui, Anda akan mendapatkan akses penuh ke dashboard pengembang
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ portal_url }}" border-radius="6px" font-size="16px" font-weight="bold" padding="15px 30px">
          Lihat Portal Pengembang
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" padding-bottom="20px"></mj-divider>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          <strong>Portal Pengembang Spwig</strong>
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          Pertanyaan? Hubungi dukungan pengembang
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Hai {{ developer_name }},

Terima kasih telah mendaftar ke Program Pengembang Spwig. Kami telah menerima aplikasi Anda dan tim kami akan segera meninjau.

Apa yang terjadi selanjutnya?
1. Tim kami meninjau aplikasi Anda (biasanya 2-3 hari kerja)
2. Anda akan menerima email dengan keputusan kami
3. Setelah disetujui, Anda akan mendapatkan akses penuh ke dashboard pengembang

Lihat Portal Pengembang: {{ portal_url }}

---
Portal Pengembang Spwig