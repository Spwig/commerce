---
title: Pengaturan Otorisasi dan Masuk dengan Sosial
---

Otorisasi dan masuk dengan media sosial memungkinkan pelanggan untuk masuk ke toko Anda menggunakan akun Google, Apple, atau Microsoft yang sudah ada — tidak perlu membuat dan mengingat kata sandi baru lagi.

![Pengaturan Otorisasi](/static/core/admin/img/help/oauth-social-login/oauth-settings.webp)

## Apa itu Otorisasi / Masuk dengan Sosial?

Otorisasi adalah standar autentikasi yang aman yang memungkinkan pelanggan masuk menggunakan kredensial dari penyedia tepercaya seperti Google, Apple, atau Microsoft.

### Manfaat

- **Checkout yang Lebih Cepat** — Pelanggan melewati formulir pendaftaran dan masuk hanya dengan satu klik
- **Mengurangi Hambatan** — Tidak perlu membuat kata sandi, email verifikasi, atau alur kata sandi yang terlupakan
- **Konversi yang Lebih Baik** — Studi menunjukkan bahwa masuk dengan media sosial dapat meningkatkan tingkat konversi sebesar 20-40%
- **Keamanan yang Lebih Baik** — Kredensial tidak melewati toko Anda; otorisasi ditangani oleh penyedia
- **Kepercayaan Pelanggan** — Pelanggan percaya penyedia yang sudah mapan dengan kredensial masuk mereka

### Cara Kerjanya

1. Pelanggan mengklik "Masuk dengan Google" (atau Apple/Microsoft) di halaman masuk Anda
2. Mereka dialihkan ke halaman masuk aman penyedia
3. Pelanggan mengautentikasi dengan kredensial penyedia
4. Penyedia mengirimkan informasi identitas yang diverifikasi kembali ke toko Anda
5. Pelanggan masuk secara otomatis

Pada masuk pertama, akun pelanggan baru dibuat secara otomatis menggunakan email dan informasi profil dari penyedia.

## Penyedia yang Didukung

Spwig mendukung tiga penyedia otorisasi utama:

| Penyedia | Penggunaan | Persyaratan Kredensial |
|----------|----------|------------------------|
| **Google** | Paling populer, paling mudah diatur | ID Klien, Kunci Rahasia Klien |
| **Apple** | Diperlukan untuk aplikasi iOS, berfokus pada privasi | ID Klien, ID Tim, ID Kunci, Kunci Rahasia |
| **Microsoft** | Pelanggan perusahaan, pengguna Office 365 | ID Klien, Kunci Rahasia Klien, ID Tenant |

Anda dapat mengaktifkan satu, dua, atau ketiga penyedia. Setiap penyedia beroperasi secara independen.

## Mengatur Otorisasi Google

Otorisasi Google adalah pilihan yang paling populer dan paling mudah dikonfigurasi.

### Prasyarat

- Akun Google
- Akses ke Google Cloud Console

### Pengaturan Langkah demi Langkah

1. **Navigasi ke Pengaturan Otorisasi**
   - Pergi ke **Pengaturan > Pengaturan Toko** di panel administrasi Anda
   - Gulir ke bagian **Penyedia Otorisasi**
   - Klik **Konfigurasi Google**

2. **Buat Proyek Google Cloud**
   - Kunjungi [Google Cloud Console](https://console.cloud.google.com/)
   - Klik **Buat Proyek**
   - Masukkan nama proyek (misalnya, "Otorisasi Toko Saya")
   - Klik **Buat**

3. **Aktifkan Google+ API**
   - Di bilah sisi kiri, pergi ke **APIs & Services > Library**
   - Cari "Google+ API"
   - Klik **Aktifkan**

4. **Buat Kredensial Otorisasi**
   - Pergi ke **APIs & Services > Credentials**
   - Klik **Buat Kredensial > ID Klien Otorisasi**
   - Pilih jenis aplikasi: **Aplikasi Web**
   - Masukkan nama (misalnya, "Login Toko")

5. **Konfigurasi URI Arahkan Kembali**
   - Di bawah **URI Arahkan Kembali yang Diizinkan**, tambahkan:
     ```
     https://yourdomain.com/accounts/google/login/callback/
     ```
   - Ganti `yourdomain.com` dengan domain Anda yang sebenarnya
   - Klik **Buat**

6. **Salin Kredensial**
   - Salin **ID Klien** dan **Kunci Rahasia Klien** dari popup

7. **Masukkan Kredensial ke Spwig**
   - Kembali ke pengaturan otorisasi administrasi Spwig
   - Tempel ID Klien dan Kunci Rahasia Klien
   - Klik **Simpan**
   - Ubah **Aktifkan Otorisasi Google** menjadi aktif

### Pengujian

- Kunjungi halaman login toko Anda
- Cari tombol "Masuk dengan Google"
- Klik dan autentikasi dengan akun Google Anda
- Anda harus masuk dan dialihkan ke dashboard pelanggan Anda

## Mengatur Otorisasi Apple

Otorisasi Apple lebih kompleks daripada Google karena sistem otorisasi berbasis kunci.

### Prasyarat

- Akun Pengembang Apple (anggota berbayar diperlukan)
- Akses ke portal pengembang Apple

### Pengaturan Langkah demi Langkah

1. **Navigasi ke Pengaturan Otorisasi**
   - Pergi ke **Pengaturan > Pengaturan Toko > Penyedia Otorisasi**
   - Klik **Konfigurasi Apple**

2. **Buat ID Layanan**
   - Masuk ke [Apple Developer](https://developer.apple.com/account/)
   - Pergi ke **Sertifikat, Identitas & Profil**
   - Klik **Identitas** dan kemudian tombol **+**
   - Pilih **ID Layanan** dan klik **Lanjutkan**
   - Masukkan deskripsi (misalnya, "Login Toko")
   - Masukkan identitas (misalnya, `com.yourstore.login`)
   - Klik **Lanjutkan** dan kemudian **Daftarkan**

3. **Konfigurasi ID Layanan**
   - Klik ID Layanan yang baru saja Anda buat
   - Centang **Masuk dengan Apple**
   - Klik **Konfigurasi**
   - Tambahkan domain Anda dan URL kembali:
     - **Domain**: `yourdomain.com`
     - **URL Kembali**: `https://yourdomain.com/accounts/apple/login/callback/`
   - Klik **Simpan** dan kemudian **Lanjutkan** dan **Simpan** lagi

4. **Buat Kunci**
   - Di bilah sisi kiri, klik **Kunci** dan kemudian tombol **+**
   - Masukkan nama kunci (misalnya, "Kunci Otorisasi Toko")
   - Centang **Masuk dengan Apple**
   - Klik **Konfigurasi** dan pilih ID Aplikasi Utama Anda
   - Klik **Simpan**, lalu **Lanjutkan** dan **Daftarkan**
   - **Unduh file kunci** (.p8) — Anda tidak dapat mengunduhnya lagi

5. **Kumpulkan Informasi yang Diperlukan**
   Anda memerlukan:
   - **ID Klien** (ID Layanan): Identitas yang Anda buat (misalnya, `com.yourstore.login`)
   - **ID Tim**: Ditemukan di bagian kanan atas portal pengembang Apple
   - **ID Kunci**: Tampil saat Anda membuat kunci
   - **Kunci Rahasia**: Isi dari file .p8 yang Anda unduh

6. **Masukkan Kredensial ke Spwig**
   - Kembali ke pengaturan otorisasi Spwig
   - Tempel ID Klien, ID Tim, dan ID Kunci
   - Buka file .p8 di editor teks dan salin isinya
   - Tempel seluruh kunci (termasuk header) ke bidang Kunci Rahasia
   - Klik **Simpan**
   - Ubah **Aktifkan Otorisasi Apple** menjadi aktif

### Pengujian

- Kunjungi halaman login toko Anda di perangkat dengan ID Apple
- Klik "Masuk dengan Apple"
- Autentikasi dengan ID Apple Anda
- Anda harus masuk dengan sukses

## Mengatur Otorisasi Microsoft

Otorisasi Microsoft ideal untuk toko yang menargetkan pelanggan bisnis yang menggunakan Office 365 atau Azure AD.

### Prasyarat

- Akun Microsoft
- Akses ke Azure Portal

### Pengaturan Langkah demi Langkah

1. **Navigasi ke Pengaturan Otorisasi**
   - Pergi ke **Pengaturan > Pengaturan Toko > Penyedia Otorisasi**
   - Klik **Konfigurasi Microsoft**

2. **Daftarkan Aplikasi di Azure**
   - Kunjungi [Azure Portal](https://portal.azure.com/)
   - Pergi ke **Azure Active Directory > Registrasi Aplikasi**
   - Klik **Registrasi Aplikasi Baru**
   - Masukkan nama (misalnya, "Otorisasi Toko")
   - Pilih **Akun dalam direktori organisasi apa pun dan akun pribadi Microsoft**
   - Di bawah **URI Arahkan Kembali**, pilih **Web** dan masukkan:
     ```
     https://yourdomain.com/accounts/microsoft/login/callback/
     ```
   - Klik **Daftar**

3. **Salin ID Aplikasi**
   - Di halaman ringkasan aplikasi, salin **ID Aplikasi (klien)**

4. **Buat Kunci Klien**
   - Di bilah sisi kiri, klik **Sertifikat & Rahasia**
   - Klik **Rahasia Klien Baru**
   - Masukkan deskripsi (misalnya, "Rahasia Otorisasi")
   - Pilih periode kedaluwarsa (dianjurkan: 24 bulan)
   - Klik **Tambahkan**
   - **Salin nilai rahasia segera** — nilai ini tidak akan ditampilkan lagi

5. **Masukkan Kredensial ke Spwig**
   - Kembali ke pengaturan otorisasi Spwig
   - Tempel ID Aplikasi (klien) sebagai ID Klien
   - Tempel nilai rahasia sebagai Kunci Rahasia Klien
   - Secara opsional masukkan ID Tenant (untuk aplikasi tunggal; kosongkan untuk multi-tenant)
   - Klik **Simpan**
   - Ubah **Aktifkan Otorisasi Microsoft** menjadi aktif

### Pengujian

- Kunjungi halaman login toko Anda
- Klik "Masuk dengan Microsoft"
- Autentikasi dengan akun Microsoft Anda
- Anda harus masuk dengan sukses

## Mengelola Koneksi Otorisasi

### Tampilan Pelanggan

Pelanggan dapat melihat dan mengelola penyedia otorisasi yang terhubung dari dashboard akun mereka:

- Navigasi ke **Akun Saya > Akun Terhubung**
- Lihat penyedia yang terhubung (Google, Apple, Microsoft)
- Putuskan koneksi penyedia dengan mengklik **Putuskan Koneksi**
- Hubungkan kembali dengan masuk menggunakan penyedia tersebut lagi

### Penyedia Banyak

Satu akun pelanggan dapat terhubung ke beberapa penyedia otorisasi. Misalnya, seorang pelanggan dapat menghubungkan Google dan Apple ke akun yang sama.

Jika seorang pelanggan mencoba untuk masuk dengan penyedia otorisasi yang berbeda menggunakan alamat email yang sama, Spwig secara otomatis menghubungkannya ke akun yang sudah ada.

### Manajemen Admin

Sebagai admin, Anda dapat melihat koneksi otorisasi pelanggan:

- Pergi ke **Pelanggan > Pelanggan**
- Buka catatan pelanggan
- Gulir ke bagian **Akun Terhubung**
- Lihat penyedia yang terhubung dan kapan mereka terhubung

Anda tidak dapat memutuskan koneksi penyedia atas nama pelanggan — mereka harus melakukannya sendiri untuk alasan keamanan.

## Penyelesaian Masalah

### Mismatch URI Arahkan Kembali

**Kesalahan**: "Mismatch URI Arahkan Kembali" atau "Invalid redirect_uri"

**Solusi**:
- Pastikan URI arahkan kembali di pengaturan penyedia Anda persis cocok dengan yang di Spwig
- Periksa apakah ada slash akhir — mereka harus cocok
- Verifikasi bahwa Anda menggunakan `https://` (bukan `http://`)
- Bersihkan cache browser Anda dan coba lagi

### Kredensial Tidak Valid

**Kesalahan**: "Invalid client ID" atau "Autentikasi gagal"

**Solusi**:
- Periksa kembali apakah Anda menyalin ID Klien dan Kunci Rahasia Klien dengan benar
- Pastikan tidak ada spasi tambahan atau baris baru
- Verifikasi kredensial berasal dari proyek/app yang benar
- Untuk Apple, pastikan Kunci Rahasia mencakup seluruh isi file .p8

### API Penyedia Tidak Aktif

**Kesalahan**: "API tidak aktif" atau "Akses tidak dikonfigurasi"

**Solusi**:
- Untuk Google: Pastikan Anda mengaktifkan Google+ API di proyek Google Cloud Anda
- Untuk Microsoft: Verifikasi pendaftaran aplikasi Anda disetujui dan aktif
- Untuk Apple: Periksa apakah "Masuk dengan Apple" diaktifkan untuk ID Layanan Anda

### SSL Diperlukan

**Kesalahan**: "Otorisasi memerlukan HTTPS" atau "URI arahkan kembali tidak aman"

**Solusi**:
- Penyedia otorisasi memerlukan SSL/TLS (HTTPS) untuk keamanan
- Pastikan toko Anda memiliki sertifikat SSL yang valid terinstal
- Perbarui URI arahkan kembali Anda untuk menggunakan `https://` alih-alih `http://`
- Jika menguji secara lokal, gunakan layanan seperti ngrok untuk membuat tunnel HTTPS

### Tombol Tidak Muncul

**Masalah**: Tombol "Masuk dengan Google/Apple/Microsoft" tidak muncul di halaman masuk

**Solusi**:
- Pastikan penyedia diaktifkan di pengaturan otorisasi
- Bersihkan cache browser Anda dan perbarui halaman
- Periksa apakah tema Anda mencakup template masuk dengan media sosial
- Periksa konsol browser untuk kesalahan JavaScript

## Tips & Praktik Terbaik

### Keamanan

- **Putar ulang rahasia secara berkala** — Perbarui Kunci Rahasia Klien setiap 12-24 bulan
- **Pantau upaya masuk yang gagal** — Perhatikan pola autentikasi yang tidak biasa
- **Gunakan kredensial terpisah per lingkungan** — Kredensial berbeda untuk lingkungan pengujian dan produksi
- **Batasi URI arahkan kembali** — Tambahkan hanya URI yang diperlukan secara tepat

### Pengalaman Pengguna

- **Aktifkan ketiga penyedia** — Beri pelanggan pilihan; demografi berbeda memilih penyedia yang berbeda
- **Letakkan tombol secara menonjol** — Tombol masuk dengan media sosial harus berada di atas formulir email/kata sandi
- **Gunakan branding yang dikenal** — Pertahankan gaya tombol standar Google/Apple/Microsoft
- **Uji di perangkat mobile** — Alur otorisasi bekerja berbeda di browser mobile

### Kepatuhan

- **Kebijakan Privasi** — Terbuka bahwa Anda menggunakan penyedia otorisasi dan data apa yang Anda terima
- **Syarat dan Ketentuan** — Patuhi ketentuan penyedia (Google, Apple, Microsoft masing-masing memiliki persyaratan)
- **Minimisasi data** — Hanya minta informasi profil yang benar-benar Anda butuhkan

### Daftar Pemeriksaan Pengujian

Sebelum diluncurkan, uji:

- [ ] Masuk dengan setiap penyedia di desktop
- [ ] Masuk dengan setiap penyedia di perangkat mobile
- [ ] Masuk pertama kali (pembuatan akun)
- [ ] Masuk berikutnya (pemetaan akun)
- [ ] Masuk dengan email yang sama di berbagai penyedia
- [ ] Putuskan dan hubungkan kembali penyedia
- [ ] Alur pengaturan ulang kata sandi masih berfungsi untuk pengguna non-Otorisasi

Ingat: Pertahankan semua format markdown, jalur gambar, blok kode, dan istilah teknis secara tepat seperti yang ditunjukkan dalam aturan pelestarian.