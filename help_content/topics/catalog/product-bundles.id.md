---
title: Paket Produk
---

Paket produk memungkinkan Anda menjual paket produk yang telah dirangkai sebelumnya dengan harga bundling. Ini sempurna untuk set hadiah, kit pemula, atau kombinasi produk apa pun yang ingin Anda tawarkan bersama dengan diskon.

![Admin komponen paket](/static/core/admin/img/help/product-bundles/bundle-components.webp)

## Strategi Harga

Pilih cara harga paket dihitung:

| Strategi | Deskripsi |
|----------|-------------|
| **Harga Tetap** | Tetapkan satu harga flat untuk seluruh paket, tanpa memandang harga komponen. |
| **Diskon Persentase** | Hitung otomatis harga sebagai persentase dari harga komponen yang dikombinasikan. |
| **Jumlah Komponen** | Harga paket sama dengan total harga semua komponen (berguna untuk tampilan grup tanpa diskon). |

## Membuat Paket

### Langkah 1: Buat Produk

1. Navigasikan ke **Produk > Semua Produk** dan klik **+ Tambahkan Produk**
2. Setel **Jenis Produk** menjadi **Paket Produk**
3. Isi nama paket, deskripsi, dan gambar
4. Simpan produk

### Langkah 2: Tambahkan Komponen

Beralih ke tab **Item Paket** untuk menambahkan produk ke paket Anda:

1. Klik **+ Tambahkan Komponen**
2. Cari dan pilih produk dari dropdown
3. Tetapkan **Jumlah** untuk setiap komponen (misalnya, 2x masker wajah dalam set perawatan kulit)
4. Tetapkan **Urutan Penyortiran** untuk mengontrol urutan tampilan
5. Secara opsional, tandai komponen sebagai **Opsional** (pelanggan dapat mengecualikannya)
6. Jika komponen adalah produk variabel, pilih salah satu:
   - **Variasi tetap** — semua pelanggan mendapatkan variasi yang sama
   - **Izinkan pemilihan variasi** — pelanggan memilih variasi yang mereka sukai saat checkout

Ringkasan di bagian bawah menampilkan **Total Komponen** dan **Nilai Paket** (jumlah harga komponen).

### Langkah 3: Konfigurasi Harga

Beralih ke tab **Harga**:

1. Pilih **Strategi Harga Paket** Anda
2. Untuk **Harga Tetap** — masukkan harga paket secara langsung
3. Untuk **Diskon Persentase** — atur persentase diskon (misalnya, 15% diskon)
4. Untuk **Jumlah Komponen** — harga dihitung secara otomatis

## Apa yang Bisa Dibundling

| Jenis Produk | Bisa Menjadi Komponen? |
|-------------|-------------------|
| Produk Sederhana | Ya |
| Produk Variabel | Ya (variasi tetap atau pilihan pelanggan) |
| Produk Digital | Ya |
| Produk Kustom | Tidak |
| Produk Konfigurasi | Tidak |
| Paket Produk | Tidak (paket tidak bisa disusun bersama) |
| Kartu Hadiah | Tidak |

## Manajemen Stok

Stok paket dikelola melalui komponennya:

- **Semua komponen harus dalam stok** agar paket bisa dibeli
- Ketika paket dipesan, stok dikurangi dari setiap produk komponen secara individual
- Jika komponen apa pun habis stok, paket menjadi tidak tersedia
- Tingkat stok komponen diperiksa secara real time selama checkout

## Komponen Opsional

Tandai komponen sebagai **Opsional** untuk memungkinkan pelanggan mengkustomisasi paket mereka:

- Komponen opsional termasuk secara default tetapi dapat dihapus oleh pelanggan
- Harga paket menyesuaikan diri secara otomatis ketika komponen opsional dikecualikan
- Setidaknya satu komponen harus non-opsional (wajib)

## Pengalaman Pelanggan

Ketika pelanggan melihat paket di toko Anda:

1. **Daftar Komponen** — Semua produk yang termasuk ditampilkan dengan gambar dan jumlah
2. **Penghematan Paket** — Penghematan dibandingkan membeli item secara individual ditampilkan
3. **Pemilihan Variasi** — Untuk komponen dengan pemilihan variasi yang diaktifkan, pelanggan memilih opsi yang mereka sukai
4. **Item Opsional** — Pelanggan dapat mengaktifkan/mematikan komponen opsional
5. **Tambah ke Keranjang Tunggal** — Seluruh paket ditambahkan sebagai satu item

## Tips

- Gunakan strategi **Diskon Persentase** untuk harga paling fleksibel — menyesuaikan otomatis ketika harga komponen berubah.
- Tunjukkan jumlah penghematan secara terang di deskripsi produk untuk mendorong pembelian paket.
- Batasi paket hingga 3-5 komponen untuk pengalaman pelanggan terbaik. Terlalu banyak item bisa terasa membingungkan.
- Gunakan komponen opsional untuk menawarkan versi "dasar" dan "premium" dari paket yang sama.
- Periksa secara rutin bahwa semua produk komponen masih aktif dan dalam stok.
