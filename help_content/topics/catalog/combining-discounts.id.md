---
title: Menggabungkan Diskon
---

Platform menawarkan empat jenis diskon yang dapat bekerja bersama: penjualan produk, promosi, kode voucher, dan kartu hadiah. Memahami cara mereka berinteraksi membantu Anda menjalankan kampanye yang efektif tanpa hasil tak terduga atau diskon ganda yang tidak disengaja.

## Empat Lapisan Diskon

Setiap jenis diskon beroperasi pada tingkat yang berbeda dan terlihat oleh pelanggan dengan cara yang berbeda.

| Lapisan | Diatur Di | Cara Penerapan | Terlihat oleh Pelanggan |
|-------|---------------|-----------------|-------------------|
| **Penjualan Produk** | Formulir Edit Produk > Bagian Penjualan | Secara otomatis mengubah harga yang ditampilkan | Ya — ditampilkan sebagai harga asli yang dihapus |
| **Promosi** | Pemasaran > Penjualan & Promosi | Secara otomatis diterapkan pada produk yang cocok | Ya — ditampilkan sebagai harga diskon pada kartu produk |
| **Kode Voucher** | Pemasaran > Voucher | Pelanggan memasukkan kode saat checkout | Hanya saat checkout setelah memasukkan kode |
| **Kartu Hadiah** | Diterapkan saat checkout dari saldo kartu hadiah | Mengurangi total pembayaran | Hanya saat checkout |

## Bagaimana Prioritas Bekerja

Promosi memiliki bidang **Prioritas** yang menerima nilai 0 dan lebih tinggi. Angka yang lebih tinggi berarti prioritas yang lebih tinggi.

Ketika beberapa promosi cocok dengan produk yang sama, yang memiliki **prioritas tertinggi menang**. Mereka tidak menumpuk — hanya satu promosi yang berlaku per produk.

**Contoh:** "Flash Sale 50% off" (prioritas 10) dan "Summer Sale 20% off" (prioritas 5) keduanya menargetkan semua produk. Pelanggan melihat harga diskon flash sale 50%, bukan 70% yang digabungkan.

Dalam tingkat prioritas yang sama, sistem memilih promosi yang memberikan diskon terbesar kepada pelanggan.

## Aturan Penumpukan

Tabel berikut menunjukkan kombinasi diskon mana yang diperbolehkan dan cara mengontrolnya.

| Kombinasi | Diperbolehkan? | Cara Mengontrolnya |
|-------------|----------|-------------------|
| Penjualan Produk + Promosi | Hanya jika diaktifkan | Centang **"Dapat dikombinasikan dengan penjualan produk"** di Pengaturan Lanjutan promosi |
| Promosi + Promosi | Tidak — prioritas tertinggi menang | Tetapkan nilai Prioritas untuk mengontrol mana yang berlaku |
| Promosi + Kode Voucher | Ya | Diskon promosi mengurangi harga produk, voucher mengurangi total keranjang secara terpisah |
| Voucher + Voucher | Dapat dikonfigurasi | Flag **"Tidak dapat dikombinasikan dengan voucher lain"** pada voucher mengontrol ini (diaktifkan secara default) |
| Voucher + Item Penjualan | Dapat dikonfigurasi | Flag **"Eksklusif item penjualan"** pada voucher mengontrol ini |
| Kartu Hadiah + Diskon Apa Saja | Ya — selalu | Kartu hadiah diterapkan terakhir, mengurangi jumlah pembayaran akhir setelah semua diskon lain diterapkan |

## Situasi Umum

### Situasi A: Promosi sitewide + kode voucher

- **Pengaturan:** 20% off semua produk (promosi) + pelanggan memiliki voucher $10-off
- **Hasil:** Produk $100 menjadi $80 (promosi), kemudian voucher $10 diterapkan pada total keranjang. Pelanggan membayar **$70**.

### Situasi B: Produk yang sedang dijual + promosi sitewide

- **Pengaturan:** Produk memiliki diskon tingkat produk 30% + promosi sitewide 20% ada
- **Hasil (penumpukan dinonaktifkan):** Hanya diskon produk yang berlaku. Pelanggan membayar **$70**.
- **Hasil (penumpukan diaktifkan):** Keduanya berlaku. Diskon 30% terlebih dahulu = $70, kemudian diskon 20% = **$56**.

### Situasi C: Dua promosi pada produk yang sama

- **Pengaturan:** "Flash Sale 40% off" (prioritas 10) + "Summer Sale 20% off" (prioritas 5), keduanya menargetkan semua produk
- **Hasil:** Flash Sale menang karena memiliki prioritas yang lebih tinggi. Pelanggan membayar **$60** pada produk $100.

### Situasi D: Voucher pada item yang sedang dijual

- **Pengaturan:** Produk sedang dijual dengan diskon 25%. Pelanggan memasukkan kode voucher 10% yang memiliki flag "Eksklusif item penjualan" yang diaktifkan.
- **Hasil:** Voucher tidak berlaku untuk produk tersebut. Jika keranjang memiliki item yang tidak sedang dijual, voucher hanya berlaku untuk item tersebut.

## Jenis Diskon yang Harus Digunakan

| Tujuan | Pendekatan yang Direkomendasikan | Kenapa |
|------|---------------------|-----|
| Mendorong inventaris musiman | **Promosi** (penargetan kategori atau koleksi) | Otomatis, tidak memerlukan tindakan pelanggan, terlihat pada kartu produk |
| Memberi hadiah kepada pelanggan tertentu | **Kode Voucher** (penggunaan tunggal, batas per pelanggan) | Dapat ditargetkan, dapat dilacak, terasa pribadi |
| Penawaran cepat untuk satu produk | **Penjualan Produk** (pada formulir edit produk) | Paling cepat untuk diatur, tidak memerlukan wizard promosi |
| Kredit toko atau hadiah | **Kartu Hadiah** | Berbasis saldo, pelanggan mengelola kredit mereka sendiri |
| Acara sitewide | **Promosi** (penargetan semua produk) | Jangkauan maksimal, satu pengaturan mencakup semuanya |
| Kampanye memperoleh kembali pelanggan | **Kode Voucher** (batasan pelanggan baru atau kembali) | Dapat menargetkan segmen pelanggan tertentu |

## Tips

- **Uji dengan keranjang nyata** — setelah mengatur promosi dan voucher, tambahkan produk ke keranjang dan lalui checkout untuk memverifikasi diskon berlaku seperti yang diharapkan.
- **Periksa jumlah "produk yang terdampak"** — pada langkah tinjau promosi, verifikasi jumlah produk yang terdampak sesuai dengan niat Anda.
- **Gunakan prioritas secara sengaja** — jika Anda menjalankan beberapa promosi secara bersamaan, selalu atur nilai prioritas yang berbeda agar Anda mengontrol mana yang menang.
- **Nonaktifkan penumpukan secara default** — hanya aktifkan "Dapat dikombinasikan dengan penjualan produk" ketika Anda secara khusus ingin diskon ganda.
- **Dokumentasikan strategi Anda** — gunakan bidang deskripsi promosi untuk mencatat alasan promosi tersebut ada dan bagaimana terkait dengan promosi aktif lainnya.