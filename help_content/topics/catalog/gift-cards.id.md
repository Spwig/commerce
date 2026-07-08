---
title: Kartu Hadiah
---

Kartu hadiah memungkinkan pelanggan Anda membeli kredit toko yang dapat dikirimkan kepada seseorang sebagai hadiah atau disimpan untuk penggunaan pribadi. Penerima menerima kode unik melalui email yang dapat mereka tukarkan saat checkout.

![Manajemen kartu hadiah](/static/core/admin/img/help/gift-cards/gift-card-list.webp)

## Jenis Nama Nilai

Kontrol cara pelanggan memilih jumlah kartu hadiah:

| Jenis | Deskripsi |
|------|-------------|
| **Nama Nilai Tetap** | Pelanggan memilih dari jumlah yang telah ditetapkan (misalnya, $25, $50, $100) |
| **Jumlah Kustom** | Pelanggan memasukkan jumlah apa pun dalam rentang minimum/maksimum |
| **Keduanya** | Tawarkan nama nilai yang telah ditetapkan ditambah opsi jumlah kustom |

## Membuat Produk Kartu Hadiah

### Langkah 1: Siapkan Produk

1. Navigasi ke **Produk > Semua Produk** dan klik **+ Tambah Produk**
2. Setel **Jenis Produk** menjadi **Kartu Hadiah**
3. Isi nama produk dan deskripsi
4. Konfigurasikan pengaturan nama nilai:
   - Pilih **Jenis Nama Nilai** (Tetap, Kustom, atau Keduanya)
   - Untuk Tetap: atur jumlah nama nilai yang tersedia
   - Untuk Kustom: atur **Minimum** dan **Maksimum** jumlah yang diperbolehkan
5. Setel **Hari Kadaluarsa** (0 = tidak pernah kadaluarsa) — ini menentukan seberapa lama kartu hadiah tetap valid setelah dibeli
6. Simpan dan publikasikan produk

### Langkah 2: Publikasikan dan Jual

Setelah diterbitkan, kartu hadiah muncul di toko online Anda seperti produk lainnya. Pelanggan dapat menjelajahi produk ini, memilih jumlah, dan menambahkannya ke keranjang belanja.

## Siklus Hidup Kartu Hadiah

Sebuah kartu hadiah mengikuti siklus hidup ini:

1. **Pembelian** — Pelanggan membeli produk kartu hadiah dan memberikan detail penerima
2. **Pengiriman** — Email dengan kode kartu hadiah dikirimkan ke penerima secara otomatis
3. **Penukaran** — Penerima memasukkan kode saat checkout untuk menerapkan saldo
4. **Pelacakan Saldo** — Setiap penggunaan mengurangi saldo hingga mencapai nol

## Alur Pembelian Pelanggan

Ketika seorang pelanggan membeli kartu hadiah:

1. **Pilih Jumlah** — Pilih nama nilai atau masukkan jumlah kustom
2. **Detail Penerima** — Masukkan alamat email dan nama penerima
3. **Pesan Pribadi** — Tambahkan pesan opsional untuk disertakan dalam email pengiriman
4. **Nama Pengirim** — Sediakan nama pengirim untuk email
5. **Pengiriman Terjadwal** — Secara opsional jadwalkan email untuk tanggal di masa depan (misalnya, ulang tahun)
6. **Checkout** — Selesaikan pembelian seperti produk lainnya

## Pengiriman Otomatis

Setelah pembelian, kartu hadiah dikirimkan secara otomatis:

- Email yang dirancang dikirim ke penerima dengan:
  - Kode kartu hadiah unik
  - Nilai kartu hadiah
  - Pesan pribadi dari pengirim
  - Tautan untuk memeriksa sisa saldo
- Jika pengiriman terjadwal telah diatur, email dikirim pada tanggal dan waktu yang ditentukan
- Pengirim menerima konfirmasi pesanan dengan detail kartu hadiah

## Mengelola Kartu Hadiah di Admin

Navigasi ke **Produk > Kartu Hadiah** untuk mengelola semua kartu hadiah:

### Dashboard Statistik

Di bagian atas halaman, empat kartu menampilkan metrik kunci:

- **Total Kartu Hadiah** — Jumlah total kartu hadiah yang diterbitkan
- **Aktif** — Kartu yang saat ini aktif dengan saldo yang tersedia
- **Total Saldo** — Saldo tersisa yang dikombinasikan dari semua kartu
- **Dibeli Sebagian** — Kartu yang telah ditukarkan sebagian

### Filter

Saring kartu hadiah berdasarkan:

- **Cari** — Cari berdasarkan kode, email, atau nama penerima
- **Status** — Aktif, Tidak Aktif, Kadaluarsa, Terverifikasi Penuh, atau Dibeli Sebagian
- **Saldo** — Memiliki Saldo atau Saldo Nol
- **Dibuat** — Periode waktu (Hari Ini, Minggu Ini, Bulan Ini, Tahun Ini)

### Detail Kartu Hadiah

Setiap kartu hadiah menampilkan:

- **Kode** — Kode penukaran unik (misalnya, GC-XXXX-XXXX-XXXX)
- **Penerima** — Email dan nama
- **Status badge** — Status saat ini dengan kode warna
- **Saldo / Awal / Dibeli** — Ringkasan keuangan dengan persentase yang digunakan
- **Tanggal penting** — Dibuat, diterbitkan, digunakan pertama kali
- **Pengirim** — Siapa yang membeli kartu hadiah

### Tindakan

Untuk setiap kartu hadiah, Anda dapat:

- **Edit** — Lihat dan ubah detail kartu hadiah
- **Lihat Transaksi** — Lihat riwayat transaksi lengkap
- **Kirim Ulang Email** — Kirim ulang email pengiriman ke penerima
- **Nonaktifkan** — Nonaktifkan kartu (saldo tetap dijaga tetapi tidak dapat digunakan)

## Penukaran di Checkout

Ketika seorang pelanggan memasukkan kode kartu hadiah di checkout:

1. Kode divalidasi (aktif, tidak kadaluarsa, memiliki saldo)
2. Saldo yang tersedia ditampilkan
3. Saldo diterapkan ke total pesanan
4. Jika saldo menutupi pesanan secara penuh, tidak diperlukan pembayaran tambahan
5. Jika saldo kurang dari total pesanan, pelanggan membayar sisa pembayaran
6. Transaksi dicatat dan saldo diperbarui

## Penanganan Pengembalian Dana

Ketika mengembalikan pesanan yang menggunakan kartu hadiah:

- **Kartu hadiah yang belum digunakan** — Nonaktifkan kartu hadiah secara keseluruhan
- **Kartu yang digunakan sebagian** — Saldo harus disesuaikan secara manual melalui transaksi
- **Pengembalian penuh** — Kreditkan jumlah kembali ke saldo kartu hadiah melalui transaksi pengembalian dana

## Tips

- Tetapkan periode kedaluarsa yang masuk akal (misalnya, 365 hari) untuk mematuhi regulasi kartu hadiah lokal — beberapa yurisdiksi memerlukan periode validitas minimum.
- Gunakan jenis denominasi **Keduanya** untuk menawarkan kenyamanan (jumlah yang ditetapkan) dan fleksibilitas (jumlah kustom).
- Pantau secara teratur metrik **Total Saldo** — ini mewakili kewajiban yang belum terpenuhi di buku Anda.
- Gunakan pengiriman terjadwal untuk promosi musiman — pelanggan dapat membeli kartu hadiah lebih awal dan memiliki mereka dikirimkan pada tanggal yang tepat.
- Uji alur penuh (pembelian, pengiriman email, penukaran) dengan pesanan uji sebelum diluncurkan.
- Jika Anda menjual ke pelanggan di beberapa negara, Anda dapat menerbitkan kartu hadiah dalam mata uang tertentu — lihat topik bantuan **Kartu Hadiah Multi-Mata Uang** untuk detail.