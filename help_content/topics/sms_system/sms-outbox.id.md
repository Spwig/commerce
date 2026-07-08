---
title: Kotak Keluar SMS
---

Kotak Keluar SMS adalah catatan lengkap dari setiap pesan teks yang telah dicoba dikirimkan toko Anda. Gunakan untuk memastikan notifikasi telah sampai ke pelanggan, menyelidiki kegagalan pengiriman, dan memahami aktivitas pesan Anda secara keseluruhan.

Navigasikan ke **Sistem SMS > Kotak Keluar SMS** untuk melihat log pesan.

![Daftar Kotak Keluar SMS dengan badge status](/static/core/admin/img/help/sms-outbox/outbox-list.webp)

## Membaca kotak keluar

Setiap baris dalam kotak keluar mewakili satu upaya pengiriman pesan dan menampilkan:

- **Telepon** — nomor telepon penerima
- **Jenis Pesan** — SMS atau WhatsApp
- **Status** — status pengiriman saat ini (lihat di bawah)
- **Dibuat** — kapan pesan dibuat
- **Dikirim Pada** — kapan pesan dikirim ke penyedia

Baris ringkasan di bagian atas menampilkan jumlah agregat untuk status yang paling penting secara sekilas.

## Status Pesan

| Status | Arti |
|--------|---------|
| Menunggu | Pesan sedang menunggu untuk diambil oleh antrian pengiriman |
| Diantrikan | Pesan telah diantrikan dan akan segera dikirim |
| Dikirim | Penyedia menerima pesan untuk dikirimkan |
| Terkirim | Penyedia mengonfirmasi pesan telah sampai ke perangkat penerima |
| Gagal | Penyedia menolak atau tidak dapat mengirimkan pesan |
| Dilewati | Pengiriman sengaja dilewati (lihat alasan dilewati di bawah) |
| Dilogkan Sandbox | Pesan hanya dicatat (toko berada dalam mode uji/sandbox) |

> **Dikirim vs Terkirim:** Status **Dikirim** berarti pesan telah keluar dari toko Anda dan diterima oleh penyedia. Status **Terkirim** berarti penyedia menerima bukti pengiriman dari penyedia jasa. Tidak semua penyedia mendukung bukti pengiriman — jika penyedia Anda tidak mendukung, pesan mungkin menunjukkan **Dikirim** tetapi tidak pernah berkembang ke **Terkirim**, yang normal.

## Melihat detail pesan

Klik baris apa pun di kotak keluar untuk melihat detail lengkap pesan tersebut:

- Teks **Pesan** lengkap yang dikirim
- **ID Pesan Penyedia** — nomor referensi dari penyedia SMS (berguna saat menghubungi dukungan penyedia)
- **Pesan Kesalahan** (untuk pesan gagal) — pesan kesalahan yang tepat dikembalikan oleh penyedia
- **Jumlah Pengulangan** — seberapa banyak kali Spwig telah mencoba mengirim pesan tersebut
- Semua timestamp (dibuat, diantrikan, dikirim, terkirim)

## Memfilter kotak keluar

Gunakan filter di sisi kanan untuk menyempitkan daftar:

- **Status** — tampilkan hanya pesan dengan status tertentu
- **Jenis Pesan** — tampilkan hanya SMS atau hanya pesan WhatsApp
- **Tanggal** — filter berdasarkan hari pesan dibuat

Kotak pencarian di bagian atas memungkinkan Anda mencari berdasarkan nomor telepon, isi pesan, atau ID pesan penyedia.

## Memahami alasan dilewati

Pesan yang dilewati tidak dikirim karena Spwig menentukan pengiriman tidak tepat atau tidak diperlukan. Alasan umum dilewati:

| Alasan Dilewati | Artinya |
|-------------|---------------|
| `user_preference_disabled` | Pelanggan mematikan notifikasi SMS di pengaturan akun mereka |
| `unsubscribed` | Pelanggan telah berlanggan untuk SMS |
| `no_provider` | Tidak ada akun penyedia SMS default yang aktif dikonfigurasikan |
| `template_inactive` | Template untuk jenis notifikasi ini tidak aktif |

Pesan yang dilewati bukanlah kegagalan — ini berarti sistem berfungsi seperti yang dimaksudkan. Namun, jumlah tinggi dari `no_provider` dilewati menunjukkan bahwa Anda perlu mengonfigurasi dan mengaktifkan akun penyedia SMS.

## Menangani pengiriman yang gagal

Jika pesan menunjukkan status **Gagal**, ikuti langkah-langkah berikut:

1. Klik pesan yang gagal untuk melihat **Pesan Kesalahan**
2. Penyebab umum kesalahan:

   | Kesalahan | Penyebab kemungkinan |
   |-------|-------------|
   | Nomor telepon tidak valid | Nomor telepon pelanggan hilang atau tidak dalam format E.164 |
   | Autentikasi gagal | Kredensial penyedia Anda tidak valid atau sudah kedaluwarsa — perbarui di **SMS Provider Accounts** |
   | Akun ditangguhkan | Akun penyedia Anda telah ditangguhkan — masuk ke dashboard penyedia |
   | Dana tidak cukup | Saldo akun penyedia Anda terlalu rendah — tambah saldonya |
   | Penolakan oleh penyedia | Penyedia tujuan memblokir pesan (sering disebabkan oleh penyaringan konten) |

3. Setelah memperbaiki masalah mendasar, pesan masa depan akan dikirim secara normal — outbox hanya merupakan log yang dapat dibaca dan pesan individu tidak dapat dikirim ulang secara manual

## Outbox hanya dapat dibaca

Outbox SMS adalah catatan hanya. Anda tidak dapat menambahkan pesan ke outbox secara manual, dan Anda tidak dapat mengirim ulang pesan individu dari sini. Pesan dikirim secara otomatis oleh Spwig ketika kejadian relevan terjadi (misalnya, pesanan ditempatkan).

## Tips

- Periksa outbox setelah periode sibuk untuk memastikan semua pesan konfirmasi pesanan telah berhasil dikirim
- Jika seorang pelanggan mengatakan mereka tidak menerima SMS, cari outbox berdasarkan nomor telepon mereka untuk melihat apakah pesan dikirim, gagal, atau dilewati
- Lonjakan mendadak dalam pesan **Gagal** biasanya menunjukkan masalah dengan kredensial penyedia atau saldo akun Anda — periksa hal ini segera
- Jika Anda melihat banyak pesan **Dilewati** dengan alasan `no_provider`, navigasikan ke **SMS System > SMS Provider Accounts** dan pastikan akun default yang aktif dikonfigurasikan
- Hierarki tanggal di bagian atas daftar memungkinkan Anda menavigasi dengan cepat berdasarkan hari, bulan, atau tahun untuk meninjau pesan historis