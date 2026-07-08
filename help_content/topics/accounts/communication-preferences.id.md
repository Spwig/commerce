---
title: Preferensi Komunikasi
---

Preferensi komunikasi memungkinkan pelanggan mengontrol email dan pesan SMS yang mereka terima dari toko Anda. Sistem ini memastikan kepatuhan terhadap GDPR dan membantu Anda menghormati preferensi komunikasi pelanggan di semua saluran.

Navigasikan ke **Pelanggan > Preferensi Komunikasi** di bilah sisi admin untuk mengelola preferensi komunikasi pelanggan.

## Memahami Preferensi Komunikasi

Sistem preferensi komunikasi memberi pelanggan kendali granular terhadap pesan yang mereka terima. Ini mencakup:

- **Email Transaksional** — Konfirmasi pesanan penting, pembaruan pengiriman, email keamanan akun (selalu aktif)
- **Email Pemasaran** — Surat berita, promosi, rekomendasi produk (memerlukan pendaftaran)
- **Pemberitahuan Aplikasi Khusus** — Posting blog, poin loyalitas, hadiah referensi, komisi afiliasi
- **Pemberitahuan SMS** — Pemberitahuan melalui pesan teks (memerlukan pendaftaran eksplisit sesuai TCPA)

Semua komunikasi pemasaran memerlukan persetujuan pelanggan dan verifikasi email untuk memastikan kepatuhan terhadap GDPR.

## Penjelasan Jenis Preferensi

### Komunikasi Transaksional (Selalu Aktif)

Pesan transaksional penting untuk akun dan pesanan pelanggan. Pesan-pesan ini **tidak dapat dinonaktifkan** oleh pelanggan:

| Jenis | Deskripsi | Contoh |
|------|-------------|----------|
| **Konfirmasi Pesanan** | Konfirmasi ketika pesanan ditempatkan | Pesanan #12345 telah diterima |
| **Pembaruan Pengiriman** | Pemberitahuan ketika status pesanan berubah | Pesanan Anda telah dikirim |
| **Konfirmasi Pembayaran** | Pembayaran diterima, pengembalian dana diproses | Pembayaran $49.99 telah dikonfirmasi |
| **Keamanan Akun** | Reset kata sandi, verifikasi email | Reset kata sandi Anda |

### Komunikasi Pemasaran (Pendaftaran Diperlukan)

Pesan pemasaran memerlukan persetujuan pelanggan dan verifikasi email:

| Jenis | Deskripsi | Default |
|------|-------------|---------|
| **Surat Berita** | Surat berita umum dan pembaruan | Non-aktif |
| **Tawaran Pemasaran** | Penjualan, diskon, tawaran khusus | Non-aktif |
| **Rekomendasi Produk** | Rekomendasi produk pribadi | Non-aktif |
| **Kembali ke Stok** | Pemberitahuan ketika produk kembali ke stok | Non-aktif |

Pelanggan harus **memverifikasi alamat email mereka** sebelum menerima email pemasaran apa pun (persyaratan GDPR double opt-in).

### Preferensi Aplikasi Khusus

Pelanggan dapat mengontrol pemberitahuan dari fitur khusus:

**Pemberitahuan Blog**
- Posting blog baru diterbitkan (segera, digest mingguan, atau digest bulanan)
- Langganan kategori khusus
- Preferensi frekuensi

**Program Loyalitas**
- Pemberitahuan poin yang diperoleh
- Peningkatan tingkat
- Hadiah yang dibuka
- Poin yang segera kedaluwarsa
- Bonus ulang tahun
- Tawaran kampanye

**Program Referensi**
- Hadiah diberikan (pemilik referensi dan penerima referensi)
- Pendaftaran sukses referensi
- Hadiah yang segera kedaluwarsa
- Undangan referensi

**Program Afiliasi**
- Komisi yang diperoleh
- Komisi disetujui atau ditolak
- Pembayaran diproses, selesai, atau gagal
- Laporan kinerja bulanan

### Pemberitahuan SMS (Pendaftaran Eksplisit Diperlukan)

Semua pemberitahuan SMS memerlukan **pendaftaran eksplisit** sesuai regulasi TCPA. Pelanggan harus secara aktif menandai kotak pendaftaran SMS:

- **SMS Transaksional** — Pesanan dikirim, terkirim (pendaftaran diperlukan)
- **SMS Pemasaran** — Promosi, tawaran khusus (pendaftaran terpisah diperlukan)

Bahkan SMS transaksional memerlukan pendaftaran karena mengirimkan pesan teks yang tidak diminta diatur lebih ketat daripada email.

## Mengelola Preferensi Pelanggan di Admin

### Melihat Semua Preferensi

Navigasikan ke **Pelanggan > Preferensi Komunikasi** untuk melihat semua preferensi pelanggan:

| Kolom | Deskripsi |
|--------|-------------|
| **Email Pengguna** | Alamat email pelanggan (tautan ke admin pengguna) |
| **Status Email** | Tanda centang hijau ✓ jika email aktif, lingkaran abu-abu ○ jika dinonaktifkan |
| **Status SMS** | Tanda centang hijau ✓ jika SMS aktif, lingkaran abu-abu ○ jika dinonaktifkan |
| **Status Pemasaran** | Badge "Opted In" atau "Opted Out" |
| **Status Verifikasi** | 📧✓ jika email diverifikasi, 📱✓ jika SMS diverifikasi |
| **Sumber Persetujuan** | Di mana pelanggan memberikan persetujuan (pendaftaran, checkout, pusat preferensi) |
| **Diperbarui Pada** | Waktu terakhir preferensi diubah |

### Memfilter Preferensi

Gunakan bilah sisi filter untuk menemukan pelanggan:

- **Email Aktif** — Ya/Tidak
- **SMS Aktif** — Ya/Tidak
- **Email Pemasaran** — Ya/Tidak (telah mendaftar untuk pemasaran)
- **SMS Pemasaran** — Ya/Tidak (telah mendaftar untuk SMS pemasaran)
- **Email Diverifikasi** — Ya/Tidak (telah memverifikasi alamat email)
- **SMS Diverifikasi** — Ya/Tidak (telah memverifikasi nomor telepon)
- **Sumber Persetujuan** — Pendaftaran, Checkout, Pusat Preferensi, API, Migrasi
- **Kode Bahasa** — Bahasa yang dipilih untuk komunikasi

### Mencari Preferensi

Cari pelanggan berdasarkan:
- Email pengguna
- Nama pengguna
- Nama depan
- Nama belakang
- Token batal langganan

### Tindakan Massal

Pilih beberapa pelanggan dan terapkan tindakan massal:

**✓ Tandai Email sebagai Diverifikasi**
- Verifikasi alamat email pelanggan secara manual
- Berguna ketika mengimpor pelanggan dari sistem lain
- Membatalkan cache preferensi untuk menerapkan perubahan segera

**🚫 Batal Langganan dari Semua Pemasaran**
- Menonaktifkan semua komunikasi pemasaran (email, SMS, semua aplikasi)
- Menyimpan komunikasi transaksional tetap aktif
- Gunakan ini untuk pelanggan yang meminta untuk sepenuhnya batal langganan
- Mematuhi hak GDPR untuk menarik persetujuan

**📥 Ekspor Preferensi ke CSV**
- Ekspor preferensi pelanggan ke spreadsheet
- Termasuk semua bidang preferensi dan pengaturan aplikasi khusus
- Berguna untuk audit kepatuhan dan analisis
- Format: CSV dengan header

## Pusat Preferensi Self-Service Pelanggan

Pelanggan dapat mengelola preferensi mereka sendiri di `/accounts/preferences/` saat mereka masuk.

### Fitur Pusat Preferensi

**Tindakan Cepat**
- **Langganan ke Semua Pemasaran** — Aktifkan semua komunikasi pemasaran dengan satu klik
- **Batal Langganan dari Semua** — Nonaktifkan semua komunikasi pemasaran (komunikasi transaksional tetap aktif)

**Kartu Preferensi**
- **Email Transaksional** — Hanya baca (selalu aktif, ditandai sebagai "Diperlukan")
- **Komunikasi Pemasaran** — Nyalakan/matikan dengan badge verifikasi
- **Preferensi Blog** — Nyalakan/matikan, pilih frekuensi (segera, mingguan, bulanan)
- **Program Loyalitas** — Nyalakan/matikan jenis pemberitahuan individu
- **Program Referensi** — Nyalakan/matikan pemberitahuan hadiah
- **Program Afiliasi** — Nyalakan/matikan pemberitahuan komisi dan pembayaran
- **Pemberitahuan SMS** — Pilih untuk mendaftar atau batal langganan SMS (menampilkan status verifikasi)

**Pembaruan Waktu Nyata**
- Perubahan disimpan secara langsung melalui AJAX
- Tidak diperlukan reload halaman
- Umpan balik visual saat disimpan

### Proses Verifikasi Email

Ketika pelanggan mengaktifkan email pemasaran:

1. Pelanggan menyalakan "Email Pemasaran" ke ON
2. Sistem mengirim email verifikasi dengan tautan unik
3. Pelanggan mengklik tautan verifikasi
4. Email ditandai sebagai diverifikasi (badges 📧✓ muncul)
5. Email pemasaran akan dikirim sekarang

**Pelanggan yang belum diverifikasi TIDAK akan menerima email pemasaran** bahkan jika toggle ON. Ini memastikan kepatuhan double opt-in GDPR.

## Batal Langganan Satu Klik

Semua email pemasaran menyertakan tautan batal langganan di bagian bawah. Mengklik tautan ini:

1. Membawa pelanggan ke `/accounts/unsubscribe/<token>/` (tidak memerlukan login)
2. Menampilkan apa yang mereka batal langganan
3. Memungkinkan umpan balik opsional (alasan batal langganan)
4. Menonaktifkan komunikasi pemasaran
5. Menyimpan komunikasi transaksional tetap aktif
6. Menyediakan tautan ke pusat preferensi penuh

Pelanggan dapat mendaftar kembali kapan saja melalui pusat preferensi.

## Kepatuhan & Persyaratan Hukum

### Kepatuhan Artikel 7 GDPR

Sistem memastikan kepatuhan penuh terhadap Artikel 7 GDPR:

**✅ Bukti Persetujuan**
- Timestamp saat persetujuan diberikan
- Sumber persetujuan (pendaftaran, checkout, pusat preferensi)
- Alamat IP persetujuan
- User agent (informasi browser)

**✅ Persetujuan Terpisah**
- Email pemasaran dan transaksional adalah toggle terpisah
- Setiap aplikasi (blog, loyalitas, dll.) memerlukan persetujuan individu

**✅ Penarikan Persetujuan yang Mudah**
- Batal langganan satu klik di semua email pemasaran
- Pusat preferensi tersedia untuk semua pelanggan yang masuk
- Batal langganan berlaku segera

**✅ Persetujuan yang Diberikan Secara Bebas**
- Default adalah non-aktif untuk pemasaran (praktik terbaik GDPR)
- Tidak ada kotak centang yang sudah dicentang (pelanggan harus secara aktif mendaftar)

**✅ Persetujuan yang Spesifik dan Diberikan dengan Informasi**
- Deskripsi jelas tentang apa yang dikontrol setiap preferensi
- Preferensi tingkat aplikasi yang granular (tidak semua atau tidak sama sekali)

**✅ Persetujuan yang Dapat Diverifikasi**
- Double opt-in untuk email pemasaran
- Jejak audit melalui pelacakan status EmailOutbox

### Kepatuhan TCPA (Regulasi SMS USA)

Semua pemberitahuan SMS memerlukan **pendaftaran eksplisit**:

- Pelanggan harus secara aktif menandai kotak pendaftaran SMS
- Tidak ada kotak centang yang sudah dicentang
- Deskripsi jelas tentang apa yang mereka pendaftarkan
- Batal langganan yang mudah melalui pusat preferensi
- Semua pengiriman SMS dicatat untuk audit kepatuhan

### Kepatuhan CAN-SPAM (Regulasi Email USA)

Sistem memastikan kepatuhan CAN-SPAM:

- Tautan batal langganan di setiap email pemasaran
- Batal langganan diproses segera (dalam 10 hari kerja yang diperlukan, kami melakukannya secara instan)
- Nama "Dari" yang jelas (nama toko Anda)
- Alamat fisik di footer email
- Tidak ada judul subjek yang menipu

## Memahami Status Email di EmailOutbox

Ketika melihat **Sistem Email > Email Outbox**, Anda akan melihat bagaimana preferensi memengaruhi pengiriman email:

| Status | Arti | Alasan |
|--------|---------|--------|
| **Menunggu** | Email dalam antrian untuk dikirim | Preferensi memungkinkan email ini |
| **Dalam Antrian** | Dalam antrian pengiriman | Preferensi memungkinkan email ini |
| **Dilewati** | Email tidak dikirim | Preferensi pelanggan dinonaktifkan |
| **Dikirim** | Berhasil dikirim | Email dikirim secara normal |

Ketika sebuah email **dilewati**, bidang `skip_reason` menunjukkan mengapa:

- **user_preference_disabled** — Pelanggan menonaktifkan jenis email ini di preferensi
- **email_not_verified** — Pelanggan belum memverifikasi alamat email mereka
- **email_disabled** — Pelanggan menonaktifkan semua email (toggle utama)

Jejak audit ini penting untuk kepatuhan GDPR — Anda dapat membuktikan bahwa Anda menghormati preferensi pelanggan.

## Pengaturan Situs untuk Preferensi

Navigasikan ke **Pengaturan > Pengaturan Situs** untuk mengonfigurasi default preferensi global:

**Aktifkan Double Opt-In untuk Email Pemasaran** (Default: Ya)
- Memerlukan verifikasi email sebelum mengirim email pemasaran
- Praktik terbaik GDPR
- Direkomendasikan: Biarkan aktif

**Status Default Pendaftaran Pemasaran** (Default: Tidak - Non-aktif)
- Status default ketika pelanggan baru mendaftar
- GDPR memerlukan non-aktif default
- Direkomendasikan: Biarkan sebagai non-aktif (False)

**Pusat Preferensi Aktif** (Default: Ya)
- Memungkinkan pelanggan mengelola preferensi mereka sendiri
- Diperlukan untuk hak GDPR menarik persetujuan
- Direkomendasikan: Biarkan aktif

**Memerlukan Verifikasi SMS** (Default: Tidak)
- Memerlukan verifikasi nomor telepon untuk pemberitahuan SMS
- Opsional tetapi direkomendasikan untuk pengirim SMS volume tinggi
- Dapat diaktifkan jika Anda ingin double opt-in untuk SMS

**Tampilkan Alasan Batal Langganan** (Default: Ya)
- Kumpulkan umpan balik opsional ketika pelanggan batal langganan
- Membantu memahami mengapa pelanggan memilih untuk batal langganan
- Direkomendasikan: Biarkan aktif untuk wawasan

## Praktik Terbaik

### 1. Default ke Non-aktif untuk Pemasaran

Selalu default komunikasi pemasaran ke **non-aktif** (tidak dicentang):
- Mematuhi GDPR
- Membangun kepercayaan dengan pelanggan
- Mengurangi keluhan spam
- Hanya kirim ke pelanggan yang aktif

### 2. Memerlukan Verifikasi Email

Biarkan **Double Opt-In** aktif:
- Memastikan alamat email valid
- Mengonfirmasi pelanggan benar-benar ingin menerima email pemasaran
- Mengurangi tingkat pengembalian
- Diperlukan untuk kepatuhan GDPR

### 3. Hormati Preferensi Langsung

Ketika pelanggan mengubah preferensi:
- Perubahan berlaku segera
- Cache preferensi dibatalkan
- Pengiriman email berikutnya akan memeriksa preferensi yang diperbarui
- Tidak ada penundaan dalam mematuhi permintaan batal langganan

### 4. Pantau Email yang Dilewati

Periksa secara teratur **Email Outbox** untuk email yang dilewati:
- Tingkat lewati tinggi menunjukkan pelanggan sedang batal langganan
- Mungkin menunjukkan konten email perlu diperbaiki
- Membantu mengidentifikasi masalah preferensi

### 5. Audit Kepatuhan Berkala

Ekspor preferensi secara berkala untuk kepatuhan:
1. Navigasikan ke **Preferensi Komunikasi**
2. Pilih semua pelanggan
3. Pilih **Ekspor Preferensi ke CSV**
4. Simpan untuk jejak audit GDPR

Simpan ekspor untuk **paling tidak 3 tahun** untuk mematuhi persyaratan retensi data GDPR.

### 6. Komunikasi yang Jelas

Ketika mengumpulkan persetujuan:
- Gunakan bahasa sederhana, bukan istilah hukum
- Jelaskan apa yang akan diterima pelanggan
- Tunjukkan frekuensi (harian, mingguan, bulanan)
- Jadikan kotak pendaftaran terlihat tetapi tidak dicentang secara default

### 7. Segmentasi Berdasarkan Preferensi

Ketika mengirim kampanye pemasaran:
- Hanya kirim ke pelanggan yang diverifikasi dan telah mendaftar
- Hormati preferensi aplikasi khusus (jangan kirim email blog ke pelanggan yang menonaktifkan blog)
- Gunakan preferensi frekuensi (jangan kirim email segera ke pelanggan yang berlangganan digest mingguan)

## Tips

**💡 Periksa Preferensi Sebelum Mengirim**

Sistem secara otomatis memeriksa preferensi ketika Anda mengirim email menggunakan `EmailSendingService.send_template_email()`. Pastikan semua pengiriman email menggunakan layanan ini, bukan panggilan SMTP langsung.

**💡 Status Dilewati adalah Normal**

Jangan khawatir dengan email yang dilewati di outbox — ini berarti sistem bekerja dengan benar dan menghormati preferensi pelanggan. Lebih baik melewati email yang tidak diinginkan daripada mengambil risiko denda GDPR atau keluhan spam.

**💡 Cache Preferensi 5 Menit**

Pemeriksaan preferensi dikach untuk 5 menit untuk kinerja. Ketika pelanggan mengubah preferensi melalui pusat preferensi atau tindakan admin, cache dibatalkan segera sehingga perubahan berlaku langsung.

**💡 Pelanggan Tamu Melewati Pemeriksaan**

Pelanggan checkout tamu (tanpa akun) akan menerima semua email secara normal karena mereka tidak memiliki catatan preferensi. Ini disengaja — mereka mendaftar dengan menyediakan email mereka di checkout.

**💡 Email Transaksional Selalu Dikirim**

Konfirmasi pesanan, pembaruan pengiriman, dan email keamanan akun **selalu dikirim** tanpa memandang preferensi. Ini memastikan pelanggan menerima informasi penting tentang pesanan dan akun mereka.

**💡 Gunakan Tindakan Massal dengan Hati-Hati**

Tindakan massal "Batal Langganan dari Semua Pemasaran" memengaruhi **semua aplikasi** (blog, loyalitas, referensi, afiliasi). Hanya gunakan ini untuk pelanggan yang secara eksplisit meminta untuk sepenuhnya batal langganan. Untuk preferensi tertentu, edit catatan pelanggan individu.

**💡 Jejak Audit untuk Kepatuhan**

Sistem melacak:
- Timestamp persetujuan dan sumber
- Alamat IP dan user agent
- Timestamp verifikasi email
- Setiap perubahan preferensi melalui status skipped EmailOutbox

Jejak audit ini membuktikan kepatuhan GDPR jika otoritas meminta bukti persetujuan.

## Topik Terkait

- [Mengelola Akun Pelanggan](/help/managing-customer-accounts) — Manajemen profil pelanggan
- [Konfigurasi Email](/help/email-configuration) — Pengaturan SMTP dan template email

Ingat: Pertahankan semua format markdown, jalur gambar, blok kode, dan istilah teknis persis seperti yang ditunjukkan dalam aturan preservasi.