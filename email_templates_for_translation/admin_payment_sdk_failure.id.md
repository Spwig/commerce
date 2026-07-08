---
template_type: admin_payment_sdk_failure
category: Admin Notifications
---

# Email Template: admin_payment_sdk_failure

## Subject
Masalah Penyedia Pembayaran - SDK {{ provider_name }} Gagal Dimuat

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.warning|default:'#f59e0b' }}">
          Masalah Penyedia Pembayaran
        </mj-text>
        <mj-text>
          SDK pembayaran {{ provider_name }} gagal dimuat oleh seorang pelanggan saat checkout. Ini mungkin menunjukkan gangguan layanan dari penyedia.
        </mj-text>
        <mj-text>
          <strong>Penyedia:</strong> {{ provider_name }}
        </mj-text>
        <mj-text>
          <strong>Jenis Kesalahan:</strong> {{ error_type }}
        </mj-text>
        <mj-text>
          <strong>Waktu:</strong> {{ timestamp }}
        </mj-text>
        <mj-text>
          <strong>Jumlah Gagal (1 jam terakhir):</strong> {{ failure_count }}
        </mj-text>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Notifikasi ini dibatasi frekuensinya menjadi satu per penyedia per jam. Jika masalah ini masih berlangsung, periksa dashboard penyedia atau hubungi dukungan mereka.
        </mj-text>
        <mj-button href="{{ admin_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          Lihat Pengaturan Pembayaran
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Masalah Penyedia Pembayaran

SDK pembayaran {{ provider_name }} gagal dimuat oleh seorang pelanggan saat checkout. Ini mungkin menunjukkan gangguan layanan dari penyedia.

Penyedia: {{ provider_name }}
Jenis Kesalahan: {{ error_type }}
Waktu: {{ timestamp }}
Jumlah Gagal (1 jam terakhir): {{ failure_count }}

Notifikasi ini dibatasi frekuensinya menjadi satu per penyedia per jam. Jika masalah ini masih berlangsung, periksa dashboard penyedia atau hubungi dukungan mereka.

Lihat pengaturan pembayaran: {{ admin_url }}