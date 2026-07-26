---
title: Kartu Hadiah Multi-Mata Uang
---

Jika Anda menjual kepada pelanggan di beberapa negara, Anda dapat menerbitkan kartu hadiah dalam mata uang tertentu. Misalnya, seorang pelanggan dari Selandia Baru dapat membeli kartu hadiah sebesar $50 NZD dan penerima menggunakannya dalam NZD — nilai nominal tetap sama terlepas dari fluktuasi kurs pertukaran.

Fitur ini memerlukan multi-mata uang untuk diaktifkan dengan setidaknya satu penyedia kurs pertukaran yang dikonfigurasikan.

> **Penjualan kartu hadiah sementara dihentikan** selama kami menyelesaikan alur pengiriman otomatis — lihat topik bantuan **Kartu Hadiah** untuk detailnya. Anda tetap dapat mengonfigurasi **Mata Uang Kartu Hadiah** pada produk saat ini sehingga siap dijual saat penjualan dibuka kembali, dan Anda dapat menerbitkan kartu hadiah berbasis mata uang secara manual hari ini dengan cara yang sama seperti menerbitkan kartu hadiah lainnya (tetapkan **Nilai Awal** dalam mata uang yang diinginkan untuk kartu tersebut).

## Cara kerjanya

Ketika Anda menetapkan **Mata Uang Kartu Hadiah** pada produk kartu hadiah, sistem mengubah harga produk menjadi mata uang target saat pembelian menggunakan kurs pertukaran saat ini. Kartu hadiah yang dihasilkan dinyatakan dalam mata uang tersebut dan hanya dapat ditukarkan oleh pelanggan yang berbelanja dalam mata uang yang sama.

| Langkah | Apa yang terjadi |
|--------|----------------|
| **Pengaturan Produk** | Anda menetapkan harga produk kartu hadiah dalam mata uang dasar Anda dan memilih mata uang target (misalnya, NZD) |
| **Pembelian** | Seorang pelanggan membeli kartu hadiah. Harga dasar dikonversi ke NZD menggunakan kurs pertukaran saat ini |
| **Kartu Hadiah Dibuat** | Kartu hadiah diterbitkan dengan nilai dalam NZD (misalnya, NZ$78.50) |
| **Penukaran** | Penerima menerapkan kode saat checkout sementara berbelanja dalam NZD. Saldo NZD dikurangi |

## Prasyarat

Sebelum mengatur kartu hadiah multi-mata uang, pastikan Anda memiliki:

1. **Multi-mata uang diaktifkan** — Buka **Pengaturan > Pengaturan Toko** dan aktifkan dukungan multi-mata uang
2. **Mata uang yang didukung dikonfigurasikan** — Tambahkan mata uang yang ingin Anda tawarkan (misalnya, NZD, SGD, EUR)
3. **Penyedia kurs pertukaran terhubung** — Buka **Pengaturan > Kurs Pertukaran** dan konfigurasikan penyedia sehingga kurs langsung tersedia

## Mengatur produk kartu hadiah multi-mata uang

### Langkah 1: Buat atau edit produk kartu hadiah

1. Navigasikan ke **Produk > Semua Produk**
2. Klik **+ Tambah Produk** atau buka produk kartu hadiah yang sudah ada
3. Tetapkan **Jenis Produk** menjadi **Kartu Hadiah**

### Langkah 2: Tetapkan mata uang kartu hadiah

1. Klik tab **Kartu Hadiah**
2. Konfigurasikan pengaturan denominasi Anda seperti biasa (jumlah tetap, jumlah khusus, atau keduanya)
3. Di bagian bawah tab Kartu Hadiah, cari dropdown **Mata Uang Kartu Hadiah**
4. Pilih mata uang target (misalnya, **NZD - New Zealand Dollar**)
5. Simpan produk

Dropdown menampilkan semua mata uang yang diaktifkan dalam pengaturan toko Anda. Memilih **Mata Uang Dasar Toko (default)** berarti kartu hadiah akan diterbitkan dalam mata uang dasar Anda — ini adalah perilaku standar.

### Langkah 3: Tetapkan harga

Tetapkan harga produk dalam mata uang dasar Anda seperti biasa. Ketika seorang pelanggan membeli kartu hadiah ini, harga akan secara otomatis dikonversi ke mata uang target menggunakan kurs pertukaran saat ini.

**Contoh:** Mata uang dasar Anda adalah USD. Anda membuat produk kartu hadiah dengan harga $50 USD dengan Mata Uang Kartu Hadiah diatur ke NZD. Jika kurs pertukaran adalah 1 USD = 1.57 NZD, kartu hadiah yang dihasilkan akan memiliki nilai sebesar NZ$78.50.

## Pemadanan mata uang dan penukaran

Kartu hadiah multi-mata uang menggunakan **penukaran dalam mata uang yang sama** — mata uang belanja aktif pelanggan harus cocok dengan mata uang kartu hadiah.

### Pengalaman pelanggan

- Seorang pelanggan yang berbelanja dalam **NZD** dapat menerapkan kartu hadiah NZD saat checkout
- Seorang pelanggan yang berbelanja dalam **USD** tidak dapat menerapkan kartu hadiah NZD — mereka akan melihat pesan yang menjelaskan ketidakcocokan mata uang
- Pelanggan dapat beralih mata uang belanja mereka menggunakan pemilih mata uang di toko online Anda sebelum menerapkan kartu hadiah

### Cara kerja saldo

Saldo kartu hadiah selalu dilacak dalam mata uang aslinya:

- Sebuah kartu hadiah sebesar NZ$78.50 dimulai dengan saldo NZ$78.50
- Jika seorang pelanggan melakukan pembelian sebesar NZ$30, sisa saldonya adalah NZ$48.50
- Saldo tidak berubah sesuai dengan kurs valuta asing — nilai nominal tetap

Ketika kartu hadiah diterapkan saat checkout, sistem mengubah diskon menjadi mata uang dasar Anda secara internal untuk perhitungan pesanan, tetapi saldo kartu hadiah selalu dikurangi dalam mata uang aslinya.

## Mengelola kartu hadiah multi-mata uang

Navigasikan ke **Produk > Kartu Hadiah** untuk melihat semua kartu hadiah yang diterbitkan. Kartu hadiah multi-mata uang ditampilkan dengan mata uang aslinya:

- **Saldo** ditampilkan dalam mata uang kartu hadiah (misalnya, NZ$48.50)
- **Transaksi** mencatat jumlah dalam mata uang kartu hadiah
- **Nilai awal** menampilkan jumlah yang dikonversi saat pembelian

### Memeriksa detail kurs valuta

Setiap transaksi kartu hadiah mencatat kurs valuta yang digunakan saat transaksi tersebut. Hal ini memberikan jejak audit lengkap untuk keperluan akuntansi.

## Contoh

### Contoh 1: Kartu hadiah regional untuk Selandia Baru

**Skenario:** Anda beroperasi dari AS tetapi memiliki pelanggan di Selandia Baru. Anda ingin menjual kartu hadiah yang dinominasikan dalam NZD.

| Pengaturan | Nilai |
|---------|-------|
| Nama produk | Kartu Hadiah NZ |
| Jenis produk | Kartu Hadiah |
| Harga | $50.00 (USD — mata uang dasar Anda) |
| Jenis denominasi | Denominasi Tetap |
| Denominasi tetap | 25, 50, 100, 200 |
| Mata uang kartu hadiah | NZD - New Zealand Dollar |
| Masa berlaku | 365 hari |

Ketika seorang pelanggan memilih denominasi $50:
- Sistem mengkonversi $50 USD ke NZD dengan kurs saat ini
- Sebuah kartu hadiah dibuat dengan nilai NZD setara (misalnya, NZ$78.50)
- Penerima dapat mencairkannya saat berbelanja dalam NZD

### Contoh 2: Kartu hadiah multi-mata uang

**Skenario:** Anda menjual kepada pelanggan di Singapura, Australia, dan Inggris. Buat tiga produk kartu hadiah:

1. **Kartu Hadiah SG** — Mata uang kartu hadiah: SGD
2. **Kartu Hadiah AU** — Mata uang kartu hadiah: AUD
3. **Kartu Hadiah UK** — Mata uang kartu hadiah: GBP

Setiap produk mengkonversi harga dasar Anda ke mata uang target saat pembelian. Pelanggan di setiap wilayah dapat mencairkan kartu hadiah dalam mata uang lokal mereka.

### Contoh 3: Penawaran kartu hadiah campuran

**Skenario:** Anda ingin menawarkan kartu hadiah dalam mata uang dasar dan regional.

- **Kartu Hadiah Toko** — Mata uang kartu hadiah: *Mata uang dasar toko (default)* — dapat diklaim dalam mata uang dasar Anda
- **Kartu Hadiah NZ** — Mata uang kartu hadiah: NZD — hanya dapat diklaim dalam NZD

Kedua produk dapat berdampingan dalam katalog Anda. Pelanggan melihat mata uang mana kartu hadiah tersebut dinominasikan saat memeriksa saldo.

## Tips

- Mulailah dengan satu mata uang regional dan uji alur lengkap (pembelian, pengiriman, pencairan) sebelum menambahkan mata uang lain.
- Kurs valuta saat pembelian menentukan nilai kartu hadiah. Jika kurs berubah secara signifikan, nilai kartu hadiah tetap tetap — ini melindungi Anda dan pelanggan Anda.
- Buat mata uang jelas dalam nama produk (misalnya, "Kartu Hadiah NZ" atau "Kartu Hadiah (NZD)") agar pelanggan tahu apa yang mereka beli.
- Kartu hadiah tanpa mata uang yang ditetapkan tetap berfungsi persis seperti sebelumnya dalam mata uang dasar Anda — produk yang ada tidak terpengaruh.
- Pantau penyedia kurs valuta Anda untuk memastikan kursnya up-to-date. Kurs yang ketinggalan bisa menyebabkan kartu hadiah terlalu mahal atau terlalu murah.
- Pertimbangkan denominasi Anda secara hati-hati. Denominasi $25 USD dikonversi menjadi sekitar NZ$39 — denominasi bulat dalam mata uang target mungkin terlihat lebih baik. Anda dapat membuat produk terpisah dengan denominasi yang merupakan angka bulat dalam mata uang target.