---
title: Preferensi Komunikasi
---

Preferensi komunikasi memungkinkan pelanggan untuk mengontrol email dan pesan SMS apa yang mereka terima dari toko Anda. Sistem ini memastikan kepatuhan GDPR dan membantu Anda menghormati preferensi komunikasi pelanggan di semua saluran.

Navigasi ke **Pelanggan > Preferensi Komunikasi** di bilah sisi admin untuk mengelola preferensi komunikasi pelanggan.

## Memahami Preferensi Komunikasi

Sistem preferensi komunikasi memberikan pelanggan kontrol terperinci atas pesan yang mereka terima. Ini mencakup:

- **Email transaksional** — Konfirmasi pesanan penting, pembaruan pengiriman, email keamanan akun (selalu aktif)
- **Email pemasaran** — Buletin, promosi, rekomendasi produk (memerlukan opt-in)
- **Notifikasi khusus aplikasi** — Artikel blog, poin loyalitas, hadiah rujukan, komisi afiliasi
- **Notifikasi SMS** — Notifikasi pesan teks (memerlukan opt-in eksplisit sesuai TCPA)

Semua komunikasi pemasaran memerlukan persetujuan pelanggan dan verifikasi email untuk memastikan kepatuhan GDPR.

## Penjelasan Jenis Preferensi

### Komunikasi Transaksional (Selalu Aktif)

Pesan transaksional sangat penting untuk akun dan pesanan pelanggan Anda. Pesan ini **tidak dapat dinonaktifkan** oleh pelanggan:

| Jenis | Deskripsi | Contoh |
|------|-------------|----------|
| **Konfirmasi Pesanan** | Konfirmasi saat pesanan dibuat | Pesanan #12345 telah diterima |
| **Pembaruan Pengiriman** | Notifikasi saat status pesanan berubah | Pesanan Anda telah dikirim |
| **Konfirmasi Pembayaran** | Pembayaran diterima, pengembalian dana diproses | Pembayaran $49.99 dikonfirmasi |
| **Keamanan Akun** | Pengaturan ulang kata sandi, verifikasi email | Atur ulang kata sandi Anda |

### Komunikasi Pemasaran (Wajib Opt-In)

Pesan pemasaran memerlukan persetujuan pelanggan dan verifikasi email:

| Jenis | Deskripsi | Default |
|------|-------------|---------|
| **Buletin** | Buletin umum dan pembaruan | Opt-out |
| **Penawaran Promosional** | Penjualan, diskon, penawaran khusus | Opt-out |
| **Rekomendasi Produk** | Saran produk yang dipersonalisasi | Opt-out |
| **Kembali Stok** | Notifikasi saat produk kembali tersedia | Opt-out |

Pelanggan harus **memverifikasi alamat email mereka** sebelum menerima email pemasaran apa pun (persyaratan double opt-in GDPR).

### Preferensi Khusus Aplikasi

Pelanggan dapat mengontrol notifikasi dari fitur tertentu:

**Notifikasi Blog**
- Artikel blog baru diterbitkan (seketika, ringkasan mingguan, atau ringkasan bulanan)
- Langganan khusus kategori
- Preferensi frekuensi

**Program Loyalitas**
- Notifikasi poin yang diperoleh
- Kenaikan tier
- Hadiah terbuka
- Poin segera kedaluwarsa
- Bonus ulang tahun
- Penawaran kampanye

**Program Rujukan**
- Hadiah diterbitkan (pemberi rujukan dan yang dirujuk)
- Pendaftaran rujukan berhasil
- Hadiah segera kedaluwarsa
- Undangan rujukan

**Program Afiliasi**
- Komisi diperoleh
- Komisi disetujui atau ditolak
- Pembayaran diproses, selesai, atau gagal
- Laporan kinerja bulanan

### Notifikasi SMS (Wajib Opt-In Eksplisit)

Semua notifikasi SMS memerlukan **opt-in eksplisit** sesuai peraturan TCPA. Pelanggan harus secara aktif mencentang kotak opt-in SMS:

- **SMS Transaksional** — Pesanan dikirim, diterima (opt-in diperlukan)
- **SMS Pemasaran** — Promosi, penawaran khusus (opt-in terpisah diperlukan)

Bahkan SMS transaksional memerlukan opt-in karena pengiriman pesan teks yang tidak diminta diatur lebih ketat daripada email.

## Mengelola Preferensi Pelanggan di Admin

### Menampilkan Semua Preferensi

Navigasi ke **Pelanggan > Preferensi Komunikasi** untuk melihat semua preferensi pelanggan:

{
  "Column": "Deskripsi",
  "--------": "-------------",
  "**User Email**": "Alamat surel pelanggan (terhubung ke admin pengguna)",
  "**Email Status**": "Hijau ✓ jika surel diaktifkan, abu-abu ○ jika dinonaktifkan",
  "**SMS Status**": "Hijau ✓ jika SMS diaktifkan, abu-abu ○ jika dinonaktifkan",
  "**Marketing Status**": "Badge 'Opted In' atau 'Opted Out'",
  "**Verification Status**": "📧✓ jika surel diverifikasi, 📱✓ jika SMS diverifikasi",
  "**Consent Source**": "Di mana pelanggan menyetujui (pendaftaran, checkout, pusat preferensi)",
  "**Updated At**": "Waktu terakhir preferensi diubah"
}

### Pencarian Preferensi

Gunakan sidebar filter untuk menemukan pelanggan:

- **Email Aktif** — Ya/Tidak
- **SMS Aktif** — Ya/Tidak
- **Email Pemasaran** — Ya/Tidak (telah menyetujui pemasaran)
- **SMS Pemasaran** — Ya/Tidak (telah menyetujui pemasaran SMS)
- **Email Diverifikasi** — Ya/Tidak (telah memverifikasi alamat surel mereka)
- **SMS Diverifikasi** — Ya/Tidak (telah memverifikasi nomor telepon mereka)
- **Sumber Persetujuan** — Pendaftaran, Checkout, Pusat Preferensi, API, Migrasi
- **Kode Bahasa** — Bahasa unggulan untuk komunikasi

### Pencarian Preferensi

Cari pelanggan berdasarkan:
- Alamat surel pengguna
- Nama pengguna
- Nama depan
- Nama belakang
- Token pembatalan langganan

### Tindakan Massal

Pilih beberapa pelanggan dan terapkan tindakan massal:

**✓ Tandai Email sebagai Diverifikasi**
- Memverifikasi alamat surel pelanggan secara manual
- Berguna ketika mengimpor pelanggan dari sistem lain
- Menghapus cache preferensi untuk menerapkan perubahan secara langsung

**🚫 Batalkan Langganan Semua Pemasaran**
- Menonaktifkan semua komunikasi pemasaran (surel, SMS, semua aplikasi)
- Tetap mempertahankan email transaksional yang aktif
- Gunakan ini untuk pelanggan yang meminta untuk sepenuhnya tidak lagi berlangganan
- Mematuhi hak untuk menarik persetujuan sesuai GDPR

**📥 Ekspor Preferensi ke CSV**
- Mengekspor preferensi pelanggan ke spreadsheet
- Termasuk semua bidang preferensi dan pengaturan khusus aplikasi
- Berguna untuk audit kepatuhan dan analisis
- Format: CSV dengan header

## Pusat Preferensi Pengguna

Pelanggan dapat mengelola preferensi mereka sendiri di `/accounts/preferences/` ketika masuk.

### Fitur Pusat Preferensi

**Tindakan Cepat**
- **Langgani Semua Pemasaran** — Mengaktifkan semua komunikasi pemasaran dalam satu klik
- **Batal Langganan Semua** — Menonaktifkan semua komunikasi pemasaran (email transaksional tetap aktif)

**Kartu Preferensi**
- **Email Transaksional** — Baca saja (selalu aktif, dicatat sebagai "Wajib")
- **Komunikasi Pemasaran** — Menyalakan/mematikan dengan badge verifikasi
- **Preferensi Blog** — Aktifkan/matikan, pilih frekuensi (segera, mingguan, bulanan)
- **Program loyalitas** — Aktifkan/matikan jenis notifikasi individu
- **Program rujukan** — Aktifkan/matikan pemberitahuan hadiah
- **Program afiliasi** — Aktifkan/matikan pemberitahuan komisi dan pembayaran
- **Notifikasi SMS** — Mengaktifkan/mematikan SMS (menampilkan status verifikasi)

**Pembaruan Real-Time**
- Perubahan disimpan secara langsung melalui AJAX
- Tidak diperlukan reload halaman
- Umpan balik visual ketika disimpan

### Proses Verifikasi Email

Ketika pelanggan mengaktifkan email pemasaran:

1. Pelanggan menggeser "Email Pemasaran" ke ON
2. Sistem mengirim email verifikasi dengan tautan unik
3. Pelanggan mengklik tautan verifikasi
4. Email ditandai sebagai diverifikasi (badge 📧✓ muncul)
5. Email pemasaran akan dikirimkan sekarang

**Pelanggan yang belum diverifikasi TIDAK akan menerima email pemasaran** meskipun saklar dalam keadaan ON. Hal ini memastikan kepatuhan terhadap double opt-in GDPR.

## Pembatalan Langganan Satu Klik

Semua email pemasaran mencakup tautan pembatalan langganan di bagian bawah. Klik tautan ini:

1. Mengarahkan pelanggan ke `/accounts/unsubscribe/<token>/` (tidak memerlukan login)
2. Menampilkan apa yang sedang dibatalkan langgangannya
3. Memungkinkan umpan balik opsional (alasan pembatalan langganan)
4. Menonaktifkan komunikasi pemasaran
5. Tetap mempertahankan email transaksional yang aktif
6. Menyediakan tautan ke pusat preferensi lengkap

Pelanggan dapat berlangganan kembali kapan saja melalui pusat preferensi.

## Persyaratan Kepatuhan & Hukum

### Kepatuhan GDPR Pasal 7

Sistem memastikan kepatuhan penuh terhadap Pasal 7 GDPR:

Preserve semua format markdown, jalur gambar, blok kode, dan istilah teknis.

**✅ Bukti Persetujuan**
- Stempel waktu saat persetujuan diberikan
- Sumber persetujuan (registrasi, checkout, pusat preferensi)
- Alamat IP persetujuan
- User agent (informasi browser)

**✅ Persetujuan Terpisah**
- Email pemasaran dan transaksional adalah toggle terpisah
- Setiap aplikasi (blog, loyalitas, dll.) memerlukan persetujuan individual

**✅ Penarikan yang Mudah**
- Berlangganan ulang dengan satu klik di semua email pemasaran
- Pusat preferensi tersedia untuk semua pelanggan yang masuk
- Pembatalan berlangganan berlaku segera

**✅ Persetujuan Diberikan Secara Bebas**
- Default adalah opt-out untuk pemasaran (praktik terbaik GDPR)
- Tidak ada kotak yang sudah dicentang sebelumnya (pelanggan harus secara aktif memilih opt-in)

**✅ Persetujuan Spesifik dan Terinformasi**
- Deskripsi yang jelas tentang apa yang dikendalikan oleh setiap preferensi
- Preferensi tingkat aplikasi yang granular (bukan semua-atau-tidak-ada)

**✅ Persetujuan yang Dapat Diverifikasi**
- Double opt-in untuk email pemasaran
- Jejak audit melalui pelacakan status EmailOutbox

### Kepatuhan TCPA (Regulasi SMS AS)

Semua notifikasi SMS memerlukan **opt-in eksplisit**:

- Pelanggan harus secara aktif mencentang kotak opt-in SMS
- Kotak yang sudah dicentang sebelumnya tidak diizinkan
- Deskripsi yang jelas tentang apa yang mereka pilih untuk diikuti
- Opt-out yang mudah melalui pusat preferensi
- Semua pengiriman SMS dicatat untuk audit kepatuhan

### Kepatuhan CAN-SPAM (Regulasi Email AS)

Sistem memastikan kepatuhan CAN-SPAM:

- Tautan pembatalan berlangganan di setiap email pemasaran
- Pembatalan berlangganan diproses segera (diwajibkan dalam 10 hari kerja, kami melakukannya secara instan)
- Nama "From" yang jelas (nama toko Anda)
- Alamat fisik di footer email
- Tidak ada baris subjek yang menipu

## Memahami Status Email di EmailOutbox

Saat melihat **Sistem Email > Kotak Keluar Email**, Anda akan melihat bagaimana preferensi memengaruhi pengiriman email:

| Status | Arti | Alasan |
|--------|---------|--------|
| **Pending** | Email antre untuk dikirim | Preferensi mengizinkan email ini |
| **Queued** | Dalam antrean pengiriman | Preferensi mengizinkan email ini |
| **Skipped** | Email tidak dikirim | Preferensi pelanggan dinonaktifkan |
| **Sent** | Berhasil dikirim | Email dikirim secara normal |

Ketika email **dilewati**, field `skip_reason` menunjukkan alasannya:

- **user_preference_disabled** — Pelanggan menonaktifkan jenis email ini di preferensi
- **email_not_verified** — Pelanggan belum memverifikasi alamat email mereka
- **email_disabled** — Pelanggan menonaktifkan semua email (toggle utama)

Jejak audit ini penting untuk kepatuhan GDPR — Anda dapat membuktikan bahwa Anda menghormati preferensi pelanggan.

## Pengaturan Situs untuk Preferensi

Navigasi ke **Pengaturan > Pengaturan Situs** untuk mengonfigurasi default preferensi global:

**Aktifkan Double Opt-In untuk Email Pemasaran** (Default: Ya)
- Memerlukan verifikasi email sebelum mengirim email pemasaran
- Praktik terbaik GDPR
- Rekomendasi: Biarkan aktif

**Status Opt-In Pemasaran Default** (Default: Tidak - Opt-Out)
- Status default saat pelanggan baru mendaftar
- GDPR memerlukan opt-out secara default
- Rekomendasi: Biarkan sebagai opt-out (False)

**Pusat Preferensi Diaktifkan** (Default: Ya)
- Memungkinkan pelanggan mengelola preferensi mereka sendiri
- Diperlukan untuk hak GDPR untuk menarik persetujuan
- Rekomendasi: Biarkan aktif

**Wajibkan Verifikasi SMS** (Default: Tidak)
- Memerlukan verifikasi nomor telepon untuk notifikasi SMS
- Opsional tetapi direkomendasikan untuk pengirim SMS bervolume tinggi
- Dapat diaktifkan jika Anda ingin double opt-in untuk SMS

**Tampilkan Alasan Pembatalan Berlangganan** (Default: Ya)
- Mengumpulkan umpan balik opsional saat pelanggan membatalkan berlangganan
- Membantu memahami mengapa pelanggan memilih untuk keluar
- Rekomendasi: Biarkan aktif untuk wawasan

## Praktik Terbaik

### 1. Default ke Opt-Out untuk Pemasaran

Selalu defaultkan komunikasi pemasaran ke **opt-out** (tidak dicentang):
- Mematuhi GDPR
- Membangun kepercayaan dengan pelanggan
- Mengurangi keluhan spam
- Hanya kirim ke pelanggan yang terlibat

### 2. Wajibkan Verifikasi Email

Biarkan **Double Opt-In** tetap aktif:
- Memastikan alamat email valid
- Memastikan pelanggan benar-benar ingin email pemasaran
- Mengurangi tingkat pantulan (bounce rate)
- Diperlukan untuk kepatuhan GDPR

### 3. Hormati Preferensi Segera

Simpan semua format markdown, jalur gambar, blok kode, dan istilah teknis.

Ketika pelanggan mengubah preferensi:
- Perubahan berlaku segera
- Cache preferensi dinonaktifkan
- Pengiriman email berikutnya akan memeriksa preferensi yang diperbarui
- Tidak ada penundaan dalam menghormati permintaan pembatalan langganan

### 4. Pantau Email yang Dilewati

Periksa **Email Outbox** secara rutin untuk email yang dilewati:
- Tingkat skip yang tinggi menunjukkan pelanggan sedang membatalkan langganan
- Dapat menjadi sinyal bahwa konten email perlu diperbaiki
- Membantu mengidentifikasi masalah preferensi

### 5. Audit Kepatuhan Berkala

Ekspor preferensi secara berkala untuk kepatuhan:
1. Navigasi ke **Communication Preferences**
2. Pilih semua pelanggan
3. Pilih **Export Preferences to CSV**
4. Simpan untuk jejak audit GDPR

Simpan ekspor selama **minimal 3 tahun** untuk mematuhi persyaratan retensi data GDPR.

### 6. Komunikasi yang Jelas

Saat mengumpulkan persetujuan:
- Gunakan bahasa yang sederhana, bukan jargon hukum
- Jelaskan apa yang akan diterima pelanggan
- Tampilkan frekuensi (harian, mingguan, bulanan)
- Buat kotak opt-in menonjol tetapi tidak dicentang sebelumnya

### 7. Segmentasi Berdasarkan Preferensi

Saat mengirim kampanye pemasaran:
- Hanya kirim ke pelanggan yang terverifikasi dan telah memilih untuk berlangganan
- Hormati preferensi spesifik aplikasi (jangan kirim email blog ke pelanggan yang menonaktifkan blog)
- Gunakan preferensi frekuensi (jangan kirim email segera ke pelanggan langganan ringkasan mingguan)

## Tips

**💡 Periksa Preferensi Sebelum Mengirim**

Sistem secara otomatis memeriksa preferensi saat Anda mengirim email menggunakan `EmailSendingService.send_template_email()`. Pastikan semua pengiriman email menggunakan layanan ini, bukan panggilan SMTP langsung.

**💡 Status Dilewati adalah Normal**

Jangan panik dengan email yang dilewati di outbox — ini berarti sistem bekerja dengan benar dan menghormati preferensi pelanggan. Lebih baik melewatkan email yang tidak diinginkan daripada berisiko terkena denda GDPR atau keluhan spam.

**💡 Cache Preferensi adalah 5 Menit**

Pemeriksaan preferensi di-cache selama 5 menit untuk performa. Ketika pelanggan mengubah preferensi melalui pusat preferensi atau tindakan admin, cache segera dinonaktifkan sehingga perubahan berlaku langsung.

**💡 Pelanggan Tamu Melewati Pemeriksaan**

Pelanggan checkout tamu (tanpa akun) akan menerima semua email secara normal karena mereka tidak memiliki catatan preferensi. Ini disengaja — mereka memilih untuk berlangganan dengan memberikan email mereka saat checkout.

**💡 Email Transaksional Selalu Dikirim**

Konfirmasi pesanan, pembaruan pengiriman, dan email keamanan akun **selalu dikirim** terlepas dari preferensi. Ini memastikan pelanggan menerima informasi penting tentang pesanan dan akun mereka.

**💡 Gunakan Aksi Massal dengan Hati-hati**

Aksi massal "Unsubscribe from All Marketing" memengaruhi **semua aplikasi** (blog, loyalitas, rujukan, afiliasi). Hanya gunakan ini untuk pelanggan yang secara eksplisit meminta untuk sepenuhnya membatalkan langganan. Untuk preferensi spesifik, edit catatan pelanggan individu.

**💡 Jejak Audit untuk Kepatuhan**

Sistem melacak:
- Stempel waktu dan sumber persetujuan
- Alamat IP dan user agent
- Stempel waktu verifikasi email
- Setiap perubahan preferensi melalui status dilewati EmailOutbox

Jejak audit ini membuktikan kepatuhan GDPR jika otoritas pernah meminta bukti persetujuan.

## Topik Terkait

- [Managing Customer Accounts](/help/managing-customer-accounts) — Manajemen profil pelanggan
- [Email Configuration](/help/email-configuration) — Pengaturan SMTP dan template email