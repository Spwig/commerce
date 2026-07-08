---
title: Manajemen Blog
---

Blog memungkinkan Anda menerbitkan artikel, panduan, dan berita untuk menarik lalu lintas dan memengaruhi audiens Anda. Blog Spwig mencakup editor teks kaya, jadwal penerbitan, notifikasi pelanggan, berbagi otomatis ke media sosial, dan alat SEO.

![Blog posts](/static/core/admin/img/help/blog-management/blog-post-list.webp)

## Membuat Posting Blog

Navigasikan ke **Marketing > Blog Posts** dan klik **Add Post**.

### Konten Posting

Tulis posting Anda menggunakan editor teks kaya **CKEditor 5**, yang mendukung:
- Pemformatan teks (judul, teks tebal, miring, daftar, kutipan teks)
- Gambar dan media (diunggah melalui perpustakaan media)
- Video tersemat (YouTube, Vimeo)
- Tabel dan blok kode
- Tautan ke produk, kategori, dan URL eksternal

Untuk tata letak yang lebih kompleks, aktifkan toggle **Page Builder** untuk menggunakan pembangun halaman drag-and-drop alih-alih editor teks.

### Pengaturan Posting

| Pengaturan | Deskripsi |
|---------|-------------|
| **Judul** | Judul yang ditampilkan di blog dan dalam hasil pencarian |
| **Slug** | Identifier yang ramah URL (dihasilkan secara otomatis dari judul, dapat diedit) |
| **Ringkasan** | Ringkasan pendek yang ditampilkan di kartu daftar blog dan feed RSS |
| **Gambar Unggulan** | Gambar utama yang ditampilkan di bagian atas posting dan di kartu daftar |
| **Kategori** | Kategori utama untuk posting |
| **Tag** | Kata kunci untuk pengfilteran dan konten terkait |
| **Penulis** | Anggota staf yang dikreditkan sebagai penulis |
| **Status** | Draft, Jadwal, Diterbitkan, atau Dikarantina |
| **Unggulan** | Pin posting ke bagian atas daftar blog |

### Pengaturan SEO

Setiap posting mencakup bidang SEO:
- **Meta Judul** — Judul kustom untuk hasil mesin pencari (defaultnya adalah judul posting)
- **Meta Deskripsi** — Ringkasan yang ditampilkan dalam hasil mesin pencari
- **Gambar Open Graph** — Gambar yang digunakan saat posting dibagikan ke media sosial

## Status Posting

| Status | Deskripsi |
|--------|-------------|
| **Draft** | Masih dalam proses, tidak terlihat oleh publik |
| **Jadwal** | Akan diterbitkan secara otomatis pada tanggal dan waktu yang ditetapkan |
| **Diterbitkan** | Aktif dan terlihat oleh pengunjung |
| **Dikarantina** | Tersembunyi dari daftar blog tetapi masih dapat diakses melalui URL langsung |

### Jadwal Posting

Untuk menjadwalkan posting untuk penerbitan di masa depan:
1. Atur status menjadi **Jadwal**
2. Pilih **tanggal dan waktu penerbitan**
3. Simpan posting

Tugas latar belakang secara otomatis menerbitkan posting pada waktu yang dijadwalkan dan memicu notifikasi pelanggan.

## Kategori

Navigasikan ke **Marketing > Blog Categories** untuk mengorganisir konten Anda.

Kategori mendukung:
- **Hierarki** — Buat kategori induk dan anak (misalnya, "Panduan" > "Getting Started")
- **URL Kustom** — Setiap kategori memiliki slug khusus untuk URL yang bersih
- **Deskripsi** — Tambahkan deskripsi kategori yang ditampilkan di halaman arsip kategori
- **Pengurutan** — Kontrol urutan tampilan kategori dalam navigasi

## Tag

Tag memberikan cara sekunder untuk mengklasifikasikan konten. Berbeda dengan kategori (yang bersifat hierarkis), tag adalah label datar. Pengunjung dapat mengklik tag untuk melihat semua posting dengan tag tersebut.

## Pelanggan

Navigasikan ke **Marketing > Blog Subscribers** untuk mengelola daftar pelanggan Anda.

### Cara Kerja Langganan

1. Pengunjung mendaftar melalui formulir di blog (alamat email diperlukan)
2. Email konfirmasi **double opt-in** dikirim
3. Setelah dikonfirmasi, pelanggan menerima notifikasi saat posting baru diterbitkan

### Frekuensi Notifikasi

Pelanggan memilih seberapa sering mereka menerima notifikasi:

| Frekuensi | Deskripsi |
|-----------|-------------|
| **Segera** | Email dikirim segera setelah posting baru diterbitkan |
| **Ringkasan Mingguan** | Ringkasan mingguan dari semua posting baru |
| **Ringkasan Bulanan** | Ringkasan bulanan dari semua posting baru |

Tugas latar belakang menangani kompilasi dan pengiriman ringkasan secara otomatis.

### Mengelola Pelanggan

- Lihat jumlah pelanggan, status konfirmasi, dan tanggal pendaftaran
- Ekspor daftar pelanggan untuk digunakan dalam alat pemasaran email eksternal
- Hapus atau batalkan langganan alamat individu
- Setiap email notifikasi mencakup tautan **batalkan langganan** dengan satu klik

## Berbagi Otomatis ke Media Sosial

Spwig dapat secara otomatis membagikan posting baru ke akun media sosial Anda saat mereka diterbitkan.

### Menghubungkan Akun Media Sosial

Navigasikan ke **Marketing > Social Connectors** untuk menghubungkan akun Anda:

| Platform | Otentikasi |
|----------|---------------|
| **Facebook** | OAuth — hubungkan halaman Facebook Anda |
| **Instagram** | OAuth — hubungkan akun bisnis Anda |
| **LinkedIn** | OAuth — hubungkan halaman perusahaan Anda |

### Cara Berbagi Otomatis Bekerja

1. Hubungkan satu atau lebih akun media sosial
2. Saat membuat posting, aktifkan **Auto Share** untuk setiap akun terhubung
3. Kustomisasi pesan berbagi (defaultnya adalah judul dan ringkasan posting)
4. Saat posting diterbitkan (atau mencapai waktu yang dijadwalkan), secara otomatis dibagikan

Berbagi otomatis juga bekerja dengan posting yang dijadwalkan — berbagi media sosial dikirim pada waktu yang sama posting menjadi hidup.

## Feed RSS

Blog secara otomatis menghasilkan feed RSS di `/blog/feed/`. Ini memungkinkan pengunjung dan agregator untuk berlangganan konten Anda. Feed mencakup:
- Judul dan ringkasan posting
- Tanggal penerbitan
- Informasi penulis
- Tautan langsung ke posting lengkap

## Pengaturan Blog

Navigasikan ke **Marketing > Blog Settings** untuk mengonfigurasi opsi blog global:

- **Posts Per Page** — Jumlah posting yang ditampilkan per halaman dalam daftar
- **Allow Comments** — Aktifkan atau nonaktifkan komentar pada posting
- **Default Category** — Kategori cadangan untuk posting tanpa kategori yang ditetapkan
- **Social Sharing Buttons** — Tampilkan tombol berbagi pada halaman posting individu

## Tips

- Tulis posting dengan **SEO di benak** — gunakan judul yang deskriptif, isi meta deskripsi, dan sertakan kata kunci yang relevan secara alami dalam konten.
- Gunakan **penerbitan jadwal** untuk mempertahankan cadence pascakonten yang konsisten tanpa usaha manual.
- Aktifkan **berbagi otomatis** untuk memaksimalkan jangkauan — posting yang dibagikan ke media sosial segera setelah penerbitan mendapatkan interaksi terbanyak.
- Dorong pengunjung untuk **berlangganan** dengan menempatkan formulir langganan secara menonjol di blog Anda dan menggunakan ajakan bertindak yang menarik.
- Gunakan **kategori** untuk kelompok konten luas dan **tag** untuk topik spesifik — ini membantu pengunjung menemukan konten terkait.
- Tambahkan **gambar unggulan** ke setiap posting — posting dengan gambar bekerja lebih baik dalam hasil pencarian dan berbagi media sosial.
- Gunakan opsi **ringkasan mingguan atau bulanan** untuk pelanggan yang tidak ingin menerima email sering — ini mengurangi tingkat pembatalan langganan.