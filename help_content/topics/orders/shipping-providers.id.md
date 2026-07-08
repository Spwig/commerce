---
title: Pengirim Barang
---

Pengirim barang menghubungkan toko Anda ke API penyedia pengiriman untuk tarif pengiriman langsung, pembuatan label, dan pelacakan paket. Spwig mendukung penyedia pengiriman utama di seluruh dunia dan juga memungkinkan Anda membuat tabel tarif manual untuk penyedia tanpa integrasi API.

![Pengirim barang](/static/core/admin/img/help/shipping-providers/provider-list.webp)

## Pengirim yang Tersedia

| Pengirim | Wilayah | Fitur Utama |
|---------|---------|-------------|
| **FedEx** | Global | Tarif langsung, cetak label, pelacakan, multi-paket |
| **UPS** | Global | Tarif langsung, cetak label, pelacakan, validasi alamat |
| **USPS** | Amerika Serikat | Tarif domestik dan internasional, pelacakan |
| **NinjaVan** | Asia Tenggara | Pengiriman last-mile, dukungan bayar di tempat |
| **Canada Post** | Kanada | Domestik dan internasional, tarif paket dan surat |
| **Australia Post** | Australia | Domestik dan internasional, paket dan ekspres |

## Menghubungkan Pengirim

Buka **Pengaturan > Pengirim Barang** dan klik **Koneksi Pengirim** untuk memulai wizard pengaturan.

### Langkah 1: Pilih Pengirim

Pilih dari pengirim pengiriman yang tersedia. Setiap kartu menampilkan wilayah yang didukung dan fitur pengirim.

### Langkah 2: Petunjuk Pengaturan

Lihat panduan pengaturan khusus pengirim:
- Cara membuat akun pengembang/perusahaan dengan pengirim
- Di mana menemukan kredensial API Anda
- Pengaturan akun yang diperlukan (misalnya, nomor pengirim, nomor meter)

### Langkah 3: Masukkan Kredensial

Masukkan kredensial API untuk akun pengirim Anda. Bidang yang diperlukan bervariasi tergantung pengirim:

- **API Key / Secret** — Kredensial otentikasi
- **Nomor Akun** — Nomor akun pengirim atau pengirim Anda
- **Nomor Meter** — Diperlukan oleh beberapa pengirim (misalnya, FedEx)
- **Mode Sandbox** — Aktifkan untuk menguji dengan API sandbox pengirim sebelum go live

### Langkah 4: Uji Koneksi

Klik **Uji Koneksi** untuk memverifikasi kredensial Anda. Wizard memastikan:
- Otentikasi API berhasil
- Izin akun valid
- Kueri tarif mengembalikan hasil yang diharapkan

### Langkah 5: Konfigurasi dan Simpan

Selesaikan pengaturan:
- **Aktif** — Aktifkan atau nonaktifkan pengirim
- **Nama Tampilan** — Nama yang ditampilkan kepada pelanggan saat checkout
- **Alamat Asal** — Alamat gudang atau pemenuhan pesanan untuk perhitungan tarif

## Zona Pengiriman

Zona pengiriman mendefinisikan area geografis untuk perhitungan tarif. Buka **Pengaturan > Zona Pengiriman** untuk mengelolanya.

### Membuat Zona

1. Klik **+ Tambah Zona**
2. Beri nama zona (misalnya, "Domestik", "Eropa", "Asia Pasifik")
3. Definisikan cakupan zona menggunakan satu atau lebih:
   - **Negara** — Pilih negara spesifik
   - **Negara Bagian/Provinsi** — Sempitkan ke wilayah spesifik dalam sebuah negara
   - **Polanya Kode Pos** — Cocokkan kode pos/ZIP menggunakan pola (misalnya, "90*" untuk area Los Angeles)
4. Atur **Prioritas** — Saat zona tumpang tindih, zona dengan prioritas tertinggi digunakan

### Cocokkan Zona

Ketika pelanggan memasukkan alamat pengiriman mereka saat checkout, sistem:
1. Memeriksa pola kode pos terlebih dahulu (paling spesifik)
2. Lalu cocokkan negara bagian/provinsi
3. Lalu cocokkan negara
4. Menggunakan zona cocok dengan prioritas tertinggi

## Aturan Pengiriman

Aturan pengiriman menerapkan modifikasi kondisional pada tarif pengiriman. Buka **Pengaturan > Aturan Pengiriman** untuk mengonfigurasinya.

### Jenis Aturan

| Jenis Aturan | Deskripsi |
|-----------|-------------|
| **Diskon %** | Kurangi tarif pengiriman dengan persentase |
| **Diskon Tetap** | Kurangi tarif pengiriman dengan jumlah tetap |
| **Atur Biaya** | Ganti tarif dengan jumlah spesifik |
| **Pengiriman Gratis** | Tetapkan biaya pengiriman menjadi nol |
| **Biaya Tambahan %** | Tambahkan persentase biaya tambahan ke tarif |
| **Biaya Tambahan Tetap** | Tambahkan biaya tambahan tetap ke tarif |

### Kondisi

Setiap aturan dapat memiliki satu atau lebih kondisi yang harus dipenuhi:

| Kondisi | Contoh |
|-----------|---------|
| **Nilai Keranjang** | Pengiriman gratis untuk pesanan di atas $100 |
| **Total Berat** | Biaya tambahan untuk pesanan di atas 30 kg |
| **Jumlah Item** | Diskon untuk pesanan dengan 5+ item |
| **Zona Pengiriman** | Terapkan aturan hanya untuk pengiriman domestik |
| **Metode Pengiriman** | Terapkan ke metode pengiriman penyedia tertentu |
| **Produk** | Tarif khusus untuk produk tertentu |
| **Grup Pelanggan** | Pelanggan VIP mendapatkan pengiriman gratis |
| **Rentang Tanggal** | Promosi pengiriman hari raya |

### Prioritas Aturan

- Aturan dievaluasi dalam urutan prioritas (angka terendah terlebih dahulu)
- **Berhenti Memeriksa Aturan Lain** — Saat diaktifkan, jika aturan ini cocok, tidak akan ada aturan lain yang diperiksa
- Banyak aturan dapat tumpang tindih (misalnya, aturan diskon 10% plus aturan ambang batas pengiriman gratis)

## Tabel Tarif

Tabel tarif menyediakan harga bertingkat berdasarkan atribut pesanan. Buka **Pengaturan > Tabel Tarif Pengiriman** untuk mengonfigurasinya.

### Jenis Tabel

Buat tingkat harga berdasarkan:
- **Berat** — Tingkat harga berdasarkan berat total pesanan (misalnya, 0-1 kg = $5, 1-5 kg = $10)
- **Nilai Pesanan** — Tingkat harga berdasarkan subtotal keranjang
- **Jumlah** — Tingkat harga berdasarkan jumlah item

### Membuat Tabel Tarif

1. Klik **+ Tambah Tabel Tarif**
2. Namai tabel dan pilih jenis tingkat
3. Tambahkan tingkat dengan rentang min/max dan harga
4. Hubungkan tabel tarif ke zona pengiriman

Tabel tarif berguna ketika Anda tidak menggunakan tarif API pengirim dan ingin mendefinisikan struktur harga sendiri.

## Paket Pengiriman

Definisikan ukuran kemasan standar untuk perhitungan tarif yang akurat. Buka **Pengaturan > Paket Pengiriman**.

Untuk setiap jenis paket, atur:
- **Nama** — Deskripsi (misalnya, "Kotak Kecil", "Paket Besar Tarif Tetap")
- **Dimensi** — Panjang, lebar, tinggi
- **Berat Maksimum** — Berat maksimum yang dapat ditahan oleh paket
- **Default** — Gunakan paket ini ketika tidak ada kemasan spesifik yang ditugaskan

Penyedia menggunakan dimensi paket untuk perhitungan berat dimensi, yang dapat memengaruhi tarif pengiriman.

## Pengirim Manual (Pengaturan Pengirim)

Untuk pengirim tanpa integrasi API, buat pengaturan pengirim manual:

1. Buka **Pengaturan > Pengaturan Pengirim**
2. Klik **+ Tambah Pengaturan**
3. Konfigurasikan:
   - **Nama Pengirim** — Nama tampilan untuk checkout
   - **Template URL Pelacakan** — Pola URL dengan penempatan `{nomor_pelacakan}` (misalnya, `https://track.carrier.com/?id={tracking_number}`)
   - **Estimasi Pengiriman** — Rentang waktu pengiriman yang ditampilkan kepada pelanggan
4. Hubungkan dengan tabel tarif untuk harga

Pengirim manual menyediakan tautan pelacakan dan estimasi pengiriman tanpa integrasi API langsung.

## Pengiriman Multi-Gudang

Jika Anda memiliki beberapa gudang, pengiriman dapat dihitung dari asal yang berbeda:

- **Gudang Berdasarkan Negara** — Tetapkan gudang ke negara spesifik untuk jarak pengiriman yang lebih pendek
- **Rantai Cadangan** — Definisikan gudang mana yang mengirim saat gudang utama habis
- **Penugasan Berdasarkan Produk** — Beberapa produk mungkin hanya dikirim dari gudang spesifik

Sistem secara otomatis memilih gudang terbaik berdasarkan lokasi pelanggan dan ketersediaan produk.

## Tips

- Hubungkan API pengirim untuk **tarif langsung** selama mungkin — mereka lebih akurat daripada tabel tarif tetap dan menyesuaikan berdasarkan berat, dimensi, dan tujuan.
- Buat zona pengiriman **"Rest of World"** sebagai penangkap semua negara yang tidak tertutup oleh zona spesifik.
- Gunakan jenis aturan **Pengiriman Gratis** dengan kondisi nilai keranjang sebagai insentif penjualan (misalnya, "Pengiriman gratis untuk pesanan di atas $75").
- Uji perhitungan tarif pengiriman dengan alamat dan konten keranjang yang berbeda sebelum go live.
- Atur **Pengaturan Pengirim** dengan template URL pelacakan untuk pengirim lokal yang tidak memiliki integrasi API — pelanggan tetap mendapatkan tautan pelacakan.
- Gunakan **Paket Pengiriman** untuk mendapatkan harga berat dimensi yang akurat dari penyedia seperti FedEx dan UPS.