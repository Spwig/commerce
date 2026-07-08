---
title: Mengelola Pesanan
---

# Mengelola Pesanan

Panduan ini mencakup segala sesuatu yang Anda butuhkan untuk mengelola pesanan pelanggan — dari meninjau pesanan baru hingga memproses pengiriman dan menangani pengembalian dana.

## Daftar Pesanan

Navigasikan ke **Pesanan > Semua Pesanan** di sidebar untuk melihat semua pesanan. Daftar ini menampilkan nomor, status, pelanggan, total, dan tanggal setiap pesanan.

![Daftar Pesanan](/static/core/admin/img/help/manage-orders/order-list.webp)

Gunakan filter di bagian atas untuk menyaring pesanan berdasarkan status, rentang tanggal, atau cari berdasarkan nomor pesanan atau nama pelanggan.

## Detail Pesanan

Klik pesanan apa pun untuk membuka halaman detailnya. Di sini Anda akan menemukan segala sesuatu tentang pesanan yang disusun dalam bagian jelas.

![Detail Pesanan](/static/core/admin/img/help/manage-orders/order-detail.webp)

### Informasi Pesanan

Bagian atas menampilkan:

- **Nomor Pesanan** — Pengidentifikasi unik untuk pesanan ini
- **Status** — Status pesanan saat ini (Menunggu, Diproses, Dikirim, Diterima, Selesai, Dibatalkan)
- **Pelanggan** — Nama dan email pelanggan yang memesan
- **Dibuat** — Kapan pesanan ditempatkan

### Item Pesanan

Bagian item menampilkan segala sesuatu yang dipesan oleh pelanggan:

- Nama produk dan SKU
- Jumlah yang dipesan
- Harga satuan dan total item
- Diskon yang diterapkan

### Detail Pembayaran

Menampilkan metode pembayaran yang digunakan, ID transaksi, dan status pembayaran. Untuk pesanan yang menunggu pembayaran, Anda dapat melacak status gateway pembayaran di sini.

### Alamat Pengiriman

Alamat pengiriman pelanggan. Jika alamat pembayaran berbeda, kedua alamat akan ditampilkan.

## Siklus Hidup Pesanan

Pesanan biasanya melewati status-status berikut:

1. **Menunggu** — Pesanan baru diterima, menunggu konfirmasi pembayaran
2. **Diproses** — Pembayaran dikonfirmasi, sedang dipersiapkan untuk pengiriman
3. **Dikirim** — Pesanan dikirim dengan informasi pelacakan
4. **Diterima** — Pelanggan menerima pesanan
5. **Selesai** — Pesanan selesai

## Memproses Pesanan

### 1. Periksa Pesanan

Pastikan:

- Item dan jumlahnya benar
- Alamat pengiriman lengkap
- Pembayaran telah diterima
- Catatan pelanggan telah ditangani

### 2. Buat Pengiriman

Untuk mengirim pesanan:

1. Klik **Buat Pengiriman** di halaman detail pesanan
2. Pilih item yang akan dimasukkan (untuk pengiriman parsial, pilih hanya beberapa item)
3. Pilih pengirim dan layanan pengiriman
4. Masukkan nomor pelacakan
5. Klik **Simpan Pengiriman**

Status pesanan secara otomatis diperbarui menjadi **Dikirim** dan pelanggan menerima email pemberitahuan pengiriman dengan informasi pelacakan.

### 3. Tandai sebagai Diterima

Setelah pelanggan mengonfirmasi pengiriman atau pelacakan menunjukkan status diterima, perbarui status menjadi **Diterima** dan kemudian **Selesai**.

## Aksi Pesanan

### Menambahkan Catatan

Tambahkan catatan internal atau pesan yang terlihat oleh pelanggan:

1. Gulir ke bagian **Catatan** di halaman detail pesanan
2. Ketik pesan Anda
3. Pilih apakah ini catatan internal (hanya staf) atau pemberitahuan pelanggan
4. Klik **Tambahkan Catatan**

Catatan yang terlihat oleh pelanggan memicu notifikasi email.

### Memproses Pengembalian Dana

Untuk mengeluarkan pengembalian dana:

1. Klik **Pengembalian Dana** di halaman detail pesanan
2. Pilih item yang akan dikembalikan (atau masukkan jumlah kustom)
3. Pilih alasan pengembalian dana
4. Konfirmasi pengembalian dana

Pengembalian dana diproses melalui gateway pembayaran asli. Pelanggan menerima konfirmasi email.

### Membatalkan Pesanan

Untuk membatalkan:

1. Klik **Batal Pesanan**
2. Pilih alasan pembatalan
3. Pilih apakah akan memperbarui stok item
4. Konfirmasi

Pelanggan diberitahu secara otomatis dan pengembalian dana dimulai jika pembayaran telah diterima.

## Aksi Massal

Dari daftar pesanan, Anda dapat memilih beberapa pesanan dan menerapkan aksi massal:

- **Perbarui Status** — Pindahkan beberapa pesanan ke status yang sama
- **Ekspor** — Unduh pesanan yang dipilih sebagai CSV
- **Cetak** — Buat surat pengiriman atau invoice

## Pemberitahuan Pesanan

Pelanggan secara otomatis menerima email pada tahap kunci:

- **Konfirmasi Pesanan** — Segera setelah memesan
- **Pembayaran Diterima** — Ketika pembayaran dikonfirmasi
- **Pemberitahuan Pengiriman** — Ketika pengiriman dibuat (termasuk tautan pelacakan)
- **Konfirmasi Pengiriman** — Ketika ditandai sebagai diterima

Konfigurasikan template email di **Pengaturan > Konfigurasi Email**.

## Tips

- Proses pesanan setiap hari untuk mempertahankan waktu pengiriman yang cepat.
- Gunakan filter status untuk fokus pada pesanan yang memerlukan perhatian (Menunggu dan Diproses).
- Tambahkan catatan internal untuk melacak persyaratan penanganan khusus.
- Untuk periode volume tinggi, gunakan aksi massal untuk memperbarui beberapa pesanan sekaligus.
- Atur aturan pengiriman untuk mengotomatisasi pemilihan pengirim berdasarkan berat dan destinasi pesanan.
