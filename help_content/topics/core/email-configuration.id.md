---
title: Konfigurasi Email
---

Konfigurasi email mengontrol cara toko Anda mengirimkan email transaksional — konfirmasi pesanan, notifikasi pengiriman, pengaturan ulang kata sandi, dan lainnya. Spwig menyertakan server SMTP bawaan dan mendukung penyedia email eksternal untuk tingkat pengantaran yang lebih tinggi.

![Akun email](/static/core/admin/img/help/email-configuration/email-accounts.webp)

## Penyedia yang Tersedia

| Penyedia | Deskripsi |
|----------|-------------|
| **SMTP Bawaan** | Server email gratis, self-hosted yang disertakan dengan Spwig. Tanda tangan DKIM otomatis. |
| **Gmail API** | Kirim melalui akun Gmail atau Google Workspace Anda menggunakan otentikasi OAuth. |
| **SMTP Umum** | Hubungkan server SMTP apa pun (SendGrid, Mailgun, Amazon SES, atau server email Anda sendiri). |

## Menyiapkan Email

Navigasikan ke **Pengaturan > Akun Email** dan klik **Tambahkan Akun Email** untuk memulai wizard pengaturan.

### Langkah 1: Pilih Penyedia

Pilih penyedia email Anda. Server SMTP bawaan adalah opsi paling sederhana untuk memulai — tidak memerlukan akun eksternal.

### Langkah 2: Konfigurasi Kredensial

Masukkan kredensial untuk penyedia yang dipilih:

- **SMTP Bawaan** — Tidak diperlukan kredensial. Server berjalan pada instalasi Spwig Anda.
- **Gmail API** — Otentikasi melalui Google OAuth. Anda akan dialihkan untuk masuk dengan akun Google Anda.
- **SMTP Umum** — Masukkan alamat server SMTP, port, nama pengguna, dan kata sandi.

### Langkah 3: Konfigurasi Pengirim

Atur identitas pengirim untuk email keluar:

- **Dari Email** — Alamat email yang muncul di bidang 'Dari' (contoh: orders@yourstore.com)
- **Dari Nama** — Nama tampilan di sebelah alamat email (contoh: 'Nama Toko Anda')
- **Balas Ke Email** — Tempat balasan pelanggan dialihkan (dapat berbeda dari alamat Dari)

### Langkah 4: Validasi DNS

Verifikasi catatan otentikasi email domain Anda. Wizard memeriksa tiga catatan DNS:

| Catatan | Tujuan |
|--------|---------|
| **SPF** | Mengizinkan server Anda mengirimkan email atas nama domain Anda |
| **DKIM** | Menandatangani digital email untuk membuktikan bahwa mereka tidak dimanipulasi |
| **DMARC** | Memberi tahu server penerima apa yang harus dilakukan dengan email yang gagal pemeriksaan SPF/DKIM |

Untuk setiap catatan, wizard menampilkan:
- **Status saat ini** — Apakah catatan dikonfigurasi dengan benar
- **Nilai yang diperlukan** — Catatan DNS yang tepat untuk ditambahkan di registrar domain Anda
- **Status penyebaran** — Apakah perubahan terbaru telah berlaku (perubahan DNS dapat memakan waktu hingga 48 jam)

Server SMTP bawaan secara otomatis menghasilkan kunci DKIM untuk domain Anda.

### Langkah 5: Kirim Email Uji

Kirim email uji untuk memverifikasi semuanya berfungsi:
1. Masukkan alamat email penerima
2. Klik **Kirim Uji**
3. Periksa kotak masuk Anda untuk pesan uji
4. Verifikasi email tiba tanpa peringatan spam

### Langkah 6: Simpan dan Aktifkan

Simpan konfigurasi dan atur akun sebagai aktif. Tandai sebagai **Default** jika akun tersebut harus menjadi akun email utama.

## Template Email

Spwig menyertakan lebih dari 30 template email untuk setiap acara transaksional. Navigasikan ke **Pengaturan > Template Email** untuk mengelolanya.

### Jenis Template

Template mencakup semua acara toko termasuk:
- **Siklus Pesanan** — Konfirmasi, pemrosesan, dikirim, diterima, dibatalkan
- **Pembayaran** — Struk, konfirmasi pengembalian dana, pembayaran gagal
- **Akun Pelanggan** — Selamat datang, pengaturan ulang kata sandi, verifikasi email
- **Kartu Hadiah** — Pengiriman, pemberitahuan saldo
- **Pengiriman** — Pembaruan pelacakan, konfirmasi pengiriman
- **Produk Digital** — Tautan unduh, kunci lisensi
- **Pemasaran** — Pemulihan keranjang yang ditinggalkan, permintaan ulasan

### Menyesuaikan Template

1. Navigasikan ke daftar template
2. Klik template untuk mengedit
3. Ubah baris subjek, header, konten tubuh, dan footer
4. Gunakan variabel template (misalnya, `{{ order.number }}`, `{{ customer.name }}`) untuk konten dinamis
5. Pratinjau email sebelum menyimpan

### Dukungan Multi-Bahasa

Template email mendukung beberapa bahasa:
- Setiap template dapat memiliki terjemahan untuk semua bahasa aktif toko Anda
- Sistem mengirimkan email dalam bahasa yang disukai pelanggan
- **Rantai fallback bahasa** — Jika terjemahan tidak tersedia, sistem kembali ke bahasa default toko
- Gunakan fitur **Terjemahan AI** untuk menerjemahkan otomatis template ke bahasa lain

### Menyalin Template

Untuk membuat versi disesuaikan dari template sistem:
1. Buka template yang ingin Anda ubah
2. Klik **Salin Template**
3. Edit versi yang disalin
4. Salinan mengambil prioritas atas template sistem asli

## Antrian Email

Lacak email keluar di **Pengaturan > Antrian Email**:

- **Diantrikan** — Email yang menunggu untuk dikirim
- **Mengirim** — Saat ini sedang ditransmisikan
- **Dikirim** — Berhasil dikirimkan
- **Gagal** — Tidak dapat dikirimkan (dengan detail kesalahan)
- **Dibalas** — Ditolak oleh server email penerima

Klik email apa pun untuk melihat detail lengkap termasuk penerima, subjek, waktu pengiriman, dan status pengiriman.

## Pelacakan Pengiriman

Lacak keterlibatan email:
- **Pembukaan** — Berapa banyak penerima yang membuka email
- **Klik** — Klik tautan dalam email
- **Dibalas** — Pelacakan balasan keras dan lunak
- **Keluhan** — Laporan spam dari penerima

## Akun Multi

Anda dapat mengonfigurasi beberapa akun email:
- **Akun Default** — Digunakan untuk semua email keluar kecuali diganti
- **Fallback** — Jika akun default gagal, email akan diantrikan untuk dicoba kembali
- Gunakan akun berbeda untuk tujuan berbeda (misalnya, satu untuk email transaksional, yang lain untuk pemasaran)

## Tips

- Mulailah dengan **Server SMTP Bawaan** untuk pengaturan cepat, lalu beralih ke penyedia eksternal jika Anda membutuhkan volume pengiriman yang lebih tinggi atau pengantaran yang lebih baik.
- Selalu konfigurasikan **SPF, DKIM, dan DMARC** — tanpa mereka, email jauh lebih mungkin berakhir di folder spam.
- Kirim **email uji** setelah setiap perubahan konfigurasi untuk memverifikasi pengiriman berfungsi.
- Pantau antrian email secara teratur untuk **gagal** atau **dibalas** email — ini menunjukkan masalah pengantaran.
- Gunakan **alamat pengirim profesional** (misalnya, orders@yourstore.com) daripada alamat email gratis untuk kepercayaan dan pengantaran yang lebih baik.
- Pertahankan template Anda ringkas — email transaksional harus menyampaikan informasi secara cepat, bukan sebagai surat kabar pemasaran.