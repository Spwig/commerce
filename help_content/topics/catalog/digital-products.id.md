---
title: Produk Digital
---

Produk digital memungkinkan Anda menjual file yang dapat diunduh, lisensi perangkat lunak, dan barang non-fisik lainnya. Spwig mendukung produk digital mandiri, serta produk hybrid yang menggabungkan pengiriman fisik dan digital.

![Pemberi lisensi](/static/core/admin/img/help/digital-products/license-providers.webp)

## Jenis Produk Digital

### Produk Digital Mandiri

Atur **Jenis Produk** ke **Produk Digital** untuk item yang sepenuhnya digital:
- Aplikasi perangkat lunak
- Buku elektronik dan PDF
- Musik dan file audio
- Karya seni digital dan template

### Produk Hybrid

Jenis produk apa pun dapat mencakup pengiriman digital dengan menandai **Adalah Produk Digital** di tab Info Dasar. Ini berguna untuk:
- **Produk digital bervariasi** — Perangkat lunak dengan edisi Basic/Pro/Enterprise
- **Produk digital yang dapat dikustomisasi** — Aset digital yang dirancang khusus
- **Bundel fisik + digital** — Buku yang mencakup unduhan digital

## Menyiapkan Produk Digital

### Langkah 1: Membuat Produk

1. Beralih ke **Produk > Semua Produk** dan klik **+ Tambah Produk**
2. Atur **Jenis Produk** ke **Produk Digital** (atau tanda **Adalah Produk Digital** pada jenis produk lain)
3. Isi detail produk (nama, deskripsi, harga)
4. Simpan produk

### Langkah 2: Menambahkan File Unduhan

1. Beralih ke tab **Stok** produk
2. Di bagian **File Digital**, unggah file yang akan diterima pelanggan setelah pembelian
3. Untuk setiap file, Anda dapat mengatur:
   - **Nama file** — Nama tampilan yang ditampilkan kepada pelanggan
   - **Batas unduhan** — Jumlah maksimum kali file dapat diunduh (0 = tak terbatas)
   - **Hari kedaluwarsa** — Jumlah hari tautan unduh tetap aktif

### Langkah 3: Mengatur Pengiriman Lisensi (Opsional)

Jika produk digital Anda memerlukan kunci lisensi:

1. Beralih ke **Pengaturan > Manajemen Lisensi**
2. Hubungkan pemberi lisensi (lihat di bawah)
3. Di formulir edit produk, tetapkan pemberi lisensi

## Pemberi Lisensi

Pemberi lisensi adalah layanan eksternal yang secara otomatis menghasilkan dan mengelola kunci lisensi perangkat lunak saat pelanggan membeli produk Anda.

### Jenis Pemberi Lisensi yang Tersedia

| Pemberi Lisensi | Deskripsi |
|------------------|------------|
| **Spwig Built-in License Server** | Pembuatan kunci lisensi sederhana yang terintegrasi ke dalam platform |
| **Keygen.sh** | API manajemen lisensi lengkap |
| **LicenseSpring** | Manajemen lisensi enterprise |
| **Cryptlex** | Lisensi perangkat lunak dengan dukungan offline |
| **Custom API** | Hubungkan sistem lisensi apa pun melalui REST API |

### Menghubungkan Pemberi Lisensi

1. Beralih ke **Pengaturan > Manajemen Lisensi**
2. Klik **Hubungkan Pemberi Lisensi**
3. Ikuti wizard pengaturan:
   - **Langkah 1** — Pilih jenis pemberi lisensi
   - **Langkah 2** — Konfigurasi pengaturan umum
   - **Langkah 3** — Masukkan kredensial API
4. Uji koneksi untuk memverifikasi apakah berfungsi
5. Simpan konfigurasi

### Kartu Pemberi Lisensi

Setiap pemberi lisensi yang terhubung menampilkan:
- **Lencana Status** — Aktif/Nonaktif dan status koneksi
- **Titik Akhir API** — URL server yang dikonfigurasi
- **Kemampuan Sinkronisasi** — Dukungan sinkronisasi Pesanan, Aktivasi, dan Deaktivasi
- **Tombol Aksi** — Konfigurasi, Uji, dan Sinkronisasi Sekarang

### Kemampuan Sinkronisasi

Pemberi lisensi dapat sinkronisasi pada tiga kejadian:

- **Pesanan** — Secara otomatis menghasilkan kunci lisensi saat pelanggan menyelesaikan pembelian
- **Aktivasi** — Lacak saat pelanggan mengaktifkan lisensinya
- **Deaktivasi** — Handle deaktivasi lisensi untuk pengembalian atau transfer

## Pengalaman Pelanggan

### Setelah Pembelian

Ketika pelanggan membeli produk digital:

1. **Konfirmasi Pesanan** — Menunjukkan bahwa pengiriman digital termasuk
2. **Pengiriman Email** — Tautan unduh dan/atau kunci lisensi dikirim secara otomatis
3. **Halaman Akun** — Pelanggan dapat mengakses unduhan mereka dari dashboard akun
4. **Halaman Unduh** — Tautan unduh yang aman dengan batas waktu

### Keamanan Unduh

Unduhan file digital dilindungi oleh:
- Token unduh unik dengan batas waktu
- Batas jumlah unduh opsional
- Tanggal kedaluwarsa setelah itu tautan menjadi tidak aktif
- Persyaratan login (untuk pelanggan yang terdaftar)

## Tips

- Tetapkan batas unduh yang wajar (3-5 unduhan) untuk mencegah penyalahgunaan sambil memungkinkan unduhan ulang.
- Gunakan hari kedaluwarsa yang sesuai dengan periode dukungan Anda (misalnya, 365 hari untuk akses satu tahun).
- Uji alur pembelian penuh dengan pesanan uji untuk memastikan tautan unduh dan kunci lisensi dikirim dengan benar.
- Untuk produk perangkat lunak, hubungkan pemberi lisensi untuk mengotomatisasi pembuatan kunci daripada mengelola kunci secara manual.
- Gunakan fitur produk hybrid saat menjual barang fisik yang mencakup ekstra digital (misalnya, buku cetak + PDF).
