---
title: Akun vs Pelanggan
---

Pengusaha sering bertanya: "Apa perbedaan antara akun dan pelanggan?" Kebingungan ini umum terjadi karena setiap pelanggan adalah akun, tetapi tidak setiap akun adalah pelanggan. Panduan ini menjelaskan perbedaan tersebut dan menjelaskan kapan menggunakan masing-masing antarmuka admin.

![Daftar Pengguna](/static/core/admin/img/help/accounts-vs-customers/user-list.webp)

## Apa itu Akun?

Akun adalah objek otentikasi inti di Spwig. Siapa pun yang dapat masuk ke platform Anda — staf atau pelanggan — memiliki akun. Akun dikelola dalam sistem otentikasi Spwig dan disimpan dalam model `User`.

Semua akun memiliki:
- **Alamat email** — Identifikasi utama dan kredensial login
- **Nama pengguna** — Nama unik (dihasilkan secara otomatis dari email secara default)
- **Kata sandi** — Di-hash dan disimpan secara aman
- **Bendera is_staff** — Menentukan apakah akun dapat mengakses backend admin

Akun juga dapat melakukan otentikasi melalui penyedia OAuth (Google, Facebook, dll.) yang dikonfigurasikan di **Pengaturan > Otentikasi**.

## Apa itu Pelanggan?

Pelanggan adalah jenis akun khusus dengan `is_staff=False`. Pelanggan berbelanja di toko Anda, membuat pesanan, dan mengelola profil mereka. Setiap akun pelanggan secara otomatis diperpanjang dengan:

- **CustomerProfile** — Menyimpan preferensi, status pendaftaran newsletter, dan nilai bidang kustom
- **CustomerMetrics** — Melacak nilai seumur hidup (LTV), skor RFM, riwayat pesanan, dan data segmentasi
- **OrderHistory** — Tautan ke semua pesanan yang ditempatkan oleh pelanggan ini

Pelanggan dapat berupa:
- **Pelanggan terdaftar** — Dibuat melalui pendaftaran toko atau admin
- **Pengguna tamu** — Akun sementara yang dibuat selama checkout tamu (nama pengguna dimulai dengan `guest_`)
- **Pelanggan yang diimpor** — Digratifikasi dari platform lain melalui impor CSV

## Perbedaan Utama

| Atribut | Akun | Pelanggan |
|-----------|---------|----------|
| **Tujuan** | Otentikasi dan otorisasi | Berbelanja, pesanan, dan analitik |
| **Cakupan** | Staf dan pelanggan | Hanya pelanggan |
| **Bendera is_staff** | Benar atau salah | Selalu salah |
| **Data yang diperpanjang** | Tidak ada (hanya bidang inti) | CustomerProfile + CustomerMetrics |
| **Lokasi admin** | Pengaturan > Pengguna | Pelanggan > Profil Pelanggan |
| **Dapat masuk** | Ya | Ya |
| **Dapat menempatkan pesanan** | Hanya jika memiliki CustomerProfile | Ya |
| **Dapat mengakses admin** | Hanya jika is_staff=True | Tidak |

Secara singkat:
- Sebuah **akun** adalah siapa pun yang dapat masuk
- Sebuah **pelanggan** adalah akun yang berbelanja dan menempatkan pesanan

## Staf Juga Merupakan Akun

Staf adalah akun dengan `is_staff=True`. Mereka dapat masuk ke backend admin dan melakukan tindakan berdasarkan izin **StaffRole** yang ditugaskan.

Staf dapat memiliki **CustomerProfile** secara opsional jika mereka juga berbelanja di toko. Misalnya, jika Anda (pengusaha) menempatkan pesanan uji di toko Anda sendiri, CustomerProfile dibuat untuk akun staf Anda. Ini TIDAK memengaruhi akses admin Anda.

Izin staf dikontrol oleh:
- **StaffRole** — Menentukan bagian admin dan tindakan apa yang dapat diakses oleh staf
- **Bendera is_superuser** — Memberikan akses penuh tanpa batasan (gunakan secara hati-hati)

Kelola staf di **Pengaturan > Manajemen Staf**.

## Pengguna Tamu

Checkout tamu membuat akun sementara dengan nama pengguna yang dihasilkan secara otomatis yang dimulai dengan `guest_`. Akun-akun ini:
- Memiliki `is_staff=False` (mereka adalah pelanggan)
- Memiliki CustomerProfile (untuk asosiasi pesanan)
- Memiliki kata sandi acak (pengguna tamu tidak dapat masuk kecuali mereka berubah menjadi terdaftar)
- Secara default dikecualikan dari analitik pelanggan

Pengguna tamu dapat berubah menjadi pelanggan terdaftar dengan:
1. Membuat akun di toko dengan email yang sama
2. Memverifikasi alamat email mereka
3. Sistem menggabungkan riwayat pesanan tamu ke akun terdaftar baru

Kelola pengaturan konversi tamu di **Pengaturan > Checkout > Checkout Tamu**.

## Di Mana Anda Menemukan Masing-Masing

| Lokasi Admin | Apa yang Anda Kelola | Kasus Penggunaan Utama |
|----------------|-----------------|---------------|
| **Pengaturan > Pengguna** | Semua akun (staf + pelanggan) | Reset kata sandi, mengaktifkan/menonaktifkan akun, menetapkan izin staf |
| **Pengaturan > Manajemen Staf** | Akun staf hanya (is_staff=True) | Menetapkan peran, mengelola akses anggota tim, mengonfigurasi izin |
| **Pelanggan > Profil Pelanggan** | Akun pelanggan hanya (is_staff=False) | Lihat preferensi pelanggan, riwayat pesanan, LTV, skor RFM, segmen |
| **Pelanggan > Analitik** | Metrik dan segmen pelanggan | Analisis perilaku pelanggan, buat segmen pemasaran, lacak retensi |

![Daftar Profil Pelanggan](/static/core/admin/img/help/accounts-vs-customers/customer-profile-list.webp)

## Kapan Menggunakan Setiap Antarmuka

Gunakan **Pengaturan > Pengguna** ketika Anda perlu:
- Reset kata sandi pelanggan
- Menonaktifkan akun yang terinfeksi
- Membuat akun pelanggan secara manual
- Melihat koneksi login OAuth
- Melihat semua akun (staf + pelanggan) dalam satu daftar

Gunakan **Pengaturan > Manajemen Staf** ketika Anda perlu:
- Menambahkan anggota tim baru
- Menetapkan atau mengubah peran staf
- Mengonfigurasi izin granular
- Memeriksa log aktivitas staf

Gunakan **Pelanggan > Profil Pelanggan** ketika Anda perlu:
- Melihat riwayat pesanan pelanggan
- Melihat preferensi pelanggan dan nilai bidang kustom
- Memeriksa status langganan newsletter
- Melihat nilai seumur hidup (LTV) dan skor RFM pelanggan
- Mengelola segmen pelanggan

Gunakan **Pelanggan > Analitik** ketika Anda perlu:
- Mengidentifikasi pelanggan bernilai tinggi
- Membuat segmen pemasaran (misalnya, "pelanggan yang belum memesan dalam 90 hari")
- Menganalisis tren nilai seumur hidup pelanggan
- Mengekspor daftar pelanggan untuk kampanye

## Tips

- **Profil pelanggan dibuat secara otomatis** — Ketika pelanggan menempatkan pesanan pertama mereka (tamu atau terdaftar), Spwig membuat catatan CustomerProfile dan CustomerMetrics untuk analitik.
- **Staf juga bisa menjadi pelanggan** — Jika seorang staf menempatkan pesanan di toko, mereka mendapatkan CustomerProfile. Ini normal dan tidak memengaruhi akses admin mereka.
- **Akun tamu mengotori daftar pengguna** — Gunakan antarmuka profil pelanggan untuk fokus pada pelanggan yang benar-benar terlibat. Daftar pengguna mencakup semua akun tamu.
- **Segmentasi berdasarkan is_staff=False** — Ketika mengekspor daftar pelanggan untuk kampanye email, selalu saring untuk `is_staff=False` untuk mengecualikan anggota tim.
- **Akun OAuth juga merupakan akun** — Ketika pelanggan masuk melalui Google atau Facebook, Spwig membuat akun dan menghubungkannya dengan profil OAuth mereka. Bidang email diisi dari penyedia OAuth.

