---
title: Produk yang Dapat Dipesan
---

Produk yang dapat dipesan memungkinkan pelanggan untuk memesan tanggal dan waktu tertentu saat mereka membeli. Ini mendukung janji temu, sewa, kelas, acara, dan pemesanan akomodasi — semua dikelola langsung dari admin Spwig Anda.

## Jenis Pemesanan

| Jenis | Terbaik Untuk |
|------|----------|
| **Janji Temu** | Layanan: konsultasi, potong rambut, pelatihan pribadi |
| **Sewa** | Sewa peralatan, sewa kendaraan, sewa ruangan |
| **Kelas / Workshop** | Sesi kelompok dengan kapasitas tetap |
| **Akomodasi** | Penginapan multi-malam dengan waktu check-in/check-out |
| **Acara** | Acara satu kali atau berulang yang diberi tiket |

## Menyiapkan Produk yang Dapat Dipesan

### Langkah 1: Membuat Produk

1. Navigasikan ke **Produk > Semua Produk** dan klik **+ Tambah Produk**
2. Atur **Jenis Produk** menjadi **Produk Pemesanan**
3. Lengkapi bidang produk standar (nama, deskripsi, harga)
4. Simpan produk

### Langkah 2: Mengatur Pengaturan Pemesanan

Setelah disimpan, bagian **Konfigurasi Pemesanan** muncul di formulir edit produk. Isi pengaturan pemesanan:

#### Jenis dan Durasi Pemesanan

- **Jenis Pemesanan** — Pilih jenis yang paling cocok dengan layanan Anda (Janji Temu, Sewa, Kelas, dll.)
- **Jenis Durasi** — Pilih **Durasi Tetap** untuk sesi dengan durasi tetap, atau **Pelanggan Memilih Durasi** untuk memungkinkan pelanggan memilih seberapa lama mereka membutuhkan
- **Durasi** dan **Satuan Durasi** — Tetapkan panjangnya (misalnya, `60` menit, `1` jam, `2` hari)
- **Durasi Minimum/Maksimum** — Jika pelanggan dapat memilih durasi, tetapkan rentang yang diizinkan

#### Waktu Buffer

Waktu buffer ditambahkan secara otomatis antara pemesanan untuk memungkinkan persiapan atau pembersihan:
- **Buffer Sebelum** — Menit yang disisihkan sebelum pemesanan dimulai
- **Buffer Setelah** — Menit yang disisihkan setelah pemesanan selesai

Contoh, janji temu pijat 60 menit dengan buffer 15 menit setelahnya memberikan 15 menit untuk mempersiapkan pelanggan berikutnya.

#### Jendela Pemesanan Awal

- **Pemberitahuan Awal Minimum** — Seberapa jauh sebelumnya pelanggan harus memesan (misalnya, `24 jam` sehingga pemesanan hari yang sama tidak diperbolehkan)
- **Jendela Maksimum Awal** — Seberapa jauh di masa depan pelanggan dapat memesan (misalnya, `365 hari`)

#### Kapasitas

- **Maksimal Pemesanan Per Slot** — Untuk kelas dan acara, tetapkan jumlah pelanggan yang dapat memesan slot waktu yang sama. Tetapkan ke `1` untuk janji temu pribadi.

#### Konfirmasi

- **Memerlukan Konfirmasi Manual** — Saat dicentang, pemesanan tidak dikonfirmasi secara otomatis. Anda harus menyetujui setiap pemesanan secara manual dari daftar pemesanan. Berguna ketika Anda ingin memverifikasi pelanggan sebelum mengonfirmasi.

#### Kebijakan Pembatalan

- **Pembatalan Diperbolehkan** — Apakah pelanggan dapat membatalkan pemesanan mereka
- **Batas Waktu Pembatalan** — Seberapa banyak jam/hari sebelum pemesanan pelanggan dapat membatalkan (misalnya, `24 jam`)

#### Tampilan Kalender

Bagaimana pelanggan memilih tanggal dan waktu mereka di halaman produk:

| Mode Tampilan | Terbaik Untuk |
|-------------|----------|
| **Tampilan Kalender** | Penggunaan umum — kalender bulan penuh |
| **Pemilih Tanggal** | Pemilihan tanggal tunggal yang sederhana |
| **Dropdown Tanggal Tersedia** | Produk dengan slot ketersediaan terbatas |
| **Pemilih Rentang Tanggal** | Akomodasi dan sewa multi-hari |

#### Deposit

Untuk meminta deposit saat checkout alih-alih pembayaran penuh:
1. Centang **Deposit Diaktifkan**
2. Atur **Jenis Deposit** menjadi **Jumlah Tetap** atau **Persentase dari Total**
3. Masukkan **Jumlah Deposit** (misalnya, `50` untuk $50, atau `25` untuk 25%)

#### Pengaturan Khusus Akomodasi

Untuk pemesanan akomodasi, bidang tambahan muncul:
- **Waktu Check-in** dan **Waktu Check-out** — Waktu standar untuk properti
- **Kapasitas Standar** — Jumlah tamu default yang termasuk dalam harga dasar

### Langkah 3: Menambahkan Sumber Pemesanan (Opsional)

Sumber adalah barang fisik atau staf yang ditugaskan ke pemesanan — contohnya, "Kamar 1", "Lapangan A", atau "Instruktur Sam".

1. Di formulir edit produk, pergi ke bagian **Sumber Pemesanan**
2. Klik **Tambahkan Sumber**
3. Beri sumber nama dan atur **Kapasitasnya** (berapa banyak pemesanan yang dapat ditangani secara bersamaan)
4. Secara opsional tambahkan gambar sumber


Sumber daya memungkinkan Anda melacak ketersediaan per aset atau anggota staf individu, bukan hanya per slot waktu.

### Langkah 4: Tetapkan aturan ketersediaan

Aturan ketersediaan mendefinisikan kapan pemesanan dapat dilakukan:

1. Di bawah bagian **Ketersediaan** produk, klik **Tambahkan Aturan Ketersediaan**
2. Pilih **Sumber Daya** yang berlaku untuk aturan ini
3. Tetapkan **Hari dalam Minggu** saat pemesanan tersedia
4. Tetapkan **Waktu Mulai** dan **Waktu Akhir** untuk jendela ketersediaan
5. Secara opsional, tetapkan rentang tanggal (**Valid From** / **Valid Until**) untuk ketersediaan musiman
6. Simpan

## Melihat dan mengelola pemesanan

### Daftar pemesanan

Beralih ke **Catalog > Bookings** untuk melihat semua pemesanan. Anda dapat menyaring berdasarkan:
- Status (Pending Confirmation, Confirmed, Cancelled, Completed, No Show)
- Produk
- Rentang tanggal

### Status pemesanan

| Status | Arti |
|--------|---------|
| **Pending Confirmation** | Menunggu persetujuan manual (jika konfirmasi diperlukan) |
| **Confirmed** | Pemesanan telah dikonfirmasi dan aktif |
| **Cancelled** | Pemesanan dibatalkan oleh pelanggan atau Anda |
| **Completed** | Tanggal pemesanan telah lewat dan telah dipenuhi |
| **No Show** | Pelanggan tidak hadir |

### Mengonfirmasi pemesanan yang menunggu konfirmasi

1. Buka pemesanan dari **Catalog > Bookings**
2. Ubah **Status** menjadi **Confirmed**
3. Simpan — pelanggan secara otomatis menerima email konfirmasi

### Membatalkan pemesanan

1. Buka pemesanan
2. Ubah **Status** menjadi **Cancelled**
3. Masukkan **Alasan Pembatalan** (ditampilkan dalam email pelanggan)
4. Simpan

## Mengelola daftar tunggu

Ketika slot waktu penuh, pelanggan dapat menambahkan diri mereka ke daftar tunggu. Spwig secara otomatis memberi tahu pelanggan yang berada dalam daftar tunggu ketika pembatalan menciptakan slot yang tersedia.

### Melihat daftar tunggu

Beralih ke **Catalog > Booking Waitlist** untuk melihat semua entri daftar tunggu. Setiap entri menampilkan:
- Nama dan email pelanggan
- Produk dan tanggal yang diinginkan
- Status: **Waiting**, **Notified**, **Converted to Booking**, atau **Expired**

### Status daftar tunggu

| Status | Arti |
|--------|---------|
| **Waiting** | Pelanggan sedang dalam antrian, slot belum tersedia |
| **Notified** | Pelanggan telah dikirimkan email tentang slot yang tersedia |
| **Converted to Booking** | Pelanggan mengambil slot dan menyelesaikan pemesanan |
| **Expired** | Tanggal yang diinginkan telah lewat tanpa slot yang tersedia |

### Memberi tahu pelanggan dalam daftar tunggu secara manual

Jika Anda ingin menghubungi pelanggan dalam daftar tunggu tertentu sebelum notifikasi otomatis:
1. Buka entri daftar tunggu
2. Salin alamat email mereka dan hubungi secara langsung
3. Setelah mereka menyelesaikan pemesanan, status entri daftar tunggu mereka diperbarui menjadi **Converted to Booking**

## Tips

- Aktifkan konfirmasi manual untuk pemesanan bernilai tinggi (misalnya, sesi fotografi, acara pribadi) sehingga Anda dapat memeriksa ketersediaan dan memenuhi kebutuhan sebelum menyetujui.
- Tetapkan waktu buffer secara generous saat memulai — Anda selalu dapat menguranginya setelah memahami kebutuhan penyelesaian nyata.
- Untuk kelas kelompok, tetapkan **Max Bookings Per Slot** ke kapasitas kelas dan aktifkan daftar tunggu sehingga sesi populer secara otomatis membangun antrian.
- Gunakan mode pemilihan rentang tanggal untuk produk akomodasi — pelanggan mengharapkan memilih tanggal kedatangan dan keberangkatan bersama.
- Tetapkan pemberitahuan minimum sebelumnya untuk mencegah pemesanan terakhir menit jika Anda membutuhkan waktu persiapan (misalnya, minimum 48 jam untuk pesanan catering khusus).
- Periksa daftar tunggu Anda secara teratur selama musim sibuk — pendekatan manual ke pelanggan dalam daftar tunggu dapat mengisi pembatalan lebih cepat daripada notifikasi otomatis.