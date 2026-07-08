---
template_type: subscription_dunning_final_notice
category: Subscriptions
---

# Email Template: subscription_dunning_final_notice

## Subject
⚠️ PERINGATAN AKHIR: Langganan Anda akan dibatalkan dalam {{ days_until_cancellation }} hari

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#991b1b" align="center">
          ⚠️ PERINGATAN AKHIR
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Penangguhan Langganan Segera
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Ini adalah peringatan akhir Anda. Kami tidak dapat memproses pembayaran untuk langganan {{ plan_name }} Anda. Jika kami tidak menerima pembayaran dalam {{ days_until_cancellation }} hari, langganan Anda akan dibatalkan.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b" font-size="16px">
              ⚠️ Pembayaran Gagal - Tindakan Diperlukan
            </mj-text>
            <mj-text color="#991b1b">
              <strong>Langganan:</strong> {{ plan_name }}<br/>
              <strong>Jumlah yang Harus Dibayar:</strong> {{ amount_due }}<br/>
              <strong>Coba Gagal:</strong> {{ retry_count }}<br/>
              <strong>Coba Terakhir:</strong> {{ last_retry_date }}<br/>
              <strong>Tanggal Pembatalan:</strong> <span style="font-weight: bold; font-size: 16px;">{{ cancellation_date }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Kesalahan Pembayaran:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" font-family="monospace" color="{{ theme.color.text|default:'#4b5563' }}">
              {{ payment_error_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Apa yang Akan Terjadi:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          Jika pembayaran tidak diterima hingga {{ cancellation_date }}:<br/>
          • Langganan Anda akan dibatalkan<br/>
          • Anda akan kehilangan akses ke semua manfaat langganan<br/>
          • Data Anda mungkin dihapus (lihat kebijakan retensi)<br/>
          • Anda perlu mendaftar ulang untuk mendapatkan akses kembali
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Perbarui Metode Pembayaran Anda Sekarang
        </mj-text>

        <mj-spacer height="20px" />

        <mj-button href="{{ update_payment_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Perbarui Metode Pembayaran
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Masalah Umum & Solusi:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • <strong>Kartu Kadaluarsa:</strong> Perbarui dengan kartu kredit saat ini<br/>
          • <strong>Saldo Tidak Cukup:</strong> Pastikan saldo cukup<br/>
          • <strong>Kartu Ditolak:</strong> Hubungi bank Anda atau gunakan kartu yang berbeda<br/>
          • <strong>Mismatch Alamat:</strong> Verifikasi alamat penagihan cocok dengan kartu
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" font-weight="bold">
              Membutuhkan Bantuan?
            </mj-text>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              Jika Anda mengalami masalah pembayaran atau membutuhkan bantuan, silakan hubungi tim dukungan kami segera.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Hubungi Dukungan
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Jika Anda ingin membatalkan langganan Anda, Anda dapat melakukannya di pengaturan akun Anda.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ PERINGATAN AKHIR

Penangguhan Langganan Segera

Hi {{ customer_name }},

Ini adalah peringatan akhir Anda. Kami tidak dapat memproses pembayaran untuk langganan {{ plan_name }} Anda. Jika kami tidak menerima pembayaran dalam {{ days_until_cancellation }} hari, langganan Anda akan dibatalkan.

⚠️ PEMBAYARAN GAGAL - TINDAKAN DIPERLUKAN:
- Langganan: {{ plan_name }}
- Jumlah yang Harus Dibayar: {{ amount_due }}
- Coba Gagal: {{ retry_count }}
- Coba Terakhir: {{ last_retry_date }}
- Tanggal Pembatalan: {{ cancellation_date }}

KESALAHAN PEMBAYARAN:
{{ payment_error_message }}

APA YANG AKAN TERJADI:
Jika pembayaran tidak diterima hingga {{ cancellation_date }}:
• Langganan Anda akan dibatalkan
• Anda akan kehilangan akses ke semua manfaat langganan
• Data Anda mungkin dihapus (lihat kebijakan retensi)
• Anda perlu mendaftar ulang untuk mendapatkan akses kembali

PERBARUI METODE PEMBAYARAN SEKARANG

Masalah Umum & Solusi:
• Kartu Kadaluarsa: Perbarui dengan kartu kredit saat ini
• Saldo Tidak Cukup: Pastikan saldo cukup
• Kartu Ditolak: Hubungi bank Anda atau gunakan kartu yang berbeda
• Mismatch Alamat: Verifikasi alamat penagihan cocok dengan kartu

MEMBUTUHKAH BANTUAN?
Jika Anda mengalami masalah pembayaran atau membutuhkan bantuan, silakan hubungi tim dukungan kami segera.

Perbarui metode pembayaran: {{ update_payment_url }}
Hubungi dukungan: {{ support_url }}

Jika Anda ingin membatalkan langganan Anda, Anda dapat melakukannya di pengaturan akun Anda.