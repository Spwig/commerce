---
title: Pengaturan Pembayaran
---

Penggunaan penyedia pembayaran menghubungkan toko Anda ke gateway pembayaran sehingga Anda dapat menerima kartu kredit, dompet digital, dan metode pembayaran lainnya saat checkout. Spwig mendukung beberapa penyedia secara bersamaan, memberi pelanggan Anda opsi pembayaran yang fleksibel.

![Penggunaan penyedia pembayaran](/static/core/admin/img/help/payment-setup/payment-dashboard.webp)

## Penyedia yang Tersedia

| Penyedia | Deskripsi |
|----------|-------------|
| **Stripe** | Kartu kredit, Apple Pay, Google Pay, dan 135+ mata uang |
| **PayPal** | Saldo PayPal, kartu kredit/debit, dan opsi Bayar Nanti |
| **Airwallex** | Pembayaran multi-mata uang yang dioptimalkan untuk perdagangan lintas batas |
| **Adyen** | Pembayaran kelas perusahaan dengan 250+ metode pembayaran di seluruh dunia |
| **Square** | Pembayaran tatap muka dan online dengan dukungan POS terintegrasi |
| **Revolut** | Pembayaran Eropa yang cepat dengan kurs FX kompetitif |

## Menghubungkan Penyedia

Navigasikan ke **Pengaturan > Penyedia Pembayaran** dan klik **Koneksi Penyedia** untuk memulai wizard pengaturan.

### Langkah 1: Pilih Penyedia

Pilih dari penyedia pembayaran yang tersedia. Setiap kartu menampilkan fitur dan wilayah yang didukung oleh penyedia.

### Langkah 2: Petunjuk Pengaturan

Lihat panduan pengaturan khusus penyedia. Ini termasuk:
- Cara membuat akun dengan penyedia (jika Anda belum memiliki akun)
- Di mana menemukan kredensial API Anda di dashboard penyedia
- Persyaratan apa pun (misalnya, verifikasi bisnis)

### Langkah 3: Masukkan Kredensial

Masukkan kredensial API Anda:
- **API Key / Secret Key** — Kredensial otentikasi Anda dari dashboard penyedia
- **Mode Checkout** — Pilih cara pelanggan berinteraksi dengan formulir pembayaran:

| Mode | Deskripsi |
|------|-------------|
| **Hosted** | Pelanggan dialihkan ke halaman pembayaran penyedia (misalnya, Stripe Checkout). Pengaturan paling sederhana, kepatuhan PCI ditangani oleh penyedia. |
| **Integrated** | Formulir pembayaran disematkan langsung di halaman checkout Anda. Pengalaman yang mulus, tetapi memerlukan SDK JavaScript penyedia. |

- **Sandbox / Mode Live** — Mulai dalam mode sandbox untuk pengujian, lalu beralih ke mode live saat siap

### Langkah 4: Uji Koneksi

Klik **Uji Koneksi** untuk memverifikasi kredensial Anda valid. Wizard memeriksa:
- Otentikasi kunci API
- Izin akun
- Ketersediaan akhir titik webhook

### Langkah 5: Konfigurasi dan Simpan

Selesaikan pengaturan penyedia:
- **Aktif** — Aktifkan atau nonaktifkan penyedia
- **Penyedia Default** — Tetapkan sebagai metode pembayaran utama saat checkout
- **Nama Tampilan** — Nama yang ditampilkan kepada pelanggan saat checkout
- **Urutan Penyortiran** — Mengontrol urutan penyedia muncul saat checkout (angka yang lebih rendah muncul lebih dulu)

## Dashboard Pembayaran

Navigasikan ke **Pengaturan > Dashboard Pembayaran** untuk melihat ringkasan aktivitas pembayaran Anda:

### Tindakan yang Diperlukan

Kartu peringatan di bagian atas menyoroti masalah yang memerlukan perhatian:
- **Transaksi Gagal** — Pembayaran yang tidak dapat diproses
- **Pengambilan Tertunda** — Pembayaran yang telah disetujui menunggu pengambilan
- **Kesalahan Koneksi** — Penyedia dengan masalah koneksi

### Analitik Pendapatan

- **Grafik Pendapatan** — Pemecahan visual volume pembayaran seiring waktu, dikelompokkan berdasarkan hari, minggu, atau bulan
- **Metrik Kinerja** — Total pendapatan, tingkat keberhasilan, nilai transaksi rata-rata, dan tingkat pengembalian
- **Perbandingan Penyedia** — Kartu kinerja sampingan untuk setiap penyedia yang terhubung

### Pemecahan Transaksi

- **Distribusi Status** — Jumlah transaksi yang selesai, tertunda, gagal, dan dikembalikan
- **Campuran Metode Pembayaran** — Metode pembayaran yang paling sering digunakan oleh pelanggan (kartu kredit, PayPal, dompet digital)

## Mengelola Metode Pembayaran

Setiap penyedia mendukung metode pembayaran yang berbeda. Anda dapat mengaktifkan atau menonaktifkan metode tertentu per negara:

1. Navigasikan ke halaman konfigurasi penyedia
2. Gulir ke bagian **Metode Pembayaran**
3. Nyalakan atau matikan metode individu
4. Gunakan kontrol tingkat negara untuk membatasi metode ke pasar tertentu

Ini berguna ketika metode pembayaran populer di satu wilayah tetapi tidak di wilayah lain (misalnya, iDEAL di Belanda, Bancontact di Belgia).

## Webhook

Webhook menjaga toko Anda tetap sinkron dengan penyedia pembayaran secara real time. Mereka menangani peristiwa seperti:
- Pembayaran selesai atau gagal
- Pengembalian dana diproses
- Dispute dan pembatalan tagihan dibuka
- Perpanjangan langganan

### Pengaturan Otomatis

Ketika Anda menghubungkan penyedia, Spwig secara otomatis mendaftarkan titik akhir webhook dengan penyedia. URL webhook ditampilkan di halaman konfigurasi penyedia untuk referensi.

### Pemantauan Webhook

Setiap webhook yang masuk dicatat dengan:
- **Jenis Acara** (misalnya, payment_intent.succeeded)
- **Tanda Waktu** dan status pemrosesan
- **Payload** untuk debugging

Jika webhook gagal diproses, akan dicatat sebagai kesalahan sehingga Anda dapat menyelidiki.

## Menggunakan Banyak Penyedia

Anda dapat menghubungkan beberapa penyedia pembayaran secara bersamaan:

- **Penyedia Default** — Penyedia yang dipilih secara default saat checkout. Tandai satu penyedia sebagai default dalam konfigurasinya.
- **Urutan Penyortiran** — Mengontrol urutan tampilan saat checkout. Pelanggan melihat semua penyedia aktif dan dapat memilih yang mereka sukai.
- **Failover** — Jika penyedia mengalami gangguan, pelanggan masih dapat membayar menggunakan penyedia alternatif.

## Tips

- Mulai dengan **Stripe** atau **PayPal** — mereka menutupi rentang metode pembayaran dan wilayah yang paling luas.
- Gunakan **mode sandbox/pengujian** untuk memproses transaksi pengujian sebelum diluncurkan. Setiap penyedia memiliki nomor kartu pengujian di dokumentasinya.
- Aktifkan **banyak penyedia** sehingga pelanggan memiliki opsi pembayaran cadangan jika satu penyedia mengalami masalah.
- Tetapkan **urutan penyortiran yang rendah** untuk penyedia favorit Anda sehingga muncul pertama saat checkout.
- Pantau Dashboard Pembayaran secara mingguan untuk menangkap transaksi gagal dan masalah koneksi secara dini.
- Jaga kredensial API Anda aman — mereka disimpan dalam bentuk terenkripsi di database tetapi seharusnya tidak pernah dibagikan.