---
title: Contoh Voucher
---

Panduan ini memberikan contoh konkret, berdasarkan bidang demi bidang, untuk jenis voucher yang paling umum. Setiap contoh menunjukkan tepat apa yang harus dimasukkan saat membuat voucher di **Pemasaran > Voucher** → **+ Tambahkan Voucher**.

![Kartu Voucher](/static/core/admin/img/help/voucher-examples/voucher-card.webp)

## Contoh 1: Persentase Potongan dengan Batas Potongan

**Skenario:** Tawarkan potongan 20% untuk seluruh keranjang, tetapi batasi potongan maksimal hingga $50 agar pesanan bernilai tinggi tetap menguntungkan. Tidak ada tanggal kedaluwarsa.

| Bidang | Nilai |
|-------|-------|
| Kode | `SAVE20` |
| Nama | 20% Potongan — Maks $50 |
| Jenis Potongan | Persentase |
| Nilai Potongan | 20 |
| Jumlah Potongan Maksimal | 50 |
| Cakupan Penerapan | Seluruh Keranjang |
| Jumlah Penggunaan Total Maksimal | *(kosong — tidak terbatas)* |
| Jumlah Penggunaan per Pelanggan | 1 |
| Nilai Pesanan Minimum | *(kosong — tidak ada minimum)* |

**Bagaimana batas bekerja:** Pada pesanan $200, potongan adalah $40. Pada pesanan $300, potongan akan menjadi $60, tetapi batas membatasinya hingga $50. Pada pesanan $500, potongan tetap $50. Ini memungkinkan Anda menjalankan promosi yang terdengar murah tetapi tetap menjaga potongan sebenarnya dapat diprediksi.

## Contoh 2: Potongan Jumlah Tetap dengan Minimum

**Skenario:** Berikan potongan $10 untuk setiap pesanan di atas $75 untuk mendorong keranjang yang lebih besar.

| Bidang | Nilai |
|-------|-------|
| Kode | `TAKE10` |
| Nama | $10 Potongan untuk Pesanan di Atas $75 |
| Jenis Potongan | Jumlah Tetap |
| Nilai Potongan | 10 |
| Cakupan Penerapan | Seluruh Keranjang |
| Nilai Pesanan Minimum | 75 |
| Jumlah Penggunaan per Pelanggan Maksimal | 0 *(tidak terbatas)* |
| Tanggal Berakhir | *(kosong — tidak ada kedaluwarsa)* |

> **Catatan:** Menetapkan nilai pesanan minimum melindungi margin keuntungan Anda. Tanpa itu, seorang pelanggan bisa menggunakan kode ini pada pesanan $12 dan menghilangkan keuntungan Anda. Selalu pasangkan voucher jumlah tetap dengan nilai minimum yang masuk akal.

## Contoh 3: Voucher Pengiriman Gratis

**Skenario:** Tawarkan pengiriman gratis untuk setiap pesanan tanpa nilai minimum.

| Bidang | Nilai |
|-------|-------|
| Kode | `FREESHIP` |
| Nama | Pengiriman Gratis |
| Jenis Potongan | Pengiriman Gratis |
| Cakupan Penerapan | Seluruh Keranjang |
| Jumlah Penggunaan Total Maksimal | *(kosong — tidak terbatas)* |
| Jumlah Penggunaan per Pelanggan | 1 |
| Nilai Pesanan Minimum | *(kosong — tidak ada minimum)* |

> **Catatan:** Pilih jenis potongan **Pengiriman Gratis**, yang secara otomatis menghilangkan biaya pengiriman dari pesanan. Ini adalah pendekatan terbersih dan berfungsi terlepas dari metode pengiriman yang dipilih pelanggan.

## Contoh 4: Kode Selamat Datang untuk Pelanggan Baru

**Skenario:** Berikan potongan 15% untuk pesanan pertama pelanggan baru untuk mendorong konversi.

| Bidang | Nilai |
|-------|-------|
| Kode | `WELCOME15` |
| Nama | Selamat Datang — 15% Potongan untuk Pesanan Pertama |
| Jenis Potongan | Persentase |
| Nilai Potongan | 15 |
| Cakupan Penerapan | Seluruh Keranjang |
| Jumlah Penggunaan per Pelanggan Maksimal | 1 |
| Hanya untuk Pelanggan Baru | Dicentang |

Sistem memverifikasi status pelanggan baru dengan memeriksa apakah pelanggan memiliki pesanan sebelumnya yang selesai. Jika seorang pelanggan dengan riwayat pesanan mencoba menerapkan kode ini, mereka akan melihat pesan kesalahan yang jelas saat checkout.

## Contoh 5: Voucher untuk Produk Tertentu

**Skenario:** Tawarkan potongan $5 untuk produk tertentu — misalnya, untuk mempercepat penjualan produk yang lamban.

| Bidang | Nilai |
|-------|-------|
| Kode | `PICK5` |
| Nama | $5 Potongan untuk Item Terpilih |
| Jenis Potongan | Jumlah Tetap |
| Nilai Potongan | 5 |
| Cakupan Penerapan | Produk Tertentu |
| Produk yang Layak | *(pilih produk target)* |
| Jumlah Penggunaan per Pelanggan Maksimal | 1 |

> **Catatan:** Gunakan cakupan produk ketika Anda ingin memberikan diskon untuk SKU individu. Gunakan cakupan kategori (contoh berikutnya) ketika Anda ingin memberikan diskon untuk semua produk dalam sebuah departemen. Cakupan produk memberi Anda kontrol yang presisi; cakupan kategori lebih mudah dipelihara ketika katalog Anda sering berubah.

## Contoh 6: Voucher Kategori

**Skenario:** Jalankan promosi potongan 25% untuk semua item dalam kategori Elektronik.

| Bidang | Nilai |
|-------|-------|
| Kode | `ELEC25` |
| Nama | 25% Potongan untuk Elektronik |
| Jenis Potongan | Persentase |
| Nilai Potongan | 25 |
| Cakupan Penerapan | Kategori Tertentu |
| Kategori yang Layak | Elektronik |
| Jumlah Penggunaan Total Maksimal | *(kosong — tidak terbatas)* |
| Jumlah Penggunaan per Pelanggan | 1 |


Ketika dibatasi pada kategori, diskon hanya berlaku untuk barang yang memenuhi syarat di keranjang.

Item non-Elektronik dikenakan harga penuh.

## Perbandingan Jenis Diskon

| Jenis | Cara Kerja | Terbaik Untuk | Contoh |
|------|-------------|----------|---------|
| **Persentase** | Mengurangi persentase dari total yang memenuhi syarat | Diskon yang berkembang seiring dengan ukuran pesanan | 20% potongan untuk seluruh keranjang |
| **Jumlah Tetap** | Mengurangi jumlah dolar tetap | Promosi sederhana dan dapat diprediksi | $10 potongan untuk pesanan di atas $75 |
| **Pengiriman Gratis** | Menghilangkan biaya pengiriman dari pesanan | Mengurangi peninggalkan keranjang saat checkout | Pengiriman gratis, tanpa batas minimum |

## Perbandingan Cakupan

| Cakupan | Cara Kerja | Terbaik Untuk |
|-------|-------------|----------|
| **Seluruh Keranjang** | Diskon berlaku untuk total pesanan penuh | Promosi seluruh toko dan kode selamat datang |
| **Produk Tertentu** | Diskon hanya berlaku untuk produk yang dipilih di keranjang | Membersihkan inventaris tertentu atau penawaran terpilih |
| **Kategori Tertentu** | Diskon hanya berlaku untuk barang dalam kategori yang dipilih | Penjualan per departemen dan promosi musiman |

## Tips

- **Gunakan kode yang mudah diingat** — `SUMMER20` lebih mudah diingat daripada `COUPONX1600406498`. Simpan kode yang dihasilkan secara otomatis untuk kampanye dalam jumlah besar.
- **Uji sebelum menyebar** — Buat pesanan uji dengan kode voucher untuk memverifikasi bahwa kode berlaku dengan benar dan menghormati semua batasan.
- **Pantau penggunaan** — Periksa jumlah Redemptions di setiap kartu voucher untuk melacak kinerja kampanye secara real time.
- **Gabungkan dengan bar pengumuman** — Promosikan kode voucher Anda dalam pengumuman situs sehingga pelanggan melihatnya sebelum memulai berbelanja.