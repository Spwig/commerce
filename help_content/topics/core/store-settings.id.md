---
title: Mengonfigurasi Pengaturan Toko
---

Pengaturan Toko adalah tempat pusat untuk mengonfigurasi identitas, lokalisasi, branding, dan preferensi operasional toko Anda. Navigasikan ke **Pengaturan > Pengaturan Toko** untuk memulai.

![Tab pengaturan umum toko](/static/core/admin/img/help/store-settings/store-settings-general.webp)

## Tab Umum

Tab **Umum** berisi pengaturan identitas inti toko Anda.

### Identitas Toko

- **Nama Toko** — Nama tampilan yang ditampilkan dalam judul halaman, email, dan header admin.
- **Tagline** — Deskripsi pendek toko Anda, digunakan dalam SEO dan berbagi media sosial.
- **URL Situs** — Alamat web publik toko Anda. Ini digunakan dalam email, pembuatan peta situs, dan pembangunan tautan.

### Informasi Kontak

- **Email Kontak** — Menerima notifikasi pesanan dan ditampilkan dalam komunikasi pelanggan.
- **Nomor Telepon** — Nomor telepon dukungan opsional yang ditampilkan di footer dan email.

### Alamat Bisnis

Masukkan alamat lengkap Anda (jalan, kota, negara bagian, kode pos, negara). Ini digunakan untuk:
- Perhitungan asal pengiriman
- Perhitungan pajak
- Persyaratan hukum dan faktur

## Branding

### Logo

Unggah logo toko Anda (disarankan PNG atau SVG, ~200x50px dengan latar belakang transparan). Logo muncul di:
- Header toko
- Template email
- Panel admin

### Favicon

Unggah favicon persegi (ICO atau PNG, 32x32px). Ini muncul sebagai:
- Ikon tab browser
- Ikon bookmark
- Ikon layar beranda mobile

## Lokalisasi

### Bahasa Default

Pilih bahasa utama toko Anda dari 10 opsi yang didukung:

| Bahasa | Kode |
|----------|------|
| English | en |
| Spanish | es |
| French | fr |
| German | de |
| Portuguese | pt |
| Japanese | ja |
| Chinese Simplified | zh-hans |
| Chinese Traditional | zh-hant |
| Russian | ru |
| Arabic | ar |

Bahasa default mengontrol bahasa antarmuka admin dan fallback untuk konten toko.

### Timezone

Pilih zona waktu toko Anda untuk timestamp pesanan yang akurat, promosi yang dijadwalkan, dan pelaporan.

### Mata Uang

- **Mata Uang Default** — Mata uang utama untuk penentuan harga dan akuntansi.
- **Multi-Mata Uang** — Aktifkan untuk memungkinkan pelanggan melihat harga dalam mata uang yang mereka pilih dengan konversi otomatis menggunakan kurs tukar real-time.

Konfigurasikan mata uang tambahan di **Pengaturan > Pengaturan Toko > Mata Uang**.

## Pengaturan E-Commerce

### Checkout Pengunjung

Izinkan pembelian tanpa membuat akun:
- Alur checkout yang lebih cepat
- Mengurangi hambatan bagi pembeli baru
- Menangkap lebih sedikit data pelanggan

### Format Nomor Pesanan

Kustomisasi cara nomor pesanan muncul:
- **Awalan** — contoh, "ORD-"
- **Nomor Awal** — Nomor pesanan pertama
- **Padding** — contoh, 00001

### Default Persediaan

- **Lacak Persediaan** — Aktifkan pelacakan stok secara global
- **Ambang Batas Persediaan Rendah** — Tingkat peringatan (default: 5 unit)
- **Izinkan Pemesanan Kembali** — Terima pesanan ketika stok habis

## Pengaturan Email

### Informasi Pengirim

- **Nama Dari** — Tampil sebagai pengirim email (biasanya nama toko Anda)
- **Email Dari** — Harus berasal dari domain yang diverifikasi
- **Email Balasan Ke** — Tempat balasan pelanggan dialihkan

### Penyedia Email

Konfigurasikan layanan pengiriman email Anda di **Pengaturan > Konfigurasi Email**. Penyedia yang didukung termasuk SMTP, SendGrid, Mailgun, dan Amazon SES.

## Hukum & Kepatuhan

Tambahkan kebijakan toko Anda untuk memenuhi persyaratan hukum:

- **Syarat & Ketentuan** — Diperlukan untuk checkout; pelanggan harus menerima sebelum membeli
- **Kebijakan Privasi** — Kepatuhan GDPR/CCPA; tautan di footer
- **Kebijakan Pengembalian** — Definisikan jendela pengembalian, kondisi, dan proses pengembalian dana

## Mode Pemeliharaan

Aktifkan mode pemeliharaan untuk sementara menonaktifkan toko Anda:
- Menampilkan pesan pemeliharaan khusus kepada pengunjung
- Membatasi akses hanya untuk pengguna admin
- Berguna selama pembaruan besar atau migrasi

## Pengaturan Pajak

Konfigurasikan pengumpulan pajak di **Pengaturan > Pengaturan Pajak**:

1. **Metode Perhitungan** — Berdasarkan alamat pengiriman, alamat pembayaran, atau lokasi toko
2. **Tarif Pajak** — Definisikan tarif berdasarkan wilayah dan kelas pajak produk
3. **Tampilan Pajak** — Tampilkan harga dengan pajak, tanpa pajak, atau keduanya

## Tips

- Atur zona waktu Anda dengan benar sebelum memproses pesanan apa pun — ini memengaruhi semua timestamp dan laporan.
- Aktifkan checkout pengunjung untuk meningkatkan tingkat konversi.
- Isi alamat bisnis Anda untuk perhitungan pengiriman dan pajak yang akurat.
- Unggah logo dan favicon untuk pengalaman berbranding yang profesional.
- Periksa ulang halaman hukum Anda secara teratur untuk tetap mematuhi regulasi setempat.

## Penyelesaian Masalah

**Perubahan tidak muncul di toko online:**
- Bersihkan cache browser Anda
- Jalankan pembersihan cache dari panel admin
- Periksa apakah mode pemeliharaan secara tidak sengaja diaktifkan

**Email tidak terkirim:**
- Verifikasi pengaturan penyedia email Anda di Konfigurasi Email
- Periksa bahwa domain "Email Dari" telah diverifikasi
- Uji koneksi dari halaman pengaturan penyedia

**Konversi mata uang tidak berfungsi:**
- Verifikasi penyedia kurs tukar Anda terhubung
- Periksa kredensial API di pengaturan kurs tukar
- Coba perbarui kurs secara manual

