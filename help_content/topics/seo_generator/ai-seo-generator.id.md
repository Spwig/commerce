---
title: Penghasil SEO AI
---

Penghasil SEO AI secara otomatis menulis judul meta, deskripsi meta, dan konten SEO lainnya untuk produk Anda menggunakan penyedia AI. Sebaliknya dari menulis konten SEO secara manual untuk setiap produk, Anda dapat menghasilkan konten yang akurat dan dioptimalkan secara massal dengan satu tindakan.

Toko Anda dilengkapi dengan penghasil SEO bawaan yang bekerja langsung. Anda juga dapat menginstal komponen penyedia AI tambahan dari pasar komponen Spwig untuk mengakses model bahasa yang lebih kuat.

## Cara penghasil SEO bekerja

Penghasil SEO membaca nama produk, deskripsi, kategori, dan atribut produk, lalu menggunakan penyedia AI yang dikonfigurasi untuk menulis konten SEO yang disesuaikan dengan produk tersebut. Konten yang dihasilkan disimpan langsung ke bidang SEO produk.

Anda dapat menghasilkan konten SEO untuk produk individual dari halaman edit produk, atau menjalankan pembuatan massal di beberapa produk dari daftar produk.

## Menyeting penyedia SEO

### Menggunakan penyedia bawaan

Toko Anda memiliki penyedia SEO bawaan yang menghasilkan konten SEO secara deterministik dari data produk Anda — tidak diperlukan kunci API eksternal. Ini secara otomatis diatur sebagai penyedia utama pada instalasi baru.

Untuk memverifikasi bahwa penyedia tersebut aktif:

1. Navigasikan ke **Pemasaran > Penyedia SEO**
2. Periksa bahwa penyedia bawaan muncul dengan badge **UTAMA** dan status **AKTIF**
3. Jika tidak ada penyedia yang terdaftar, klik **+ Tambah Akun Penyedia SEO** dan atur **Kunci Penyedia** menjadi `deterministic`

### Menghubungkan komponen penyedia AI

Untuk konten SEO yang lebih kaya dan kontekstual, Anda dapat menginstal komponen penyedia AI (seperti penyedia berbasis OpenAI atau Claude) dari pasar komponen Spwig.

1. Instal komponen penyedia melalui sistem pembaruan komponen (tanyakan administrator toko Anda)
2. Navigasikan ke **Pemasaran > Penyedia SEO**
3. Klik **+ Tambah Akun Penyedia SEO**
4. Isi formulir:

**Bagian Informasi Penyedia:**
- **Situs** — pilih toko Anda
- **Komponen Penyedia** — pilih komponen penyedia AI yang terinstal
- **Kunci Penyedia** — biarkan kosong saat menggunakan penyedia berbasis komponen
- **Nama Akun** — nama deskriptif seperti `Penyedia SEO OpenAI`

**Bagian Konfigurasi:**
- **Aktif** — centang untuk mengaktifkan penyedia ini
- **Utama** — centang untuk menggunakan penyedia ini sebagai penyedia default untuk semua pembuatan SEO
- **Prioritas** — angka yang lebih rendah dicoba terlebih dahulu dalam rantai fallback
- **Pengaturan** — pengaturan khusus penyedia sebagai objek JSON (misalnya, nama model, nada, bahasa)

5. Klik **Simpan**

Hanya satu penyedia yang dapat diatur sebagai utama. Jika Anda menandai penyedia baru sebagai utama, penyedia utama sebelumnya secara otomatis diturunkan statusnya.

### Rantai fallback penyedia

Jika penyedia utama Anda gagal (misalnya, karena gangguan API), toko Anda secara otomatis beralih ke penyedia aktif berikutnya berdasarkan urutan prioritas. Ini memastikan pembuatan SEO tetap berjalan bahkan jika satu penyedia sementara tidak tersedia.

## Membuat konten SEO untuk produk

### Produk individual

1. Navigasikan ke **Produk > Produk** dan buka produk apa pun
2. Gulir ke bagian **SEO** dari formulir produk
3. Klik tombol **Buat SEO**
4. Penyedia AI menghasilkan judul meta dan deskripsi meta berdasarkan detail produk
5. Periksa konten yang dihasilkan dan edit jika diperlukan
6. Klik **Simpan** untuk menerapkan perubahan

### Pembuatan massal

Untuk membuat atau memperbarui konten SEO untuk beberapa produk sekaligus:

1. Navigasikan ke **Produk > Produk**
2. Pilih produk yang ingin Anda perbarui menggunakan kotak centang mereka, atau pilih semua
3. Buka dropdown **Aksi**
4. Pilih **Buat Konten SEO** (atau nama aksi serupa — periksa dropdown untuk label yang tepat)
5. Klik **Lanjutkan**

Spwig mengantrekan tugas pembuatan dan memprosesnya di latar belakang. Segarkan daftar produk setelah satu atau dua menit untuk melihat bidang SEO yang diperbarui.

## Memeriksa cakupan SEO

Penghasil SEO melacak produk mana yang sudah memiliki konten SEO. Untuk mengidentifikasi produk yang masih membutuhkan SEO:

1.

Navigasikan ke **Produk > Produk**
2.


Gunakan filter **Status SEO** (jika tersedia) untuk menampilkan produk yang memiliki judul meta atau deskripsi yang hilang
3.

Pilih produk-produk tersebut dan jalankan tindakan pembuatan massal

## Pengaturan penyedia

Bidang **Pengaturan** pada akun penyedia SEO menerima objek JSON dengan konfigurasi khusus penyedia. Opsi umum meliputi:

```json
{
  "language": "en",
  "tone": "professional",
  "max_title_length": 60,
  "max_description_length": 160
}
```

Pengaturan ini bervariasi berdasarkan komponen penyedia. Lihat dokumentasi penyedia untuk daftar lengkap opsi yang tersedia.

## Mengelola beberapa penyedia

Jika Anda memiliki lebih dari satu akun penyedia SEO yang dikonfigurasi, daftar penyedia menampilkan statusnya secara sekilas:

- **Label PRIMARY** — penyedia ini digunakan untuk semua pembuatan SEO secara default
- **Label ACTIVE** — penyedia ini aktif
- **Label INACTIVE** — penyedia ini dinonaktifkan dan tidak akan digunakan

Untuk mengubah penyedia mana yang menjadi utama, buka akun penyedia yang ingin Anda tingkatkan, centang kotak **Is Primary**, dan simpan. Sistem secara otomatis memastikan hanya satu penyedia yang memiliki label utama pada waktu tertentu.

## Tips

- Buat konten SEO untuk produk baru segera setelah membuatnya — hanya memakan beberapa detik dan memberikan sesuatu yang berguna untuk diindeks oleh mesin pencari segera
- Periksa deskripsi meta yang dihasilkan oleh AI sebelum menerbitkan jika produk Anda memiliki nama yang tidak biasa atau teknis; generator bekerja terbaik dengan nama produk yang jelas dan deskriptif
- Tetapkan "max_title_length": 60 dan "max_description_length": 160 dalam pengaturan penyedia untuk menjaga konten yang dihasilkan tetap dalam batas karakter yang disarankan oleh Google
- Jalankan pembuatan SEO massal setelah mengimpor katalog produk besar untuk dengan cepat mengisi semua bidang SEO
- Jika Anda memperbarui deskripsi produk secara signifikan, buat ulang konten SEO-nya untuk menjaga tag meta selaras dengan teks baru
- Penyedia bawaan deterministik adalah titik awal yang baik; naikkan ke komponen berbasis AI setelah katalog Anda siap dan Anda ingin konten SEO yang lebih kaya dan terdengar lebih alami