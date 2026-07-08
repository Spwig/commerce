---
template_type: hosted_onboarding_tips
category: License
---

# Email Template: hosted_onboarding_tips

## Subject
Tips untuk Memanfaatkan {{ store_name }} dengan Maksimal

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
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Tips Memulai
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Manfaatkan toko Spwig Anda secara maksimal
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Hai {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          Sekarang {{ store_name }} sudah berjalan, berikut beberapa tips untuk membantu Anda memanfaatkan toko Anda secara maksimal.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 1: Theme -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Sesuaikan Tampilan Anda
        </mj-text>
        <mj-text font-size="14px">
          Kunjungi <strong>Design > Theme Settings</strong> untuk memilih tema, mengunggah logo Anda, dan mengatur warna merek Anda. Tampilan toko Anda akan diperbarui secara instan sehingga Anda dapat melihat perubahan secara langsung.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 2: Products -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Tambahkan Produk Anda
        </mj-text>
        <mj-text font-size="14px">
          Pergi ke <strong>Catalog > Products</strong> untuk mulai menambahkan item Anda. Anda dapat membuat variasi produk (ukuran, warna), mengatur harga, mengelola stok, dan mengunggah gambar berkualitas tinggi.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 3: Payments -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Atur Pembayaran
        </mj-text>
        <mj-text font-size="14px">
          Pergi ke <strong>Settings > Payment Providers</strong> untuk menghubungkan Stripe, PayPal, atau metode pembayaran lainnya. Anda dapat mengaktifkan beberapa penyedia sehingga pelanggan dapat membayar dengan cara yang mereka pilih.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 4: Shipping -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Konfigurasikan Pengiriman
        </mj-text>
        <mj-text font-size="14px">
          Di bawah <strong>Settings > Shipping</strong>, atur zona pengiriman dan tarif Anda. Anda dapat membuat aturan pengiriman berbasis flat-rate, berbasis berat, atau pengiriman gratis untuk wilayah berbeda.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 5: SEO -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Tingkatkan SEO Anda
        </mj-text>
        <mj-text font-size="14px">
          Spwig secara otomatis menghasilkan peta situs dan tag meta. Kunjungi <strong>Settings > SEO</strong> untuk menyesuaikan judul halaman, deskripsi, dan gambar berbagi sosial untuk membantu pelanggan menemukan toko Anda.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Go to Admin Panel" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Tips Memulai - {{ store_name }}

Hai {{ name|default:'there' }},

Sekarang {{ store_name }} sudah berjalan, berikut beberapa tips untuk membantu Anda memanfaatkan toko Anda secara maksimal.

1. Sesuaikan Tampilan Anda
Kunjungi Design > Theme Settings untuk memilih tema, mengunggah logo Anda, dan mengatur warna merek Anda.

2. Tambahkan Produk Anda
Pergi ke Catalog > Products untuk mulai menambahkan item Anda dengan variasi, harga, dan gambar.

3. Atur Pembayaran
Pergi ke Settings > Payment Providers untuk menghubungkan Stripe, PayPal, atau metode pembayaran lainnya.

4. Konfigurasikan Pengiriman
Di bawah Settings > Shipping, atur zona pengiriman dan tarif untuk wilayah berbeda.

5. Tingkatkan SEO Anda
Kunjungi Settings > SEO untuk menyesuaikan judul halaman, deskripsi, dan gambar berbagi sosial.

Pergi ke Admin Panel: {{ admin_url }}

Butuh bantuan? Hubungi {{ support_email }}