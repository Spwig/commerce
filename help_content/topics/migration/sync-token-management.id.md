---
title: Manajemen Token Sinkronisasi
---

Token sinkronisasi adalah kredensial aman yang memungkinkan dua instalasi Spwig untuk berkomunikasi satu sama lain. Sebelum Anda dapat menyinkronkan pengaturan atau memindahkan data antar toko, Anda perlu menghasilkan token di toko **penerima** dan memberikannya ke toko **pengirim**.

## Cara Kerja Token Sinkronisasi

Token sinkronisasi adalah kunci API yang hanya dapat dilihat sekali yang mengautentikasi permintaan antara dua instalasi Spwig. Ketika Anda mengatur koneksi, toko jarak jauh menggunakan token ini untuk membuktikan bahwa mereka memiliki izin untuk membaca dari atau menulis ke toko Anda.

- Token dihasilkan di toko yang akan **terhubung ke** (target)
- Setiap token hanya dapat dilihat sekali, segera setelah dihasilkan
- Token dapat dicabut kapan saja untuk memutus akses secara instan
- Sebuah toko dapat memiliki beberapa token aktif untuk koneksi berbeda

## Menghasilkan Token

1. Navigasikan ke **Data Migration > Spwig-to-Spwig Sync** di sidebar admin
2. Klik **Manage Tokens** di dashboard sinkronisasi
3. Masukkan nama deskriptif untuk token (misalnya, "Staging Server" atau "Production Sync")
4. Klik **Generate Token**
5. **Salin token segera** -- token ini tidak akan ditampilkan lagi

> **Penting:** Simpan token secara aman. Jika Anda kehilangannya, Anda perlu menghasilkan yang baru.

## Menggunakan Token

Setelah Anda memiliki token dari toko target:

1. Pergi ke dashboard **Spwig-to-Spwig Sync** di toko yang akan memulai koneksi
2. Mulai **Settings Sync** atau **Full Migration** baru
3. Di langkah Koneksi, masukkan URL toko target dan tempelkan token
4. Klik **Test Connection** untuk memverifikasi bahwa koneksi bekerja
5. Koneksi akan disimpan untuk penggunaan di masa depan

## Membatalkan Token

Jika token terkompromi atau tidak lagi diperlukan:

1. Pergi ke **Manage Tokens** di dashboard sinkronisasi
2. Cari token yang ingin Anda cabut
3. Klik tombol **Revoke**
4. Konfirmasi pencabutan

Membatalkan token berlaku segera. Setiap koneksi aktif yang menggunakan token tersebut akan berhenti bekerja dan perlu dikonfigurasikan ulang dengan token baru.

## Praktik Terbaik

- **Berikan nama deskriptif pada token** agar Anda tahu token mana yang cocok untuk koneksi mana
- **Batalkan token yang tidak digunakan** untuk meminimalkan paparan keamanan
- **Buat token terpisah** untuk setiap toko yang terhubung, bukan berbagi satu token di beberapa toko
- **Buat ulang token secara berkala** sebagai bagian dari rutinitas keamanan Anda, terutama setelah perubahan staf