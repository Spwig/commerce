---
title: Wilayah Penjualan
---

Wilayah penjualan memungkinkan Anda mendefinisikan pasar geografis untuk toko Anda dan mengontrol produk mana yang tersedia di setiap wilayah. Ini berguna ketika Anda menjual di beberapa negara atau wilayah dan memerlukan katalog produk yang berbeda, mata uang regional, atau ketersediaan stok per lokasi.

## Apa itu wilayah penjualan?

Wilayah penjualan adalah area geografis yang diberi nama dan terdiri dari satu atau lebih negara. Setiap wilayah memiliki mata uang default, prioritas, dan dapat dikaitkan dengan satu atau lebih gudang. Ketika seorang pelanggan menjelajahi toko Anda, Spwig menentukan wilayah mereka berdasarkan lokasi mereka dan menerapkan aturan mata uang dan visibilitas produk yang sesuai.

Kasus penggunaan umum:
- Menampilkan hanya produk yang tersedia secara lokal kepada pelanggan di setiap negara
- Menetapkan mata uang default yang spesifik untuk wilayah (misalnya, NZD untuk pelanggan Selandia Baru)
- Mengontrol gudang mana yang menangani pesanan untuk setiap wilayah
- Menyembunyikan produk yang belum tersedia di pasar tertentu

## Membuat wilayah penjualan

1. Navigasikan ke **Katalog > Wilayah Penjualan**
2. Klik **+ Tambah Wilayah Penjualan**
3. Isi detail wilayah:

| Field | Description | Example |
|-------|-------------|---------|
| **Nama Wilayah** | Nama tampilan untuk wilayah ini | `Asia-Pacific` |
| **Kode Wilayah** | Identifikasi unik singkat | `APAC` |
| **Negara** | Kode negara ISO yang termasuk dalam wilayah ini | `["NZ", "AU", "SG", "FJ"]` |
| **Mata Uang Default** | Kode mata uang ISO untuk wilayah ini | `NZD` |
| **Prioritas** | Wilayah dengan prioritas yang lebih tinggi cocok terlebih dahulu | `10` |
| **Aktif** | Apakah wilayah ini saat ini sedang digunakan | Dicentang |

4. Klik **Simpan**

### Kode negara

Masukkan negara sebagai daftar JSON dari kode ISO dua huruf. Contohnya:
- Selandia Baru dan Australia: `["NZ", "AU"]`
- Hanya Singapura: `["SG"]`
- Seluruh Eropa: `["DE", "FR", "IT", "ES", "NL", "BE", "AT", "CH", "SE", "NO", "DK", "FI", "PL"]`

### Prioritas

Jika negara pelanggan cocok dengan lebih dari satu wilayah, wilayah dengan angka prioritas tertinggi yang digunakan. Tetapkan prioritas yang lebih tinggi untuk wilayah yang lebih spesifik (misalnya, beri `NZ` prioritas 20 dan `APAC` prioritas 10 sehingga pelanggan Selandia Baru cocok dengan wilayah NZ terlebih dahulu).

## Mengontrol visibilitas produk berdasarkan wilayah

Secara default, setiap produk terlihat di semua wilayah. Untuk membatasi produk ke wilayah tertentu, gunakan catatan **Visibilitas Wilayah Produk**.

### Membatasi produk ke wilayah tertentu

1. Navigasikan ke **Katalog > Visibilitas Wilayah Produk**
2. Klik **+ Tambah Visibilitas Wilayah Produk**
3. Pilih **Produk**
4. Pilih **Wilayah**
5. Atur **Terlihat** menjadi on atau off sesuai kebutuhan
6. Klik **Simpan**

Setelah ada catatan visibilitas apa pun untuk produk, Spwig menerapkan aturan tersebut. Produk tanpa catatan visibilitas tetap terlihat di semua tempat.

### Pola umum

**Batas hanya ke satu wilayah**

Tambahkan satu catatan visibilitas per wilayah yang ingin Anda dukung, mengatur **Terlihat** menjadi `Ya` untuk wilayah yang diizinkan. Pelanggan di wilayah lain tidak akan melihat produk tersebut.

**Kecualikan dari satu wilayah**

Tambahkan satu catatan visibilitas untuk wilayah yang ingin Anda kecualikan dan atur **Terlihat** menjadi `Tidak`. Produk tetap terlihat di semua wilayah lain.

### Mengedit visibilitas dari halaman produk

Anda juga dapat mengelola visibilitas wilayah secara langsung dari formulir pengeditan produk. Di bagian **Visibilitas Wilayah** dari produk, Anda akan menemukan tabel inline yang menampilkan semua wilayah dan pengaturan visibilitas untuk produk tersebut.

## Mata uang regional

Setiap wilayah memiliki mata uang default. Pelanggan yang menjelajahi dari wilayah tersebut melihat harga yang ditampilkan dalam mata uang wilayah tersebut. Mata uang yang digunakan ditentukan saat checkout.

Untuk mengatur harga dalam beberapa mata uang, konfigurasikan tingkat pertukaran di bawah **Pengaturan > Tingkat Pertukaran**. Harga dapat dikonversi secara otomatis atau diatur secara manual per mata uang.

## Menghubungkan gudang ke wilayah

Gudang dikaitkan ke wilayah saat Anda membuat atau mengedit gudang di bawah **Katalog > Gudang**. Setiap gudang termasuk dalam satu wilayah, yang mengontrol stok wilayah mana yang digunakan untuk menyelesaikan pesanan.

Untuk detail lebih lanjut mengenai gudang, lihat topik bantuan **Inventory and Warehouses**.

## Tips

- Pertahankan kode wilayah singkat dan deskriptif (`NZ`, `APAC`, `EU`, `US`) — mereka digunakan secara internal dan dalam log.
- Gunakan angka prioritas yang lebih tinggi untuk wilayah yang lebih kecil dan spesifik agar mengambil alih wilayah yang lebih luas dan umum.
- Jika Anda hanya menjual ke satu negara, Anda tidak perlu mengonfigurasi wilayah sama sekali — Spwig berfungsi dengan baik menggunakan katalog global tunggal.
- Uji visibilitas berbasis wilayah dengan mempreview toko Anda sambil memfilter berdasarkan wilayah tertentu di admin.
- Catatan visibilitas produk hanya perlu dibuat ketika Anda ingin membatasi produk. Meninggalkan produk tanpa catatan visibilitas membuatnya tersedia secara universal.
- Periksa kembali aturan visibilitas Anda setiap kali Anda menambahkan wilayah baru untuk memastikan pembatasan produk yang sudah ada tetap benar.