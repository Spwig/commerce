---
title: Wilayah Penjualan
---

Wilayah penjualan memungkinkan Anda menentukan pasar geografis untuk toko Anda dan mengontrol produk mana yang tersedia di setiap wilayah. Ini berguna ketika Anda menjual di beberapa negara atau wilayah dan membutuhkan katalog produk yang berbeda, mata uang regional, atau ketersediaan stok per lokasi.

## Apa itu wilayah penjualan?

Wilayah penjualan adalah area geografis yang diberi nama yang terdiri dari satu atau lebih negara. Setiap wilayah memiliki mata uang default, prioritas, dan dapat dikaitkan dengan satu atau lebih gudang. Ketika pelanggan menjelajahi toko Anda, Spwig menentukan wilayahnya berdasarkan lokasinya dan menerapkan mata uang yang sesuai serta aturan visibilitas produk.

Contoh penggunaan umum:
- Menampilkan hanya produk yang tersedia secara lokal kepada pelanggan di setiap negara
- Menetapkan mata uang default yang spesifik wilayah (misalnya, NZD untuk pelanggan Selandia Baru)
- Mengontrol gudang mana yang memenuhi pesanan untuk setiap wilayah
- Menyembunyikan produk yang belum tersedia di pasar tertentu

## Membuat wilayah penjualan

1. Navigasi ke **Inventaris > Wilayah Penjualan**. Jika Anda tidak melihatnya, aktifkan **Aktifkan Banyak Gudang** di bawah **Pengaturan > Pengaturan Toko > E-Commerce** untuk menampilkan item menu — Anda tidak perlu menggunakan banyak gudang secara aktual untuk ini, hanya saja ini membuka kunci tautannya. Anda juga bisa langsung pergi ke `/admin/catalog/salesregion/`.
2. Klik **+ Tambah Wilayah Penjualan**
3. Isi detail wilayah:

| Kolom | Keterangan | Contoh |
|-------|-------------|---------|
| **Nama Wilayah** | Nama tampilan untuk wilayah ini | `Asia-Pasifik` |
| **Kode Wilayah** | Identifikasi unik singkat | `APAC` |
| **Negara** | Kode negara ISO yang termasuk dalam wilayah ini | `["NZ", "AU", "SG", "FJ"]` |
| **Mata Uang Default** | Kode mata uang ISO untuk wilayah ini | `NZD` |
| **Prioritas** | Wilayah dengan prioritas yang lebih tinggi akan dipilih terlebih dahulu | `10` |
| **Aktif** | Apakah wilayah ini saat ini digunakan | Cek |

4. Klik **Simpan**

### Kode negara

Masukkan negara-negara sebagai daftar JSON dua huruf kode ISO. Contohnya:
- Selandia Baru dan Australia: `["NZ", "AU"]`
- Hanya Singapura: `["SG"]`
- Seluruh Eropa: `["DE", "FR", "IT", "ES", "NL", "BE", "AT", "CH", "SE", "NO", "DK", "FI", "PL"]`

### Prioritas

Jika negara pelanggan cocok dengan lebih dari satu wilayah, wilayah dengan angka prioritas tertinggi yang digunakan. Tetapkan prioritas yang lebih tinggi untuk wilayah yang lebih spesifik (misalnya, beri `NZ` prioritas 20 dan `APAC` prioritas 10 sehingga pelanggan Selandia Baru dipilih ke wilayah `NZ` terlebih dahulu).

## Mengontrol visibilitas produk berdasarkan wilayah

Secara default, setiap produk terlihat di semua wilayah. Untuk membatasi produk, buka di bawah **Produk > Semua Produk** dan atur bidang **Ketersediaan Wilayah** (di bagian Status) untuk memungkinkan produk hanya di wilayah tertentu atau di semua wilayah kecuali wilayah tertentu, lalu pilih wilayah-wilayahnya di bawah tabel yang sesuai.

Ini juga menentukan apa yang dilihat pembeli di luar wilayah ketersediaan produk — apakah produknya disembunyikan dari daftar sepenuhnya, atau ditampilkan dengan pemberitahuan "Tidak dikirim ke [wilayah]". Lihat panduan **Ketersediaan Wilayah** untuk langkah-langkah lengkap, termasuk pengaturan tampilan ini dan Pemilih Pengiriman ke Pengguna Akhir.

## Mata Uang Regional

Setiap wilayah memiliki mata uang default. Jika toko Anda secara eksplisit mendukung lebih dari satu mata uang (**Pengaturan > Banyak Mata Uang**), mata uang yang ditampilkan pelanggan berubah menjadi mata uang default wilayahnya kapan pun wilayahnya berubah — apakah itu dari undangan wilayah otomatis atau Pemilih Pengiriman ke Pengguna Akhir. Toko dengan satu mata uang, atau yang belum secara sengaja mengaktifkan banyak mata uang, selalu menampilkan mata uang tunggal itu terlepasipun wilayahnya.

Untuk menyiapkan harga dalam beberapa mata uang, atur tingkat tukar di bawah **Pengaturan > Tingkat Tukar**. Harga dapat dikonversi secara otomatis atau diatur secara manual per mata uang.

## Menghubungkan gudang dengan wilayah

Gudang dihubungkan dengan wilayah ketika Anda membuat atau mengedit gudang di bawah **Katalog > Gudang**. Setiap gudang milik satu wilayah, yang mengontrol stok wilayah mana yang digunakan untuk memenuhi pesanan.

Untuk detail lebih lanjut mengenai gudang, lihat topik bantuan **Inventory dan Gudang**.

## Tips

- Pertahankan kode wilayah singkat dan deskriptif (NZ, APAC, EU, US) — mereka digunakan secara internal dan dalam catatan log.
- Gunakan nomor prioritas yang lebih tinggi untuk wilayah yang lebih kecil dan lebih spesifik sehingga memiliki prioritas yang lebih tinggi dibandingkan wilayah umum yang mencakup banyak wilayah.
- Jika Anda hanya menjual ke satu negara, Anda tidak perlu mengatur wilayah sama sekali — Spwig bekerja dengan baik dengan satu katalog global.
- Hanya atur **Ketersediaan Wilayah** produk Anda dari **Tersedia di semua wilayah** ketika Anda benar-benar perlu membatasiinya — defaultnya membuat produk tersedia secara universal tanpa perlu pemeliharaan.
- Tinjau aturan wilayah setiap produk setiap kali Anda menambahkan Wilayah Penjualan baru, sehingga pembatasan tetap sesuai dengan yang Anda inginkan.
- Tambahkan Pemilih Alamat Pengiriman ke bagian header Anda (lihat panduan **Ketersediaan Wilayah**) sehingga Anda dapat beralih ke wilayah lain dan memeriksa apakah produk yang dibatasi berjalan sesuai harapan.