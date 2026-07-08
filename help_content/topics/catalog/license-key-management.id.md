---
title: Manajemen Lisensi Kunci
---

Manajemen lisensi kunci memungkinkan Anda mengontrol cara kunci lisensi perangkat lunak dibuat, disimpan, dan dikirimkan ke pelanggan saat mereka membeli produk digital. Spwig mendukung pembuatan kunci bawaan, kumpulan kunci yang sudah diisi sebelumnya, dan integrasi dengan layanan manajemen lisensi pihak ketiga.

## Ringkasan

Ada tiga cara untuk mengelola kunci lisensi di Spwig:

| Metode | Terbaik untuk |
|--------|---------|
| **Template lisensi** | Membuat otomatis kunci unik dalam format kustom saat pembelian |
| **Kumpulan lisensi** | Membuat sejumlah kunci secara pradahulu untuk distribusi dalam jumlah besar |
| **Pemasok eksternal** | Menyerahkan pembuatan dan manajemen kunci ke layanan pihak ketiga seperti Keygen.sh |

Metode ini dapat dikombinasikan — contohnya, sebuah kumpulan dapat menggunakan template kustom untuk mendefinisikan format kunci, dan secara opsional sinkronkan kunci yang dibuat ke pemasok eksternal.

## Template kunci lisensi

Sebuah template kunci lisensi mendefinisikan *format* dari kunci yang dibuat. Template menggunakan pola dengan tempat penempatan yang Spwig isi saat pembuatan.

### Membuat template

1. Navigasi ke **Katalog > Template Kunci Lisensi**
2. Klik **+ Tambah Template Kunci Lisensi**
3. Masukkan **Nama** (contoh: `Lisensi Aplikasi Standar`)
4. Konfigurasikan **Pola** menggunakan tempat penempatan (lihat di bawah)
5. Tetapkan **Awalan** dan **Akhiran** jika diperlukan (contoh, awalan `MYAPP` menambahkan `MYAPP-` ke setiap kunci)
6. Pilih karakter **Pemisah** (default: `-`)
7. Tetapkan **Kumpulan Karakter** — karakter yang digunakan untuk bagian acak. Defaultnya menghilangkan karakter yang ambigu seperti `0` dan `O`, `1` dan `I`
8. Tetapkan **Panjang Minimum/Maksimum** untuk validasi
9. Klik **Simpan**

### Tempat penempatan pola

| Tempat Penempatan | Deskripsi | Contoh Output |
|-------------|-------------|---------------|
| `{RANDOM:N}` | N karakter acak dari kumpulan karakter | `{RANDOM:5}` → `K7JXQ` |
| `{CHECKSUM:N}` | N digit checksum untuk validasi | `{CHECKSUM:2}` → `47` |
| `{PREFIX}` | Nilai awalan dari template | `MYAPP` |
| `{SUFFIX}` | Nilai akhiran dari template | `PRO` |
| `{ORDER_ID}` | Nomor pesanan | `10045` |
| `{PRODUCT_SKU}` | SKU produk | `SOFTPRO` |
| `{DATE:FORMAT}` | Tanggal yang diformat | `{DATE:YYMMDD}` → `260318` |

**Contoh pola**: `{PREFIX}-{RANDOM:5}-{RANDOM:5}-{RANDOM:5}-{CHECKSUM:2}`

Ini menghasilkan kunci seperti: `MYAPP-K7JXQ-M3TPR-9BWKN-47`

### Melihat pratinjau kunci

Setelah menyimpan template, aksi **Buat Contoh Kunci** tersedia di daftar template. Gunakan ini untuk memverifikasi pola Anda menghasilkan kunci dalam format yang diharapkan sebelum menetapkan template ke produk.

## Kumpulan lisensi

Sebuah kumpulan lisensi adalah sejumlah kunci yang sudah dibuat sebelumnya untuk sebuah produk. Kumpulan berguna ketika:
- Anda membutuhkan kunci untuk kemasan fisik (kotak ritel, kartu cetak)
- Anda bekerja dengan distributor yang membutuhkan sejumlah kunci
- Anda ingin kunci dibuat sebelumnya, bukan saat dibutuhkan

### Membuat kumpulan lisensi

1. Navigasi ke **Katalog > Kumpulan Lisensi**
2. Klik **+ Tambah Kumpulan Lisensi**
3. Isi detail kumpulan:

| Bidang | Deskripsi |
|-------|-------------|
| **Nama** | Nama deskriptif (contoh: `Pack Retail Q1 2026`) |
| **Produk** | Produk yang kunci ini untuk |
| **Template Lisensi** | Template untuk format kunci (default ke template produk) |
| **Total Kunci** | Berapa banyak kunci yang akan dibuat |
| **Jenis Kunci** | Permanen, langganan, atau uji coba |
| **Aktivasi Maksimum** | Berapa banyak perangkat yang dapat diaktifkan oleh setiap kunci |
| **Berakhir Setelah Hari** | Hari hingga lisensi berakhir setelah aktivasi pertama (biarkan kosong untuk tidak berakhir) |
| **Kumpulan Berakhir Pada** | Tanggal setelahnya kunci yang tidak digunakan dari kumpulan ini menjadi tidak valid |
| **Sinkron ke Pemasok** | Opsional sinkronkan kunci yang dibuat ke pemasok lisensi eksternal |

4. Klik **Simpan** — Spwig mulai membuat kunci di latar belakang

### Status kumpulan

| Status | Makna |
|--------|-------|
| **Generating** | Kunci sedang dibuat di latar belakang |
| **Ready** | Semua kunci telah dibuat dan siap didistribusikan |
| **Depleted** | Semua kunci telah dialokasikan ke pesanan |
| **Expired** | Tanggal kedaluwarsa dari pool telah lewat |

### Memantau sebuah pool

Daftar pool menunjukkan berapa banyak kunci yang telah didistribusikan dibandingkan dengan total kunci yang telah dibuat. Buka sebuah pool untuk melihat daftar lengkap kunci dan status masing-masing.

## Penyedia lisensi eksternal

Penyedia eksternal adalah layanan manajemen lisensi pihak ketiga yang menangani pembuatan kunci dan pelacakan aktivasi. Ketika pelanggan menyelesaikan pembelian, Spwig berkomunikasi dengan penyedia untuk membuat dan mendaftarkan kunci.

### Penyedia yang didukung

| Penyedia | Jenis |
|----------|------|
| **Spwig Built-in License Server** | Bawaan — tidak diperlukan akun eksternal |
| **Keygen.sh** | API manajemen lisensi berbasis awan |
| **LicenseSpring** | Manajemen lisensi perusahaan |
| **Cryptlex** | Manajemen lisensi dengan dukungan offline |
| **Custom API** | Sistem lisensi berbasis REST apa pun |

### Menghubungkan penyedia

1. Navigasikan ke **Catalog > License Providers**
2. Klik **+ Add License Provider**
3. Isi detail penyedia:

| Field | Deskripsi |
|-------|-------------|
| **Name** | Label untuk koneksi ini (misalnya, `Keygen Production`) |
| **Provider Type** | Pilih dari penyedia yang didukung |
| **API Endpoint** | URL dasar API penyedia |
| **API Key** | Kunci otentikasi untuk penyedia |
| **API Secret** | Jika diperlukan oleh penyedia |

4. Konfigurasikan perilaku sinkronisasi:
   - **Sync on Order** — Sinkronisasi otomatis saat pelanggan menyelesaikan pembelian
   - **Sync on Activation** — Laporkan aktivasi perangkat ke penyedia
   - **Sync on Deactivation** — Laporkan deaktivasi (berguna untuk transfer lisensi dan pengembalian dana)
   - **Bidirectional Sync** — Izinkan penyedia untuk memperbarui catatan Spwig melalui webhooks

5. Klik **Save**, lalu klik **Test Connection** untuk memverifikasi kredensial bekerja

### Status koneksi

Setiap penyedia menampilkan salah satu dari tiga status koneksi:

| Status | Makna |
|--------|-------|
| **Not Tested** | Koneksi belum diverifikasi |
| **Connected** | Uji terakhir berhasil |
| **Error** | Uji koneksi gagal — periksa pesan kesalahan |

### Sinkronisasi lisensi yang ada

Untuk mendorong secara manual lisensi yang sudah ada ke penyedia (untuk pengaturan awal atau setelah sinkronisasi gagal), gunakan aksi **Sync Now** dari daftar penyedia.

## Memantau aktivitas sinkronisasi

Navigasikan ke **Catalog > External License Syncs** untuk melihat log sinkronisasi. Setiap catatan menunjukkan:
- Kunci lisensi yang telah disinkronisasi
- Penyedia yang dikirim ke
- Arah (Spwig → Penyedia atau Penyedia → Spwig)
- Status (Pending, Success, Failed)
- Detail kesalahan untuk sinkronisasi yang gagal

Sinkronisasi yang gagal akan dicoba otomatis. Anda juga dapat memaksa ulang coba dengan mengedit catatan dan menghapus kesalahan.

## Tips

- Gunakan himpunan karakter bawaan (`ABCDEFGHJKLMNPQRSTUVWXYZ23456789`) untuk menghindari karakter yang mudah disalahartikan oleh pelanggan — himpunan ini tidak mencakup `0`, `O`, `1`, dan `I`.
- Tambahkan segmen `{CHECKSUM}` ke pola template Anda agar pelanggan dan tim dukungan Anda dapat dengan cepat mendeteksi kunci yang salah ketik.
- Untuk produk bervolume tinggi, gunakan pool daripada pembuatan on-demand untuk memastikan kunci dikirimkan secara instan saat checkout.
- Tetapkan **Pool Expires At** pada batch kunci musiman atau terbatas waktu agar kunci lama yang tidak digunakan secara otomatis dinonaktifkan.
- Selalu uji koneksi penyedia setelah pengaturan dan setelah perubahan kredensial apa pun — koneksi yang rusak berarti pelanggan tidak menerima kunci mereka.
- Jika menggunakan sinkronisasi dua arah, konfigurasikan URL webhook penyedia Anda untuk mengarah ke titik akhir webhook lisensi toko Anda.