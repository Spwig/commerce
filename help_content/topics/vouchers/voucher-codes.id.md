---
title: Kode Voucher
---

Kode Voucher memungkinkan Anda membuat kode diskon, kupon, dan kartu hadiah yang dimasukkan oleh pelanggan saat checkout untuk mendapatkan diskon. Navigasikan ke **Marketing > Vouchers** di sidebar admin.

![Daftar voucher](/static/core/admin/img/help/voucher-codes/voucher-list.webp)

## Dashboard Voucher

Halaman voucher menampilkan ringkasan dengan:

- **Kartu Statistik** — Jumlah voucher Aktif, Tidak Aktif, Penggunaan, dan Total
- **Filter** — Cari berdasarkan kode atau nama, filter berdasarkan Tipe, Status, dan Ruang Lingkup
- **Kartu Voucher** — Setiap voucher ditampilkan dengan detail penggunaan dan status

## Membuat Voucher

1. Klik **+ Tambah Voucher** di pojok kanan atas
2. Isi detail voucher:
   - **Kode** — Kode yang dimasukkan oleh pelanggan saat checkout (contoh: "SAVE20", "FREESHIP")
   - **Nama/Deskripsi** — Deskripsi internal untuk referensi Anda
   - **Tipe Diskon** — Pilih cara diskon diterapkan
   - **Nilai Diskon** — Jumlah atau persentase diskon
3. Konfigurasikan aturan penggunaan:
   - **Batas Penggunaan** — Maksimal total penggunaan (0 = tidak terbatas)
   - **Batas per Pelanggan** — Maksimal penggunaan per pelanggan
   - **Nilai Pesanan Minimum** — Nilai total keranjang yang diperlukan
4. Tetapkan **ruang lingkup**:
   - **Seluruh Keranjang** — Diskon berlaku untuk seluruh pesanan
   - **Produk Tertentu** — Hanya berlaku untuk item yang dipilih
   - **Kategori Tertentu** — Hanya berlaku untuk item dalam kategori yang dipilih
5. Secara opsional tetapkan tanggal kedaluwarsa:
   - **Tanggal Kedaluwarsa** — Saat voucher berhenti berfungsi
6. Klik **Simpan**

## Jenis Voucher

| Tipe | Deskripsi | Contoh |
|------|-------------|---------|
| **Jumlah Tetap** | Mengurangi jumlah dolar tetap | $20 diskon dari pesanan |
| **Persentase** | Mengurangi persentase dari total | 15% diskon dari pesanan |
| **Pengiriman Gratis** | Menghilangkan biaya pengiriman | Pengiriman gratis untuk setiap pesanan |

## Mengelola Voucher

### Kartu Voucher

Setiap kartu voucher menampilkan:
- **Kode** — Kode voucher dalam teks tebal
- **Deskripsi** — Apa yang dilakukan voucher
- **Status badge** — Aktif atau Tidak Aktif
- **Detail Diskon** — Tipe dan nilai (contoh: "$ 20.00" atau "15.00%")
- **Ruang Lingkup** — Apakah berlaku untuk seluruh keranjang atau item tertentu
- **Jumlah Penggunaan** — Berapa kali voucher telah digunakan
- **Tanggal Dibuat** — Saat voucher dibuat
- **Kedaluwarsa** — Tanggal kedaluwarsa atau "Tidak ada kedaluwarsa"

### Aksi Voucher

Setiap kartu memiliki tombol aksi:
- **Edit** — Ubah pengaturan voucher
- **Lihat Riwayat** — Lihat riwayat penggunaan
- **Hapus** — Hapus voucher

### Memfilter Voucher

Gunakan bar filter untuk menemukan voucher tertentu:
- **Cari** — Cari berdasarkan kode, nama, atau deskripsi
- **Tipe** — Jumlah Tetap, Persentase, atau Pengiriman Gratis
- **Status** — Aktif atau Tidak Aktif
- **Ruang Lingkup** — Seluruh Keranjang atau item tertentu

## Pembuatan Voucher dalam Batch

Untuk kampanye besar, Anda dapat membuat voucher dalam batch:
1. Sistem secara otomatis menghasilkan kode unik (contoh: "COUPONX1600406498")
2. Tetapkan parameter umum untuk semua voucher yang dihasilkan
3. Sebarkan kode melalui email, media sosial, atau cetak

## Pengalaman Pelanggan

Ketika seorang pelanggan memiliki kode voucher:
1. Mereka melanjutkan ke **checkout**
2. Masukkan kode di bidang **kode diskon**
3. Diskon diterapkan segera jika voucher valid
4. Ringkasan pesanan diperbarui untuk menampilkan diskon

Jika voucher tidak valid (kedaluwarsa, batas penggunaan tercapai, nilai minimum tidak terpenuhi), pelanggan melihat pesan kesalahan yang jelas.

## Tips

- Gunakan kode yang mudah diingat untuk kampanye pemasaran (contoh: "SUMMER20" alih-alih string acak).
- Tetapkan batas per pelanggan untuk mencegah penyalahgunaan diskon bernilai tinggi.
- Gunakan nilai pesanan minimum untuk menjaga keuntungan (contoh: "$10 diskon untuk pesanan di atas $50").
- Pantau jumlah penggunaan di dashboard untuk melacak efektivitas kampanye.
- Buat voucher dengan batas waktu untuk menciptakan urgensi (contoh: "Hanya berlaku akhir pekan ini").
- Gunakan status Aktif/Tidak Aktif untuk menghentikan voucher tanpa menghapusnya.
