---
title: Pengirim Barang
---

Pengirim barang menghubungkan toko Anda ke API penyedia layanan pengiriman untuk tarif pengiriman langsung, pembuatan label, dan pelacakan paket. Spwig mendukung penyedia layanan utama di seluruh dunia dan juga memungkinkan Anda membuat tabel tarif manual untuk penyedia layanan tanpa integrasi API.

![Pengirim barang](/static/core/admin/img/help/shipping-providers/provider-list.webp)

## Penyedia Layanan Tersedia

| Penyedia | Wilayah | Fitur Utama |
|---------|---------|-------------|
| **FedEx** | Global | Tarif langsung, cetak label, pelacakan, multi-paket |
| **UPS** | Global | Tarif langsung, cetak label, pelacakan, validasi alamat |
| **USPS** | Amerika Serikat | Tarif domestik dan internasional, pelacakan |
| **NinjaVan** | Asia Tenggara | Pengiriman akhir, dukungan bayar di tempat |
| **Canada Post** | Kanada | Domestik dan internasional, tarif paket dan surat |
| **Australia Post** | Australia | Domestik dan internasional, paket dan ekspres |

## Menghubungkan Penyedia

Navigasikan ke **Pengaturan > Pengirim Barang** dan klik **Hubungkan Penyedia** untuk memulai wizard pengaturan.

### Langkah 1: Pilih Penyedia

Pilih dari penyedia pengiriman yang tersedia. Setiap kartu menampilkan wilayah yang didukung dan fitur penyedia.

### Langkah 2: Petunjuk Pengaturan

Lihat panduan pengaturan khusus penyedia:
- Cara membuat akun pengembang/perusahaan dengan penyedia
- Di mana menemukan kredensial API Anda
- Pengaturan akun yang diperlukan (misalnya, nomor pengirim, nomor meter)

### Langkah 3: Masukkan Kredensial

Masukkan kredensial API untuk akun penyedia Anda. Bidang yang diperlukan bervariasi tergantung penyedia:

- **API Key / Secret** — Kredensial otentikasi
- **Nomor Akun** — Nomor akun atau nomor pengirim Anda
- **Nomor Meter** — Diperlukan oleh beberapa penyedia (misalnya, FedEx)
- **Mode Sandbox** — Aktifkan untuk menguji dengan API sandbox penyedia sebelum digunakan secara langsung

### Langkah 4: Uji Koneksi

Klik **Uji Koneksi** untuk memverifikasi kredensial Anda. Wizard mengonfirmasi:
- Otentikasi API berhasil
- Izin akun valid
- Kueri tarif mengembalikan hasil yang diharapkan

### Langkah 5: Konfigurasi dan Simpan

Selesaikan pengaturan:
- **Aktif** — Aktifkan atau nonaktifkan penyedia
- **Nama Tampilan** — Nama yang ditampilkan kepada pelanggan saat checkout
- **Alamat Asal** — Alamat gudang atau alamat penyelesaian untuk perhitungan tarif

## Zona Pengiriman

Zona pengiriman mendefinisikan area geografis untuk perhitungan tarif. Navigasikan ke **Pengaturan > Zona Pengiriman** untuk mengelolanya.

### Membuat Zona

1. Klik **+ Tambah Zona**
2. Beri nama zona (misalnya, "Domestik", "Eropa", "Asia Pasifik")
3. Definisikan cakupan zona menggunakan satu atau lebih dari:
   - **Negara** — Pilih negara tertentu
   - **Negara Bagian/Provinsi** — Sempitkan ke wilayah tertentu dalam sebuah negara
   - **Polanya Kode Pos** — Cocokkan kode pos/ZIP menggunakan pola (misalnya, "90*" untuk area Los Angeles)
4. Tetapkan **Prioritas** — Ketika zona tumpang tindih, zona dengan prioritas tertinggi digunakan

### Pemadanan Zona

Ketika pelanggan memasukkan alamat pengiriman mereka saat checkout, sistem:
1. Memeriksa pola kode pos terlebih dahulu (paling spesifik)
2. Lalu cocokkan negara bagian/propinsi
3. Lalu cocokkan negara
4. Menggunakan zona dengan prioritas tertinggi yang cocok

## Promosi Pengiriman

Promosi pengiriman menerapkan modifikasi kondisional pada tarif pengiriman. Navigasikan ke **Pengaturan > Promosi Pengiriman** untuk mengonfigurasinya.

### Jenis Promosi

| Jenis Promosi | Deskripsi |
|-----------|-------------|
| **Diskon %** | Mengurangi tarif pengiriman dengan persentase |
| **Diskon Tetap** | Mengurangi tarif pengiriman dengan jumlah tetap |
| **Ganti Biaya** | Mengganti tarif dengan jumlah tertentu |
| **Pengiriman Gratis** | Menetapkan biaya pengiriman menjadi nol |
| **Biaya Tambahan %** | Menambahkan persentase biaya tambahan ke tarif |
| **Biaya Tambahan Tetap** | Menambahkan jumlah tetap biaya tambahan ke tarif |

### Kondisi

Setiap promosi dapat memiliki satu atau lebih kondisi yang harus dipenuhi:

| Kondisi | Contoh |
|-----------|---------|
| **Nilai Keranjang** | Pengiriman gratis untuk pesanan di atas $100 |
| **Total Berat** | Biaya tambahan untuk pesanan di atas 30 kg |
| **Jumlah Item** | Diskon untuk pesanan dengan 5+ item |
| **Zona Pengiriman** | Terapkan promosi hanya untuk pengiriman domestik |
| **Metode Pengiriman** | Terapkan ke metode pengangkut tertentu |
| **Produk** | Tarif khusus untuk produk tertentu |
| **Kelompok Pelanggan** | Pelanggan VIP mendapatkan pengiriman gratis |
| **Rentang Tanggal** | Promosi pengiriman liburan |

### Prioritas Promosi

- Promosi dievaluasi dalam urutan prioritas (angka terkecil terlebih dahulu)
- **Berhenti pada Promosi Berikutnya** — Saat diaktifkan, jika promosi ini cocok, tidak akan ada promosi lain yang diperiksa
- Banyak promosi dapat berlapis (misalnya, promosi diskon 10% ditambah promosi pengiriman gratis dengan ambang batas tertentu)

## Tabel Tarif

Tabel tarif menyediakan harga bertingkat berdasarkan atribut pesanan. Navigasikan ke **Pengaturan > Tabel Tarif Pengiriman** untuk mengonfigurasikannya.

### Jenis Tabel

Buat tingkatan tarif berdasarkan:
- **Berat** — Tingkatan harga berdasarkan berat total pesanan (misalnya, 0-1 kg = $5, 1-5 kg = $10)
- **Nilai Pesanan** — Tingkatan harga berdasarkan subtotal keranjang
- **Kuantitas** — Tingkatan harga berdasarkan jumlah item

### Membuat Tabel Tarif

1. Klik **+ Tambah Tabel Tarif**
2. Beri nama tabel dan pilih jenis tingkatan
3. Tambahkan tingkatan dengan rentang min/max dan harga
4. Tetapkan tabel tarif ke zona pengiriman

Tabel tarif berguna ketika Anda tidak menggunakan tarif API pengangkut dan ingin mendefinisikan struktur harga Anda sendiri.

## Paket Pengiriman

Tentukan ukuran kemasan standar untuk perhitungan tarif yang akurat. Navigasikan ke **Pengaturan > Paket Pengiriman**.

Untuk setiap jenis paket, atur:
- **Nama** — Deskripsi (misalnya, "Kotak Kecil", "Kotak Besar Tarif Tetap")
- **Dimensi** — Panjang, lebar, tinggi
- **Berat Maksimum** — Berat maksimum yang dapat ditampung oleh paket
- **Default** — Gunakan paket ini ketika tidak ada kemasan khusus yang ditetapkan

Pengangkut menggunakan dimensi paket untuk perhitungan berat dimensi, yang dapat memengaruhi tarif pengiriman.

## Pengangkut Manual (Preset Pengangkut)

Untuk pengangkut tanpa integrasi API, buat preset pengangkut manual:

1. Navigasikan ke **Pengaturan > Preset Pengangkut**
2. Klik **+ Tambah Preset**
3. Konfigurasikan:
   - **Nama Pengangkut** — Nama tampilan untuk checkout
   - **Template URL Pelacakan** — Pola URL dengan placeholder `{tracking_number}` (misalnya, `https://track.carrier.com/?id={tracking_number}`)
   - **Estimasi Pengiriman** — Rentang waktu pengiriman yang ditampilkan kepada pelanggan
4. Pasangkan dengan tabel tarif untuk penentuan harga

Pengangkut manual menyediakan tautan pelacakan dan estimasi pengiriman tanpa integrasi API langsung.

## Pengiriman Multi-Gudang

Jika Anda memiliki beberapa gudang, pengiriman dapat dihitung dari asal yang berbeda:

- **Gudang Berdasarkan Negara** — Tetapkan gudang ke negara tertentu untuk jarak pengiriman yang lebih pendek
- **Rantai Cadangan** — Tentukan gudang mana yang mengirim ketika gudang utama habis stok
- **Penugasan Berdasarkan Produk** — Beberapa produk mungkin hanya dikirim dari gudang tertentu

Sistem secara otomatis memilih gudang terbaik berdasarkan lokasi pelanggan dan ketersediaan produk.

## Tips

- Hubungkan API pengangkut untuk **tarif langsung** sebisa mungkin — mereka lebih akurat daripada tabel tarif tetap dan menyesuaikan berdasarkan berat, dimensi, dan tujuan.
- Buat zona pengiriman **"Rest of World"** sebagai penangkap untuk negara yang tidak tertutup oleh zona tertentu.
- Gunakan jenis promosi **"Pengiriman Gratis"** dengan kondisi nilai keranjang sebagai insentif penjualan (misalnya, "Pengiriman gratis untuk pesanan di atas $75").
- Uji perhitungan tarif pengiriman dengan alamat dan isi keranjang yang berbeda sebelum diluncurkan.
- Atur **Preset Pengangkut** dengan template URL pelacakan untuk pengangkut lokal yang tidak memiliki integrasi API — pelanggan tetap mendapatkan tautan pelacakan.
- Gunakan **Paket Pengiriman** untuk mendapatkan harga berat dimensi yang akurat dari pengangkut seperti FedEx dan UPS.