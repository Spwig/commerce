---
title: Kartu Hadiah
---

Kartu hadiah adalah kredit toko yang dapat dibeli oleh pelanggan untuk orang lain — atau untuk diri mereka sendiri — yang dikirimkan melalui email sebagai kode pemakaian unik. Anda juga dapat menerbitkan kartu hadiah secara langsung dari admin tanpa pembelian pelanggan.

Penjualan kartu hadiah sudah aktif. Ketika seorang pelanggan membeli satu, kartu akan dibuat dan dikirimkan secara otomatis setelah pembayaran mereka selesai — tidak sebelumnya, sehingga tidak ada yang menerima kode untuk pembayaran yang gagal nanti.

Beberapa hal yang perlu diketahui sebelum Anda mengaktifkan produk kartu hadiah:

- **Kartu hadiah adalah uang, bukan diskon.** Ini akan dikurangi dari total tagihan setelah pajak dan pengiriman, dan tidak mengurangi pajak yang Anda harus bayar. Ini berkebalikan dengan voucher, yang mengurangi harga barang.
- **Kartu hadiah hanya dalam satu mata uang.** Kartu yang dibeli dalam euro hanya dapat digunakan untuk pesanan dalam euro. Jika Anda menjual dalam beberapa mata uang, buat produk kartu hadiah terpisah untuk masing-masing. Ini melindungi Anda dari perubahan nilai tukar pada saldo yang mungkin tidak digunakan selama setahun.
- **Kartu hadiah tidak dapat didiskon.** Voucher tidak akan berlaku untuk baris kartu hadiah, karena menjual kredit sebesar £100 dengan harga £80 akan membuat Anda kehilangan £20 setiap kali.
- **Kartu hadiah tidak dapat membeli kartu hadiah lain.** Ini menutup jalur yang digunakan orang untuk mencuci uang dari kartu yang dicuri.
- **Membeli kartu hadiah tidak menghasilkan poin loyalitas.** Poin hanya diberikan ketika kartu digunakan untuk membeli barang, sehingga tidak ada yang mendapatkan poin dua kali untuk uang yang sama.

![Manajemen kartu hadiah](/static/core/admin/img/help/gift-cards/gift-card-list.webp)

## Jenis Nominal

Pengaturan ini mengontrol cara pelanggan memilih jumlah saat membeli kartu hadiah:

| Jenis | Deskripsi |
|------|-------------|
| **Nominal Tetap** | Pelanggan memilih dari jumlah yang telah ditetapkan (misalnya, $25, $50, $100) |
| **Jumlah Kustom** | Pelanggan memasukkan jumlah apa pun dalam rentang minimum/maksimum |
| **Keduanya** | Tawarkan nominal tetap ditambah opsi jumlah kustom |

## Membuat Produk Kartu Hadiah

Setiap kartu hadiah — baik yang akhirnya akan dijual atau diterbitkan secara manual hari ini — memerlukan produk jenis Kartu Hadiah di belakangnya terlebih dahulu.

### Langkah 1: Menyiapkan Produk

1. Navigasikan ke **Produk > Semua Produk** dan klik **+ Tambahkan Produk**
2. Atur **Jenis Produk** menjadi **Kartu Hadiah**
3. Isi nama dan deskripsi produk
4. Konfigurasikan pengaturan nominal:
   - Pilih **Jenis Nominal** (Tetap, Kustom, atau Keduanya)
   - Untuk Tetap: atur jumlah nominal yang tersedia
   - Untuk Kustom: atur **Minimum** dan **Maksimum** jumlah yang diperbolehkan
5. Atur **Hari Kadaluarsa** (0 = tidak pernah kadaluarsa) — ini menentukan seberapa lama kartu hadiah tetap valid setelah dibeli
6. Simpan dan publikasikan produk

### Langkah 2: Mempublikasikan

Publikasikan produk ketika Anda siap untuk menjualnya. Pelanggan dapat membelinya langsung dari toko Anda, dan kartu akan dikirimkan secara otomatis setelah pembayaran mereka selesai.

Produk ini juga yang Anda pilih ketika menerbitkan kartu secara manual — jadi, sepadan untuk membuat satu bahkan jika Anda hanya berencana memberikan kartu secara gratis.

## Membuat Kartu Hadiah Secara Manual

Ini adalah satu-satunya cara untuk membuat kartu hadiah yang dibiayai saat ini, dan ini sudah berfungsi sepenuhnya hari ini.

1. Navigasikan ke **Produk > Kartu Hadiah** dan klik **+ Tambahkan Kartu Hadiah**
2. Pilih **Produk** — ini harus menjadi produk jenis Kartu Hadiah yang sudah ada (lihat di atas)
3. Masukkan **Nilai Awal** — saldo awal, dalam jumlah apa pun yang Anda pilih. Berbeda dengan pembelian pelanggan, ini tidak dibatasi oleh pengaturan nominal produk
4. Secara opsional, atur tanggal **Kadaluarsa Pada**, dan biarkan **Aktif** dicentang agar kartu dapat ditukarkan
5. Isi bagian **Penerima**, lebih jauh di halaman yang sama:
   - **Email Penerima** — wajib; tempat email pengiriman akan dikirimkan
   - **Nama Penerima**, **Nama Pengirim**, dan **Pesan Pribadi** — semua opsional
   - **Tanggal Kirim Terjadwal** — opsional; biarkan kosong dan kirim kapan saja Anda siap, atau atur tanggal/waktu di masa depan (misalnya, ulang tahun)
6. Klik **Simpan**

Kode pemakaian akan dihasilkan secara otomatis dan saldo awal diatur dari Nilai Awal — Anda tidak perlu mengisi salah satunya sendiri.

**Menyimpan kartu tidak mengirimkannya melalui email.** Untuk mengirimkannya, kembali ke daftar kartu hadiah, pilih checkbox kartu tersebut, pilih **Kirim email kartu hadiah** dari dropdown Aksi, lalu klik **Lanjutkan**.

Tindakan yang sama mengirim ulang email jika Anda perlu mengirimkannya kembali nanti.

## Mengelola Kartu Hadiah di Admin

Navigasikan ke **Produk > Kartu Hadiah** untuk mengelola semua kartu hadiah:

### Dashboard Statistik

Di bagian atas halaman, empat kartu menampilkan metrik kunci:

- **Total Kartu Hadiah** — Jumlah total kartu hadiah yang diterbitkan
- **Aktif** — Kartu yang saat ini aktif dengan saldo tersedia
- **Total Saldo** — Saldo tersisa yang dikombinasikan dari semua kartu
- **Dibeli Sebagian** — Kartu yang telah dibeli sebagian

### Filter

Saring kartu hadiah berdasarkan:

- **Cari** — Cari berdasarkan kode, email, atau nama penerima
- **Status** — Aktif, Tidak Aktif, Kadaluarsa, Telah Dibeli Sepenuhnya, atau Dibeli Sebagian
- **Saldo** — Memiliki Saldo atau Saldo Nol
- **Dibuat** — Periode waktu (Hari Ini, Minggu Ini, Bulan Ini, Tahun Ini)

### Detail Kartu Hadiah

Setiap kartu hadiah menampilkan:

- **Kode** — Kode unik untuk pembelian (misalnya, GC-XXXX-XXXX-XXXX)
- **Penerima** — Email dan nama
- **Status badge** — Status saat ini dengan kode warna
- **Saldo / Awal / Dibeli** — Ringkasan keuangan dengan persentase yang telah dibeli
- **Tanggal penting** — Dibuat, diterbitkan, digunakan pertama kali
- **Pengirim** — Siapa yang membeli (atau siapa yang menerbitkan) kartu hadiah

### Aksi

- Klik sebuah kartu hadiah untuk **mengedit** detailnya dan lihat **riwayat transaksi** lengkapnya, yang ditampilkan secara inline di halaman yang sama
- Pilih satu atau lebih kartu dan gunakan dropdown **Aksi** untuk **Kirim email kartu hadiah** (mengirimkan atau mengirim ulang email pengiriman) atau **Tandai kartu hadiah yang dipilih sebagai tidak aktif** (menonaktifkan — saldo tetap dijaga tetapi kartu tidak dapat lagi dibeli)

## Pembelian Hari Ini

**Di toko**, di terminal Point of Sale Anda:

1. Kasir mengambil kode pada langkah pembayaran
2. Kode divalidasi — aktif, belum kadaluarsa, memiliki saldo, dan dalam mata uang yang sama dengan penjualan
3. Saldo diterapkan ke jumlah total yang terutang, termasuk pajak dan pengiriman
4. Jika saldo tidak menutupi seluruh penjualan, pelanggan membayar sisa dengan cara lain
5. Saldo dikurangi dan transaksi dicatat

Catat bahwa kasir mengambil kode pada **pembayaran**, bukan saat membangun keranjang. Kartu hadiah adalah uang yang sudah diberikan oleh pelanggan, sehingga menyelesaikan tagihan daripada memberikan diskon pada barang.

**Secara online**, proses checkout memiliki bidang kartu hadiah pada langkah pembayaran. Pelanggan memasukkan kode mereka, saldo dikurangi dari jumlah yang terutang — setelah pajak dan pengiriman — dan sisa dibebankan ke kartu mereka seperti biasa. Jika kartu menutupi seluruh pesanan, tidak diperlukan pembayaran lain. Saldo hanya benar-benar dikurangi setelah pembayaran dikonfirmasi, sehingga checkout yang dibatalkan tidak akan menyentuh kartu.

Penerima juga dapat memeriksa sisa saldo mereka kapan saja melalui tautan di email pengiriman mereka.

## Penanganan Pengembalian Dana

Ketika mengembalikan pesanan atau penjualan yang menggunakan kartu hadiah:

- **Kartu hadiah yang dibeli oleh pelanggan, belum digunakan** — kartu dinonaktifkan dan saldonya diatur menjadi nol, sehingga kredit menghilang bersama pengembalian dana.
- **Kartu hadiah yang dibeli oleh pelanggan dan telah digunakan sebagian** — ini memerlukan penilaian Anda. Menonaktifkannya akan mengembalikan kredit yang sudah digunakan oleh pelanggan, sehingga saldonya tetap dan ditandai untuk Anda sesuaikan secara manual.
- **Kartu hadiah yang digunakan untuk membayar pesanan yang dikembalikan** — pengembalian dana dikembalikan ke kartu terlebih dahulu, sebelum pembayaran kartu atau bank apa pun. Mengembalikan uang ke bank yang tidak pernah benar-benar dikumpulkan oleh pedagang adalah kesalahan terburuk, dan mengembalikan nilai ke sumber asalnya juga menutup jalur penipuan yang diketahui. Jika kartu asli telah kedaluarsa atau dinonaktifkan, kartu pengganti diterbitkan ke penerima yang sama tanpa tanggal kedaluarsa.
- **Pengembalian dana penuh** — Kreditkan jumlah kembali ke saldo kartu hadiah melalui transaksi pengembalian dana

## Tips

Jaga semua format markdown, jalur gambar, blok kode, dan istilah teknis.

- Gunakan penerbitan manual untuk kredit baik hati, penyelesaian layanan pelanggan, atau kasus apa pun di mana Anda ingin memberikan kredit toko kepada pelanggan tanpa pembelian di toko.
- Tetapkan periode kedaluwarsa yang masuk akal (misalnya, 365 hari) untuk mematuhi regulasi kartu hadiah lokal — beberapa yurisdiksi memerlukan periode validitas minimum.
- Gunakan jenis denominasi "Keduanya" untuk menawarkan kemudahan (jumlah yang ditetapkan) dan fleksibilitas (jumlah kustom).
- Pantau secara teratur metrik Total Balance — ini mewakili kewajiban yang masih terbuka di buku Anda.
- Kartu digunakan dengan cara yang sama secara online dan secara langsung — di checkout web pada langkah pembayaran, atau di kasir.

Email pengiriman mencakup tautan untuk memeriksa saldo yang dapat digunakan penerima kapan saja.
- Jika Anda menjual kepada pelanggan di beberapa negara, Anda dapat menerbitkan kartu hadiah dalam mata uang tertentu — lihat topik bantuan **Gift Cards Multi-Mata Uang** untuk detailnya.