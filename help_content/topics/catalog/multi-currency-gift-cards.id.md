---
title: Kartu Hadiah Multi Mata Uang
---

Jika Anda menjual kepada pelanggan di berbagai negara, Anda dapat menerbitkan kartu hadiah dalam mata uang tertentu. Misalnya, seorang pelanggan Selandia Baru dapat membeli kartu hadiah sebesar $50 NZD dan penerima menggunakannya dalam NZD — nilai nominal tetap sama terlepas dari fluktuasi tingkat pertukaran.

Fitur ini memerlukan multi-mata uang untuk diaktifkan dengan setidaknya satu penyedia tingkat pertukaran yang dikonfigurasikan.

## Bagaimana cara kerjanya

Ketika Anda menetapkan **Mata Uang Kartu Hadiah** pada produk kartu hadiah, sistem akan mengubah harga produk menjadi mata uang target saat pembelian menggunakan tingkat pertukaran saat ini. Kartu hadiah yang dihasilkan dinyatakan dalam mata uang tersebut dan hanya dapat ditukarkan oleh pelanggan yang berbelanja dalam mata uang yang sama.

| Langkah | Apa yang terjadi |
|--------|----------------|
| **Pengaturan Produk** | Anda menetapkan harga produk kartu hadiah dalam mata uang dasar Anda dan memilih mata uang target (misalnya, NZD) |
| **Pembelian** | Seorang pelanggan membeli kartu hadiah. Harga dasar dikonversi ke NZD menggunakan tingkat pertukaran saat ini |
| **Kartu Hadiah Dibuat** | Kartu hadiah diterbitkan dengan nilai dalam NZD (misalnya, NZ$78.50) |
| **Penukaran** | Penerima mengaplikasikan kode saat checkout sambil berbelanja dalam NZD. Saldo NZD dikurangi |

## Prasyarat

Sebelum mengatur kartu hadiah multi-mata uang, pastikan Anda memiliki:

1. **Multi-mata uang diaktifkan** — Buka **Pengaturan > Pengaturan Toko** dan aktifkan dukungan multi-mata uang
2. **Mata uang yang didukung dikonfigurasikan** — Tambahkan mata uang yang ingin Anda tawarkan (misalnya, NZD, SGD, EUR)
3. **Penyedia tingkat pertukaran terhubung** — Buka **Pengaturan > Tingkat Pertukaran** dan konfigurasikan penyedia sehingga tingkat pertukaran langsung tersedia

## Mengatur produk kartu hadiah multi-mata uang

### Langkah 1: Membuat atau mengedit produk kartu hadiah

1. Navigasi ke **Produk > Semua Produk**
2. Klik **+ Tambah Produk** atau buka produk kartu hadiah yang sudah ada
3. Setel **Jenis Produk** menjadi **Kartu Hadiah**

### Langkah 2: Menetapkan mata uang kartu hadiah

1. Klik tab **Kartu Hadiah**
2. Konfigurasikan pengaturan denominasi Anda seperti biasa (jumlah tetap, jumlah khusus, atau keduanya)
3. Di bagian bawah tab Kartu Hadiah, temukan dropdown **Mata Uang Kartu Hadiah**
4. Pilih mata uang target (misalnya, **NZD - New Zealand Dollar**)
5. Simpan produk

Dropdown menampilkan semua mata uang yang diaktifkan dalam pengaturan toko Anda. Memilih **Mata Uang Dasar Toko (default)** berarti kartu hadiah akan diterbitkan dalam mata uang dasar Anda — ini adalah perilaku standar.

### Langkah 3: Menetapkan harga

Tetapkan harga produk dalam mata uang dasar Anda seperti biasa. Ketika seorang pelanggan membeli kartu hadiah ini, harga akan secara otomatis dikonversi ke mata uang target menggunakan tingkat pertukaran saat ini.

**Contoh:** Mata uang dasar Anda adalah USD. Anda membuat produk kartu hadiah dengan harga $50 USD dan Mata Uang Kartu Hadiah diatur ke NZD. Jika tingkat pertukaran adalah 1 USD = 1.57 NZD, kartu hadiah yang dihasilkan akan memiliki nilai NZ$78.50.

## Pemadanan Mata Uang dan Penukaran

Kartu hadiah multi-mata uang menggunakan **penukaran mata uang yang sama** — mata uang berbelanja aktif pelanggan harus cocok dengan mata uang kartu hadiah.

### Pengalaman pelanggan

- Seorang pelanggan yang berbelanja dalam **NZD** dapat mengaplikasikan kartu hadiah NZD saat checkout
- Seorang pelanggan yang berbelanja dalam **USD** tidak dapat mengaplikasikan kartu hadiah NZD — mereka akan melihat pesan yang menjelaskan ketidakcocokan mata uang
- Pelanggan dapat beralih mata uang berbelanja mereka menggunakan pemilih mata uang di toko Anda sebelum mengaplikasikan kartu hadiah

### Bagaimana saldo bekerja

Saldo kartu hadiah selalu dilacak dalam mata uang aslinya:

- Kartu hadiah NZ$78.50 dimulai dengan saldo NZ$78.50
- Jika seorang pelanggan membuat pembelian sebesar NZ$30, sisa saldo adalah NZ$48.50
- Saldo tidak berfluktuasi dengan tingkat pertukaran — nilai nominal tetap

Ketika kartu hadiah diterapkan saat checkout, sistem mengubah diskon menjadi mata uang dasar Anda secara internal untuk perhitungan pesanan, tetapi saldo kartu hadiah selalu dikurangi dalam mata uang aslinya.

## Mengelola kartu hadiah multi-mata uang

Navigasi ke **Produk > Kartu Hadiah** untuk melihat semua kartu hadiah yang diterbitkan. Kartu hadiah multi-mata uang ditampilkan dengan mata uang aslinya:

- **Saldo** menampilkan dalam mata uang kartu hadiah (misalnya, NZ$48.50)
- **Transaksi** mencatat jumlah dalam mata uang kartu hadiah
- **Nilai awal** menampilkan jumlah yang dikonversi saat pembelian

### Memeriksa detail tingkat pertukaran

Setiap transaksi kartu hadiah mencatat tingkat pertukaran yang digunakan saat transaksi. Hal ini menyediakan jejak audit lengkap untuk keperluan akuntansi.

## Contoh

### Contoh 1: Kartu hadiah regional untuk Selandia Baru

**Skenario:** Anda beroperasi dari AS tetapi memiliki pelanggan di Selandia Baru. Anda ingin menjual kartu hadiah yang dinyatakan dalam NZD.

| Pengaturan | Nilai |
|-----------|------|
| Nama Produk | Kartu Hadiah NZ |
| Jenis Produk | Kartu Hadiah |
| Harga | $50.00 (USD — mata uang dasar Anda) |
| Jenis Denominasi | Denominasi Tetap |
| Denominasi Tetap | 25, 50, 100, 200 |
| Mata Uang Kartu Hadiah | NZD - New Zealand Dollar |
| Masa Berlaku | 365 hari |

Ketika seorang pelanggan memilih denominasi $50:
- Sistem mengkonversi $50 USD ke NZD menggunakan tingkat pertukaran saat ini
- Sebuah kartu hadiah dibuat dengan nilai NZD setara (misalnya, NZ$78.50)
- Penerima dapat menukarkannya saat berbelanja dalam NZD

### Contoh 2: Kartu hadiah multi mata uang

**Skenario:** Anda menjual kepada pelanggan di Singapura, Australia, dan Inggris. Buat tiga produk kartu hadiah:

1. **SG Gift Card** — Mata Uang Kartu Hadiah: SGD
2. **AU Gift Card** — Mata Uang Kartu Hadiah: AUD
3. **UK Gift Card** — Mata Uang Kartu Hadiah: GBP

Setiap produk mengkonversi harga dasar Anda ke mata uang target saat pembelian. Pelanggan di setiap wilayah dapat menukarkan kartu hadiah dalam mata uang lokal mereka.

### Contoh 3: Penawaran kartu hadiah campuran

**Skenario:** Anda ingin menawarkan kartu hadiah mata uang dasar dan regional.

- **Store Gift Card** — Mata Uang Kartu Hadiah: *Mata Uang Dasar Toko (default)* — dapat ditukarkan dalam mata uang dasar Anda
- **NZ Gift Card** — Mata Uang Kartu Hadiah: NZD — hanya dapat ditukarkan dalam NZD

Kedua produk dapat berada bersamaan dalam katalog Anda. Pelanggan melihat mata uang mana kartu hadiah dinyatakan dalam saat memeriksa saldo.

## Tips

- Mulailah dengan satu mata uang regional dan uji alur lengkap (pembelian, pengiriman, penukaran) sebelum menambahkan mata uang lain.
- Tingkat pertukaran saat pembelian menentukan nilai kartu hadiah. Jika tingkat pertukaran berubah secara signifikan, nilai kartu hadiah tetap tetap — ini melindungi Anda dan pelanggan Anda.
- Jadikan mata uang jelas dalam nama produk (misalnya, "Kartu Hadiah NZ" atau "Kartu Hadiah (NZD)") agar pelanggan tahu apa yang mereka beli.
- Kartu hadiah tanpa mata uang yang ditetapkan terus berfungsi tepat seperti sebelumnya dalam mata uang dasar Anda — produk yang sudah ada tidak terpengaruh.
- Pantau penyedia tingkat pertukaran Anda untuk memastikan tingkatnya up to date. Tingkat yang ketinggalan bisa menyebabkan kartu hadiah terlalu mahal atau terlalu murah.
- Pertimbangkan denominasi Anda secara hati-hati. Sebuah denominasi $25 USD dikonversi menjadi sekitar NZ$39 — denominasi bulat dalam mata uang target mungkin terlihat lebih baik. Anda dapat membuat produk terpisah dengan denominasi yang merupakan angka bulat dalam mata uang target.