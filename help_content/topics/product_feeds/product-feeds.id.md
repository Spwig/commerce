---
title: Product Feeds
---

Product feeds memungkinkan Anda untuk mengekspor katalog Anda ke platform belanja seperti Google Shopping dan Facebook Catalog. Setelah terhubung, data produk Anda secara otomatis disinkronkan sesuai jadwal sehingga iklan Anda selalu mencerminkan harga, stok, dan detail produk terkini.

Toko Anda menggunakan sistem komponen penyedia untuk feeds. Setiap penyedia feed (Google, Facebook, atau lainnya) diinstal sebagai komponen dan kemudian terhubung melalui akun penyedia. Anda dapat menjalankan beberapa penyedia feed sekaligus — misalnya, satu feed untuk Google Shopping dan satu terpisah untuk Facebook.

## Menghubungkan penyedia feed

Sebelum Anda dapat menyinkronkan katalog Anda, Anda perlu menginstal dan menghubungkan setidaknya satu komponen penyedia feed.

### Menginstal komponen penyedia

Komponen penyedia tersedia di pasar komponen Spwig. Administrator toko menginstalnya melalui sistem pembaruan komponen. Setelah komponen penyedia terinstal, akan muncul sebagai opsi saat membuat akun penyedia feed.

### Membuat akun penyedia feed

1. Navigasikan ke **Pemasaran > Penyedia Feed**
2. Klik **+ Tambah Akun Penyedia Feed**
3. Isi formulir:

**Bagian Informasi Penyedia:**
- **Situs** — pilih toko Anda (hanya ada satu)
- **Komponen Penyedia** — pilih penyedia feed yang terinstal (misalnya, Google Shopping, Facebook Catalog)
- **Nama Akun** — nama deskriptif seperti `Google Shopping — Utama` atau `Facebook Catalog — US`

**Bagian Konfigurasi:**
- **Aktif** — centang untuk mengaktifkan pembuatan feed dan penyinkronan
- **Utama** — centang jika ini adalah penyedia feed utama Anda untuk jenis platform ini
- **Prioritas** — mengontrol urutan penyortiran dalam daftar (angka yang lebih rendah muncul lebih dulu)
- **Konfigurasi** — pengaturan khusus penyedia (lihat di bawah)

4. Klik **Simpan**

### Opsi konfigurasi feed

Bidang **Konfigurasi** menerima objek JSON dengan opsi berikut:

| Opsi | Nilai | Deskripsi |
|--------|--------|-------------|
| `sync_interval` | `hourly`, `daily`, `weekly`, `manual` | Seberapa sering feed secara otomatis dibuat ulang |
| `format_preference` | `xml`, `csv`, `json` | Format output (sebagian besar platform memilih XML) |
| `include_variants` | `true` / `false` | Sertakan variasi produk sebagai entri feed terpisah |
| `target_country` | Kode negara misalnya `"US"` | Negara target untuk feed |
| `content_language` | Kode bahasa misalnya `"en"` | Bahasa data produk |

#### Contoh konfigurasi untuk feed XML harian yang ditujukan ke AS:

```json
{
  "sync_interval": "daily",
  "format_preference": "xml",
  "include_variants": true,
  "target_country": "US",
  "content_language": "en"
}
```

## Memfilter produk yang muncul dalam feed

Anda dapat mengontrol secara tepat produk mana yang termasuk dengan menambahkan bagian `product_filter` ke konfigurasi:

```json
{
  "product_filter": {
    "status": ["published"],
    "in_stock_only": true,
    "categories": [1, 5, 12]
  }
}
```

| Opsi Filter | Deskripsi |
|---------------|-------------|
| `status` | Hanya termasuk produk dengan status ini. Gunakan `["published"]` untuk produk yang sedang berjalan saja. |
| `in_stock_only` | Atur ke `true` untuk mengecualikan produk yang tidak tersedia |
| `categories` | Batasi ke ID kategori tertentu |
| `brands` | Batasi ke ID merek tertentu |

Anda juga dapat mengecualikan produk tertentu dengan ID-nya menggunakan `exclude_products`:

```json
{
  "exclude_products": [42, 87, 103]
}
```

## Memantau status sinkronisasi

Daftar akun penyedia feed menampilkan status sinkronisasi setiap feed terhubung secara sekilas:

- **PENDING** — belum ada sinkronisasi yang berjalan, atau feed menunggu untuk dibuat ulang
- **SYNCING** — sinkronisasi sedang berlangsung
- **SUCCESS** — sinkronisasi terakhir selesai tanpa kesalahan
- **ERROR** — sinkronisasi terakhir gagal; pesan kesalahan ditampilkan di halaman detail akun

Daftar ini juga menampilkan jumlah produk dalam feed saat ini dan kapan sinkronisasi terakhir berjalan.

## Melihat feed yang telah dibuat

Navigasikan ke **Pemasaran > Feed Produk** untuk melihat file feed yang telah dibuat. Setiap entri mewakili satu snapshot feed yang telah dibuat dan menampilkan:

- **Akun Provider** — yang mana feed ini termasuk ke dalamnya
- **Format** — XML, CSV, atau JSON
- **Jumlah Produk** — jumlah produk yang termasuk
- **Ukuran** — ukuran file dari feed yang dihasilkan
- **Dibuat Pada** — kapan feed ini dibuat
- **Berakhir Pada** — kapan versi yang disimpan ini berakhir
- **Status** — apakah feed ini masih valid atau sudah berakhir
- **Jumlah Unduh** — seberapa banyak kali feed ini telah diunduh

Feed hanya dapat dibaca di admin — mereka dihasilkan secara otomatis oleh proses sinkronisasi.

## Melihat riwayat sinkronisasi

Navigasikan ke **Pemasaran > Feed Sync Logs** untuk melihat riwayat lengkap dari setiap upaya sinkronisasi untuk semua akun feed Anda. Setiap entri log mencatat:

- Akun provider yang disinkronkan
- Jenis sinkronisasi (Penuh, Bertahap, Manual, atau Jadwal)
- Status (Berhasil, Sebagian Berhasil, Gagal, dll.)
- Produk yang disinkronkan, gagal, dan dilewati
- Durasi sinkronisasi
- Pesan kesalahan apa pun

Dashboard log sinkronisasi di bagian atas halaman menampilkan statistik secara keseluruhan: total sinkronisasi, tingkat keberhasilan, dan rata-rata durasi sinkronisasi. Gunakan filter **Akun** dan **Jenis Sinkronisasi** untuk menyempitkan ke feed tertentu.

### Yang harus dilakukan ketika sinkronisasi gagal

1. Navigasikan ke **Pemasaran > Feed Sync Logs** dan temukan entri yang gagal
2. Klik entri log untuk melihat pesan **Error Message** dan **Error Details** secara lengkap
3. Penyebab umum meliputi:
   - Tidak adanya bidang produk yang diperlukan (judul, harga, gambar)
   - Kredensial API yang tidak valid atau sudah kedaluwarsa — instal ulang komponen provider untuk memperbarui kredensial
   - Kesalahan jaringan saat terhubung ke API provider
4. Setelah masalah terpecahkan, sinkronisasi berikutnya yang dijadwalkan akan berjalan secara otomatis, atau Anda dapat memicu sinkronisasi manual dari akun provider

## Tips

- Atur `"sync_interval": "daily"` untuk kebanyakan kasus penggunaan — Google dan Facebook tidak memerlukan pembaruan yang lebih sering kecuali Anda memiliki volatilitas harga yang sangat tinggi
- Selalu sertakan `"in_stock_only": true` dalam filter produk Anda untuk menghindari iklan produk yang tidak dapat dibeli oleh pelanggan
- Gunakan nama akun yang deskriptif yang mencakup platform dan pasar target (misalnya, `Google Shopping — UK`) sehingga mudah mengelola beberapa feed
- Jumlah **Produk dalam Feed** di akun provider memberi tahu Anda secara langsung apakah jumlah produk yang termasuk lebih sedikit dari yang diharapkan — periksa pengaturan filter produk Anda jika jumlahnya tampak rendah
- Tandai satu akun sebagai **Feed Utama** untuk setiap jenis provider; beberapa alat pelaporan menggunakan ini untuk mengidentifikasi feed utama Anda
- Periksa log sinkronisasi setelah melakukan perubahan besar pada katalog produk Anda untuk memastikan data yang diperbarui telah diambil dengan benar