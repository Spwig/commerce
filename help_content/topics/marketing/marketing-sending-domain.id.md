---
title: Domain Pengiriman Pemasaran
---

# Domain pengiriman pemasaran

Toko Anda mengirim dua jenis email yang sangat berbeda:

- **Transaksional** — konfirmasi pesanan, pembaruan pengiriman, reset kata sandi. Email ini
  harus selalu sampai ke kotak masuk.
- **Pemasaran** — buletin, promosi, pemulihan keranjang, peringatan stok tersedia kembali.

Secara default, keduanya dikirim di bawah identitas pengiriman yang sama, yang berarti mereka **berbagi satu
reputasi pengirim**. Jika kampanye pemasaran memicu keluhan spam atau mengenai alamat yang sudah tidak valid,
reputasi tersebut akan turun — dan konfirmasi pesanan serta reset kata sandi Anda bisa
mulai masuk ke folder spam juga.

**Domain pengiriman pemasaran** memperbaiki hal ini. Anda mengatur identitas pengiriman kedua — pada
subdomainnya sendiri seperti `news.yourstore.com` — dan menandainya untuk pemasaran. Spwig kemudian mengirim
setiap kampanye dari identitas tersebut dan tetap menggunakan email transaksional di domain utama Anda. Kampanye yang buruk
tidak lagi dapat menurunkan kualitas email yang *dibutuhkan* oleh pelanggan Anda.

> Ini berlaku untuk toko self-hosted. Pada paket yang di-hosting oleh Spwig, reputasi pengiriman
  dikelola untuk Anda.

## Bagaimana Spwig menentukan identitas yang digunakan

Setelah akun pengiriman pemasaran ada, routing bersifat otomatis — Anda tidak perlu menandai apa pun:

- **Email pemasaran** (kampanye, perjalanan, buletin, pemulihan keranjang, stok tersedia kembali) →
  domain pengiriman pemasaran.
- **Email transaksional** (pesanan, pengiriman, reset kata sandi, verifikasi) → domain utama
  Anda.

Jika Anda tidak pernah mengatur domain pemasaran, tidak ada yang berubah: semuanya terus dikirim
dari akun default Anda persis seperti sebelumnya.

## Mengaturnya

Anda dapat memulai dari salah satu titik masuk:

- Tombol **"Set up marketing domain"** pada banner dasbor Campaign Studio, atau
- **Email Accounts → "Marketing sending domain"**.

![Dasbor Campaign Studio dengan banner "Protect your transactional email" dan tombol Set up marketing domain-nya](/static/core/admin/img/help/marketing-sending-domain/marketing-domain-nudge.webp)

![Tombol Marketing sending domain pada daftar Email Accounts, di sebelah Browse Providers](/static/core/admin/img/help/marketing-sending-domain/marketing-domain-button.webp)

Keduanya membuka wizard pengaturan email yang sudah ditandai untuk akun pemasaran. Kemudian:

1. **Pilih subdomain.** Gunakan sesuatu seperti `news.yourstore.com` atau
   `mail.yourstore.com`. Ini adalah langkah yang paling penting: identitas pemasaran harus menjadi
   **(sub)domain yang berbeda** dari yang digunakan email transaksional Anda — pemisahan itulah
   yang melindungi reputasi transaksional Anda. Mengirim pemasaran dari domain
   utama Anda tidak memberikan isolasi apa pun.
2. **Masukkan alamat pengirim** pada subdomain tersebut, misalnya `news@news.yourstore.com`.
3. **Tambahkan rekaman DNS.** Wizard menghasilkan rekaman SPF, DKIM, dan DMARC untuk
   subdomain — termasuk kunci DKIM yang unik untuk identitas pemasaran ini. Tambahkan di
   penyedia DNS Anda (wizard memiliki tombol salin dan tab per penyedia), lalu jalankan
   pemeriksaan hingga semua rekaman lulus.
4. **Selesaikan.** Akun dibuat dan ditandai **Hanya Pemasaran**. Mulai sekarang, kampanye Anda
   dikirim darinya.

Anda dapat memastikan berhasil pada daftar **Email Accounts**: Anda akan melihat akun kedua dengan
kegunaan **Hanya Pemasaran**, dan banner Campaign Studio menghilang.

## Yang perlu diketahui

- **Anda tidak bisa secara tidak sengaja merusak email transaksional.** Spwig tidak akan membiarkan Anda mengatur satu-satunya
  akun Anda menjadi "Hanya Pemasaran", atau menonaktifkan/menghapus akun transaksional terakhir Anda — selalu
  ada tempat untuk konfirmasi pesanan dan reset kata sandi.
- **Hangatkan secara bertahap.** Domain pengiriman yang baru dibuat belum memiliki reputasi.

Naikkan volume
  Anda secara bertahap selama beberapa minggu daripada mengirim ke seluruh daftar Anda pada hari pertama.
- **Jaga DNS subdomain tetap sehat.** SPF, DKIM, dan DMARC pada subdomain pemasaran
  perlu tetap valid, sama seperti domain utama Anda.

Lihatlah [Buku Petunjuk Pengiriman Email](deliverability) untuk gambaran lengkapnya.
- **Persetujuan tetap berlaku.** Email pemasaran hanya dikirimkan ke pelanggan yang telah menyetujui penerimaannya,
  dan setiap kampanye mencakup tautan untuk berhenti berlangganan — memisahkan domain tidak mengubah apa pun dari itu.