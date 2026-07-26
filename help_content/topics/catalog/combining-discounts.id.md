---
title: Menggabungkan Diskon
---

Platform menawarkan empat jenis diskon yang dapat bekerja bersama: penjualan produk, promosi, kode voucher, dan kartu hadiah. Memahami cara mereka berinteraksi membantu Anda menjalankan kampanye yang efektif tanpa hasil tak terduga atau diskon ganda yang tidak disengaja.

> **Kartu hadiah belum dapat diterapkan di checkout online saat ini.** Desain yang dijelaskan di bawah ini — kartu hadiah diterapkan terakhir, setelah semua diskon lain — adalah cara kerjanya saat fitur tersebut diluncurkan. Saat ini, kartu hadiah hanya dapat ditukarkan secara langsung di **Titik Penjualan**, sehingga interaksi yang dijelaskan untuk toko online belum berlaku untuk kartu hadiah secara khusus. Lihat topik bantuan **Kartu Hadiah** untuk melihat status saat ini.

## Empat Lapisan Diskon

Setiap jenis diskon beroperasi pada tingkat yang berbeda dan terlihat oleh pelanggan dengan cara yang berbeda.

| Lapisan | Di mana Diatur | Cara Diterapkan | Terlihat oleh Pelanggan |
|-------|---------------|-----------------|-------------------|
| **Penjualan Produk** | Formulir Edit Produk > Bagian Penjualan | Secara otomatis mengubah harga yang ditampilkan | Ya — ditampilkan sebagai harga asli yang dihapus |
| **Promosi** | Pemasaran > Penjualan & Promosi | Secara otomatis diterapkan pada produk yang cocok | Ya — ditampilkan sebagai harga diskon pada kartu produk |
| **Kode Voucher** | Pemasaran > Voucher | Pelanggan memasukkan kode di checkout | Hanya di checkout setelah memasukkan kode |
| **Kartu Hadiah** | Ditebus terhadap saldo kartu hadiah | Mengurangi total pembayaran | Hanya di Titik Penjualan untuk saat ini (lihat catatan di atas) |

## Cara Kerja Prioritas

Promosi memiliki bidang **Prioritas** yang menerima nilai 0 dan lebih tinggi. Angka yang lebih tinggi berarti prioritas yang lebih tinggi.

Ketika beberapa promosi cocok dengan produk yang sama, yang memiliki **prioritas tertinggi menang**. Mereka tidak berlapis — hanya satu promosi yang berlaku per produk.

**Contoh:** "Flash Sale 50% off" (prioritas 10) dan "Summer Sale 20% off" (prioritas 5) keduanya menargetkan semua produk. Pelanggan melihat harga diskon flash sale 50%, bukan 70% yang digabungkan.

Dalam tingkat prioritas yang sama, sistem memilih promosi yang memberikan diskon terbesar bagi pelanggan.

## Aturan Penggabungan

Tabel berikut menunjukkan kombinasi diskon mana yang diperbolehkan dan cara mengontrolnya.

| Kombinasi | Diperbolehkan? | Cara Mengontrolnya |
|-------------|----------|-------------------|
| Penjualan Produk + Promosi | Hanya jika diaktifkan | Centang **"Gabungkan dengan Penjualan Produk"** di Pengaturan Lanjutan promosi |
| Promosi + Promosi | Tidak — promosi dengan prioritas tertinggi menang | Tetapkan nilai Prioritas untuk mengontrol mana yang berlaku |
| Promosi + Kode Voucher | Ya | Diskon promosi mengurangi harga produk, voucher mengurangi total keranjang secara terpisah |
| Voucher + Voucher | Dapat dikonfigurasi | Flag **"Tidak dapat digabungkan dengan voucher lain"** pada voucher mengontrol ini (diaktifkan secara default) |
| Voucher + Item Diskon | Dapat dikonfigurasi | Flag **"Eksklusif item diskon"** pada voucher mengontrol ini |
| Kartu Hadiah + Diskon Apa Saja | Ya — selalu | Kartu hadiah diterapkan terakhir, mengurangi jumlah pembayaran akhir setelah semua diskon lain. Saat ini hanya mungkin di Titik Penjualan — lihat catatan di atas |

## Situasi Umum

### Situasi A: Promosi Sitewide + Kode Voucher

- **Pengaturan:** 20% off semua produk (promosi) + pelanggan memiliki voucher $10-off
- **Hasil:** Produk $100 menjadi $80 (promosi), kemudian voucher $10 diterapkan pada total keranjang. Pelanggan membayar **$70**.

### Situasi B: Produk yang sedang diskon + promosi sitewide

- **Pengaturan:** Produk memiliki diskon 30% pada tingkat produk + promosi sitewide 20% ada
- **Hasil (penggabungan dimatikan):** Hanya diskon produk yang berlaku. Pelanggan membayar **$70**.
- **Hasil (penggabungan diaktifkan):** Keduanya berlaku. Diskon 30% terlebih dahulu = $70, kemudian diskon 20% = **$56**.

### Situasi C: Dua promosi pada produk yang sama

- **Pengaturan:** "Flash Sale 40% off" (prioritas 10) + "Summer Sale 20% off" (prioritas 5), keduanya menargetkan semua produk
- **Hasil:** Flash Sale menang karena memiliki prioritas yang lebih tinggi. Pelanggan membayar **$60** pada produk $100.

### Situasi D: Voucher pada produk yang sedang diskon

- **Pengaturan:** Produk sedang diskon 25%.


Pelanggan memasukkan kode voucher 10% yang memiliki opsi "Eksklusi barang diskon" diaktifkan.
- **Hasil:** Voucher tidak berlaku untuk produk tersebut.

Jika keranjang memiliki barang non-diskon, voucher hanya berlaku untuk barang-barang tersebut.

## Jenis Diskon yang Harus Digunakan

| Tujuan | Pendekatan yang Direkomendasikan | Alasan |
|-------|-----------------------------|-------|
| Mendorong inventaris musiman | **Promosi** (target kategori atau koleksi) | Otomatis, tidak memerlukan tindakan pelanggan, terlihat pada kartu produk |
| Memberi hadiah kepada pelanggan tertentu | **Kode Voucher** (penggunaan tunggal, batas per pelanggan) | Terarah, dapat dilacak, terasa pribadi |
| Penawaran cepat untuk satu produk | **Penjualan Produk** (pada formulir edit produk) | Paling cepat untuk diatur, tidak memerlukan wizard promosi |
| Kredit toko atau hadiah | **Kartu Hadiah** | Berbasis saldo; saat ini hanya dapat ditukarkan di Point of Sale |
| Acara sitewide | **Promosi** (target semua produk) | Jangkauan maksimal, satu pengaturan mencakup semuanya |
| Kampanye kembali pelanggan | **Kode Voucher** (batasan pelanggan baru atau kembali) | Dapat menargetkan segmen pelanggan tertentu |

## Tips

- **Uji dengan keranjang nyata** — setelah mengatur promosi dan voucher, tambahkan produk ke keranjang dan lalui proses checkout untuk memverifikasi diskon berlaku sesuai harapan.
- **Periksa jumlah "produk yang terkena dampak"** — pada langkah tinjau promosi, pastikan jumlah produk yang terkena dampak sesuai dengan niat Anda.
- **Gunakan prioritas secara sengaja** — jika Anda menjalankan beberapa promosi secara bersamaan, selalu tetapkan nilai prioritas yang berbeda agar Anda mengontrol mana yang menang.
- **Nonaktifkan penumpukan secara default** — hanya aktifkan "Gabungkan dengan Penjualan Produk" ketika Anda secara spesifik ingin diskon ganda.
- **Dokumentasikan strategi Anda** — gunakan bidang deskripsi promosi untuk mencatat alasan promosi tersebut ada dan bagaimana hubungannya dengan promosi aktif lainnya.