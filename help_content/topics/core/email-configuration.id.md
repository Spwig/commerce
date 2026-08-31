---
title: Konfigurasi Email
---

Konfigurasi email mengontrol cara toko Anda mengirim email transaksional — konfirmasi pesanan, notifikasi pengiriman, reset kata sandi, dan lainnya. Spwig menyertakan server SMTP bawaan dan mendukung penyedia email eksternal untuk tingkat pengiriman yang lebih tinggi.

![Akun email](/static/core/admin/img/help/email-configuration/email-accounts.webp)

## Penyedia Tersedia

| Penyedia | Deskripsi |
|----------|-------------|
| **SMTP Bawaan** | Server email self-hosted gratis yang disertakan dengan Spwig. Penandatanganan DKIM otomatis. |
| **Gmail API** | Kirim melalui akun Gmail atau Google Workspace Anda menggunakan autentikasi OAuth. |
| **SMTP Umum** | Hubungkan server SMTP apa pun (SendGrid, Mailgun, Amazon SES, atau server email Anda sendiri). |

## Mengatur Email

Buka **Settings > Email Accounts** dan klik **Add Email Account** untuk memulai wizard pengaturan.

### Langkah 1: Pilih Penyedia

Pilih penyedia email Anda. Server SMTP bawaan adalah opsi paling sederhana untuk memulai — tidak memerlukan akun eksternal.

### Langkah 2: Konfigurasi Kredensial

Masukkan kredensial untuk penyedia yang Anda pilih:

- **SMTP Bawaan** — Tidak memerlukan kredensial. Server berjalan pada instalasi Spwig Anda.
- **Gmail API** — Autentikasi melalui Google OAuth. Anda akan diarahkan untuk masuk dengan akun Google Anda.
- **SMTP Umum** — Masukkan alamat server SMTP, port, nama pengguna, dan kata sandi.

### Langkah 3: Konfigurasi Pengirim

Atur identitas pengirim untuk email keluar:

- **From Email** — Alamat email yang muncul di field "From" (misalnya, orders@yourstore.com)
- **From Name** — Nama tampilan di samping alamat email (misalnya, "Nama Toko Anda")
- **Reply-To Email** — Ke mana balasan pelanggan diarahkan (dapat berbeda dari alamat From)

### Langkah 4: Validasi DNS

Verifikasi catatan autentikasi email domain Anda. Wizard memeriksa tiga catatan DNS:

| Catatan | Tujuan |
|--------|---------|
| **SPF** | Mengotorisasi server Anda untuk mengirim email atas nama domain Anda |
| **DKIM** | Menandatangani email secara digital untuk membuktikan bahwa email tidak telah diubah |
| **DMARC** | Memberitahu server penerima apa yang harus dilakukan dengan email yang gagal pemeriksaan SPF/DKIM |

Untuk setiap catatan, wizard menampilkan:
- **Status saat ini** — Apakah catatan dikonfigurasi dengan benar
- **Nilai yang diperlukan** — Catatan DNS persis yang harus ditambahkan di registrar domain Anda
- **Status propagasi** — Apakah perubahan baru-baru ini telah berlaku (perubahan DNS dapat memakan waktu hingga 48 jam)

Server SMTP bawaan secara otomatis menghasilkan kunci DKIM untuk domain Anda.

### Langkah 5: Kirim Email Uji

Kirim email uji untuk memverifikasi semuanya berfungsi:
1. Masukkan alamat email penerima
2. Klik **Send Test** (Kirim Uji)
3. Periksa kotak masuk Anda untuk pesan uji
4. Verifikasi email tiba tanpa peringatan spam

### Langkah 6: Simpan dan Aktifkan

Simpan konfigurasi dan setel akun sebagai aktif. Tandai sebagai **Default** (Bawaan) jika ini harus menjadi akun email utama.

## Template Email

Spwig menyertakan 30+ template email untuk setiap peristiwa transaksional. Buka **Settings > Email Templates** untuk mengelolanya.

### Jenis Template

Template mencakup semua peristiwa toko termasuk:
- **Siklus Hidup Pesanan** — Konfirmasi, pemrosesan, dikirim, diterima, dibatalkan
- **Pembayaran** — Kuitansi, konfirmasi pengembalian dana, pembayaran gagal
- **Akun Pelanggan** — Selamat datang, reset kata sandi, verifikasi email
- **Kartu Hadiah** — Pengiriman, notifikasi saldo
- **Pengiriman** — Pembaruan pelacakan, konfirmasi pengiriman
- **Produk Digital** — Tautan unduhan, kunci lisensi
- **Pemasaran** — Pemulihan keranjang ditinggalkan, permintaan ulasan

### Menyesuaikan Template

1. Buka daftar template
2. Klik template untuk diedit
3. Ubah baris subjek, header, konten tubuh, dan footer
4. Gunakan variabel template (misalnya, `{{ order.number }}`, `{{ customer.name }}`) untuk konten dinamis
5. Pratinjau email sebelum menyimpan

### Dukungan Multi-Bahasa

Template email mendukung beberapa bahasa:
- Setiap template dapat memiliki terjemahan untuk semua bahasa aktif di toko Anda
- Sistem mengirim email dalam bahasa yang diinginkan pelanggan
- **Rantai fallback bahasa** — Jika terjemahan tidak tersedia, sistem kembali ke bahasa default toko
- Gunakan fitur **Terjemahan AI** untuk menerjemahkan template ke bahasa lain secara otomatis

### Mengkloning Template

Untuk membuat versi kustom dari template sistem:
1. Buka template yang ingin Anda modifikasi
2. Klik **Klon Template**
3. Edit versi yang diklon
4. Klon memiliki prioritas lebih tinggi daripada template sistem asli

## Antrean Email

Pantau email yang keluar di **Pengaturan > Antrean Email**:

- **Dalam Antrean** — Email yang menunggu untuk dikirim
- **Mengirim** — Sedang dalam proses transmisi
- **Terkirim** — Berhasil dikirim
- **Gagal** — Tidak dapat dikirim (dengan detail kesalahan)
- **Bounce** — Ditolak oleh server email penerima

Klik email mana pun untuk melihat detail lengkapnya, termasuk penerima, subjek, waktu pengiriman, dan status pengiriman.

## Pelacakan Pengiriman

Pantau keterlibatan email:
- **Pembukaan** — Berapa banyak penerima yang membuka email
- **Klik** — Klik tautan di dalam email
- **Bounce** — Pelacakan bounce keras dan lunak
- **Keluhan** — Laporan spam dari penerima

## Beberapa Akun

Anda dapat mengonfigurasi beberapa akun email:
- **Akun Default** — Digunakan untuk semua email keluar kecuali jika ditimpa
- **Fallback** — Jika akun default gagal, email masuk ke antrean untuk dicoba lagi
- Gunakan akun yang berbeda untuk tujuan yang berbeda (misalnya, satu untuk email transaksional, yang lain untuk pemasaran)

## Mode Pengiriman Email

Buka **Pengaturan > Pengaturan Toko** untuk mengontrol bagaimana toko Anda menangani email keluar. Pengaturan ini berguna selama pengembangan dan pengujian.

| Mode | Deskripsi |
|------|-------------|
| **Live** | Email dikirim secara normal ke penerima asli |
| **Dijeda** | Email ditahan dalam antrean dan tidak dikirim sampai Anda beralih kembali ke Live |
| **Hanya Log** | Email dicatat di kotak keluar tetapi tidak pernah dikirim |

### Email Pengalihan Uji

Atur alamat **Email Pengalihan Uji** untuk memotong semua email keluar dan mengalihkannya ke satu alamat. Ketika diatur, setiap email — terlepas dari penerima aslinya — akan dikirim ke alamat tersebut. Ini berguna untuk menguji template email tanpa tidak sengaja mengirim ke pelanggan asli. Kosongkan untuk mengirim email ke penerima sebenarnya.

### Daftar Putih Email Sandbox

Dalam mode sandbox atau pengembangan, Anda dapat membatasi pengiriman email ke daftar putih alamat yang disetujui. Hanya email ke alamat dalam daftar putih yang akan dikirim. Semua email lainnya dicatat tetapi tidak pernah dikirim. Email admin selalu dimasukkan secara otomatis. Anda dapat menambahkan hingga 10 alamat.

## Tips

- Mulai dengan server **SMTP Bawaan** untuk pengaturan cepat, lalu beralih ke penyedia eksternal jika Anda membutuhkan volume pengiriman yang lebih tinggi atau keterjangkauan yang lebih baik.
- Selalu konfigurasikan rekaman **SPF, DKIM, dan DMARC** — tanpa mereka, email jauh lebih mungkin masuk ke folder spam.
- Kirim **email uji** setelah setiap perubahan konfigurasi untuk memverifikasi bahwa pengiriman berfungsi.
- Pantau antrean email secara teratur untuk email **gagal** atau **bounce** — ini menunjukkan masalah keterjangkauan.
- Gunakan **alamat pengirim profesional** (misalnya, orders@yourstore.com) alih-alih alamat email gratis untuk kepercayaan dan keterjangkauan yang lebih baik.
- Jaga template Anda tetap ringkas — email transaksional harus menyampaikan informasi dengan cepat, bukan menjadi buletin pemasaran.
