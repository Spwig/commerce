---
title: Manajemen Komisi
---

Manajemen komisi adalah proses meninjau dan menyetujui pendapatan afiliasi untuk memastikan hanya penjualan yang sah yang dikreditkan. Panduan ini menunjukkan cara meninjau komisi yang menunggu, menyetujui yang valid, menolak pesanan yang curang atau dikembalikan, dan mengelola komisi secara efisien menggunakan tindakan massal.

## Panel Komisi

Buka **Pemasaran > Komisi** untuk mengakses panel manajemen komisi.

Panel ini memberikan gambaran aktivitas komisi di seluruh program afiliasi:

| Statistik | Deskripsi |
|-----------|-------------|
| **Komisi yang Menunggu** | Jumlah komisi yang menunggu tinjauan Anda |
| **Komisi yang Disetujui** | Komisi yang dikonfirmasi dan siap dibayarkan |
| **Komisi yang Dibayar** | Komisi yang telah dibayarkan ke afiliasi |
| **Komisi yang Ditolak** | Komisi yang ditolak karena penipuan, pengembalian, atau pelanggaran kebijakan |
| **Jumlah Pembayaran yang Menunggu** | Nilai total dari komisi yang disetujui tetapi belum dibayar |

Statistik ini membantu Anda melacak beban kerja tinjauan dan memantau dampak finansial program afiliasi Anda.

![Panel Komisi](/static/core/admin/img/help/commission-management/commission-dashboard.webp)

## Melihat Komisi

Daftar komisi menampilkan semua catatan komisi secara kronologis.

### Kolom Daftar

| Kolom | Deskripsi |
|--------|-------------|
| **Afiliasi** | Nama dan kode unik afiliasi |
| **Program** | Program afiliasi yang menghasilkan komisi ini |
| **Pemesanan** | Nomor pesanan (klik untuk melihat detail pesanan lengkap) |
| **Jumlah** | Nilai komisi dalam mata uang toko Anda |
| **Status** | Menunggu, Disetujui, Ditolak, atau Dibayar |
| **Dibuat** | Kapan komisi ini dihasilkan |

### Menyaring Komisi

Gunakan bilah penyaring untuk menyempitkan komisi:

- **Berdasarkan Status** — Tampilkan hanya komisi yang menunggu, disetujui, ditolak, atau dibayar
- **Berdasarkan Afiliasi** — Lihat komisi untuk mitra tertentu
- **Berdasarkan Program** — Lihat komisi dari program afiliasi tertentu
- **Berdasarkan Rentang Tanggal** — Saring berdasarkan tanggal pembuatan

### Mencari Komisi

Gunakan bilah pencarian untuk menemukan komisi tertentu:

- Masukkan **nomor pesanan** untuk menemukan komisi untuk penjualan tertentu
- Masukkan **kode afiliasi** untuk melihat semua komisi untuk satu mitra

## Detail Komisi

Klik komisi apa pun dalam daftar untuk melihat detail lengkapnya.

### Bidang Detail

Tampilan detail menampilkan:

- **Informasi Pesanan** — Klik nomor pesanan untuk melihat pesanan lengkap dalam tab baru, termasuk barang, alamat pengiriman, status pembayaran, dan detail pelanggan
- **Informasi Afiliasi** — Nama, kode, email pembayaran, dan status keanggotaan program afiliasi
- **Detail Program** — Nama program, jenis komisi (persentase atau tetap), dan tingkat komisi
- **Waktu** — Tanggal pembuatan, tanggal disetujui/ditolak, dan tanggal dibayar
- **Bagian Catatan** — Catatan internal yang hanya terlihat oleh pedagang (dijelaskan di bawah)

Informasi ini membantu Anda memverifikasi keabsahan komisi sebelum menyetujuinya.

## Menyetujui Komisi

Menyetujui komisi mengonfirmasi bahwa komisi tersebut sah dan menambahkannya ke saldo afiliasi, sehingga layak untuk pembayaran.

### Kapan Menyetujui

Setujui komisi ketika:

- **Pemesanan berhasil dipenuhi** — Produk dikirim atau barang digital dikirimkan
- **Tidak ada pengembalian atau pengembalian dana** — Pelanggan tidak meminta pengembalian (pertimbangkan menunggu 14-30 hari setelah pengiriman)
- **Standar kualitas terpenuhi** — Penjualan memenuhi syarat program (misalnya, bukan self-referral, pelanggan menggunakan metode pembayaran asli)
- **Tidak ada penipuan yang terdeteksi** — Pesanan melewati pemeriksaan penipuan (periksa IP, ketidakcocokan alamat pembayaran/pengiriman, pola pesanan yang tidak biasa)

### Cara Menyetujui

**Persetujuan Komisi Tunggal:"

1. Buka **Pemasaran > Komisi**
2. Klik komisi yang ingin disetujui
3. Klik tombol **Setujui** di bagian atas halaman detail
4. Secara opsional tambahkan catatan (misalnya, "Disetujui setelah pengiriman berhasil")
5. Status berubah menjadi **Disetujui** dan komisi ditambahkan ke saldo afiliasi

**Persetujuan Massal:"

1. Buka **Pemasaran > Komisi**
2. Centang kotak di sebelah komisi yang ingin disetujui
3. Pilih **Setujui yang Dipilih** dari dropdown **Tindakan**
4. Klik **Lanjutkan**
5. Semua komisi yang dipilih berubah menjadi status **Disetujui**

Komisi yang disetujui muncul di dashboard afiliasi sebagai saldo yang tersedia dan dapat dimasukkan ke dalam batch pembayaran berikutnya.

## Menolak Komisi

Menolak komisi menghilangkan komisi tersebut dari saldo afiliasi dan menandainya sebagai tidak layak untuk pembayaran.

### Kapan Menolak

Tolak komisi ketika:

- **Pemesanan penipuan** — Pesanan menunjukkan tanda-tanda penipuan (metode pembayaran dicuri, ketidakcocokan IP, afiliasi menggunakan tautan mereka sendiri)
- **Pelanggan mengembalikan produk** — Pelanggan mengembalikan barang untuk pengembalian dana penuh
- **Masalah kualitas** — Penjualan tidak memenuhi syarat program (misalnya, afiliasi melanggar pedoman iklan)
- **Pelanggaran syarat** — Afiliasi menggunakan metode promosi yang dilarang (spam, bidding merek, cookie stuffing)
- **Pemesanan dibatalkan** — Pelanggan membatalkan sebelum pengiriman

### Cara Menolak

**Penolakan Komisi Tunggal:"

1. Buka **Pemasaran > Komisi**
2. Klik komisi yang ingin ditolak
3. Klik tombol **Tolak** di bagian atas halaman detail
4. **Tambahkan catatan** yang menjelaskan alasan (dianjurkan untuk penyelesaian sengketa)
5. Status berubah menjadi **Ditolak**

**Penolakan Massal:"

1. Buka **Pemasaran > Komisi**
2. Centang kotak di sebelah komisi yang ingin ditolak
3. Pilih **Tolak yang Dipilih** dari dropdown **Tindakan**
4. Klik **Lanjutkan**
5. Semua komisi yang dipilih berubah menjadi status **Ditolak**

Komisi yang ditolak dihapus dari saldo afiliasi dan tidak dapat dibayarkan. Mereka tetap terlihat dalam riwayat komisi untuk catatan.

## Tindakan Massal

Tindakan massal memungkinkan Anda menyetujui atau menolak beberapa komisi sekaligus, menghemat waktu saat memproses batch besar.

### Menggunakan Tindakan Massal

1. Buka **Pemasaran > Komisi**
2. Saring daftar untuk menampilkan hanya komisi yang ingin diproses (misalnya, saring berdasarkan status **Menunggu**)
3. Centang kotak di sebelah setiap komisi, atau klik kotak header untuk memilih semua di halaman saat ini
4. Pilih tindakan dari dropdown **Tindakan**:
   - **Setujui yang Dipilih** — Tandai semua komisi yang dipilih sebagai disetujui
   - **Tolak yang Dipilih** — Tandai semua komisi yang dipilih sebagai ditolak
5. Klik **Lanjutkan**
6. Tinjau pesan konfirmasi yang menunjukkan jumlah komisi yang diperbarui

### Pemrosesan Massal yang Efisien

- **Saring berdasarkan program** — Setujui semua komisi dari afiliasi tepercaya yang berkinerja tinggi sekaligus
- **Saring berdasarkan rentang tanggal** — Proses komisi yang lebih tua dari 14 hari (melebihi jendela pengembalian Anda)
- **Tinjau secara terpisah komisi bernilai tinggi** — Gunakan tindakan massal untuk komisi kecil, tinjau secara manual komisi besar

## Catatan Komisi

Bidang catatan memungkinkan Anda mendokumentasikan keputusan Anda dan berkomunikasi dengan tim Anda.

### Menambahkan Catatan

Catatan dapat ditambahkan:

- **Selama persetujuan** — Klik komisi, tambahkan catatan di bidang Catatan, lalu klik **Setujui**
- **Selama penolakan** — Tambahkan catatan yang menjelaskan alasan penolakan
- **Kapan saja** — Klik komisi, tambahkan atau ubah catatan di bidang Catatan, dan simpan

### Kapan Menggunakan Catatan

- **Komisi yang ditolak** — Selalu dokumentasikan alasan ("Pelanggan mengembalikan pesanan #12345 pada 2/10/26")
- **Komisi bernilai tinggi** — Catat langkah verifikasi yang diambil ("Verifikasi pengiriman melalui pelacakan #ABC123")
- **Komisi yang diperdebatkan** — Dokumentasikan komunikasi dengan afiliasi
- **Polusi penipuan** — Catat aktivitas mencurigakan untuk referensi di masa depan

Catatan hanya **internal** — afiliasi tidak dapat melihatnya. Mereka berfungsi sebagai alat pencatatan Anda.

## Alur Komisi

Berikut adalah alur manajemen komisi lengkap:

```
Pemesanan Dibuat → Komisi Dibuat (Menunggu)
                      ↓
              Merchant Meninjau
                      ↓
                ┌─────┴─────┐
                ↓           ↓
            Disetujui     Ditolak
                ↓           ↓
        Siap Dibayarkan  Tidak Dapat Dibayar
                ↓
        Termasuk dalam Pembayaran
                ↓
              Dibayar
```

**Contoh Garis Waktu:"

- **Hari 1:** Pelanggan memesan $100 melalui tautan afiliasi → komisi $10 dibuat (Menunggu)
- **Hari 15:** Pesanan selesai dan jendela pengembalian berlalu → Merchant menyetujui komisi
- **Hari 20:** Merchant memproses batch pembayaran bulanan → status komisi berubah menjadi Dibayar
- **Hari 21:** Afiliasi menerima pembayaran melalui PayPal

## Praktik Terbaik

### Jendela Tinjauan

Buat jadwal tinjauan yang konsisten:

- **Tinjauan harian** — Proses komisi yang menunggu setiap pagi (dianjurkan untuk program dengan volume tinggi)
- **Tinjauan mingguan** — Alokasikan waktu setiap Senin untuk menyetujui komisi minggu sebelumnya
- **Tinjauan dua mingguan** — Sesuaikan dengan jadwal pembayaran Anda (setujui komisi di tengah bulan, proses pembayaran akhir bulan)

### Pemeriksaan Kualitas

Sebelum menyetujui komisi, verifikasi:

1. **Pemesanan telah dipenuhi** — Periksa status pesanan di admin
2. **Pembayaran telah dikonfirmasi** — Verifikasi metode pembayaran berhasil diproses
3. **Jendela pengembalian telah berlalu** — Tunggu 14-30 hari setelah pengiriman untuk mempertimbangkan pengembalian
4. **Tidak ada bendera penipuan** — Periksa pesanan untuk pola mencurigakan (alamat tidak cocok, negara berisiko tinggi, beberapa pesanan dari IP yang sama)
5. **Afiliasi dalam keadaan baik** — Periksa riwayat afiliasi untuk pelanggaran penipuan atau pelanggaran sebelumnya

### Pencegahan Penipuan

Waspada terhadap tanda merah ini:

- **Self-referrals** — Afiliasi memesan menggunakan tautan pelacakan mereka sendiri
- **Cookie stuffing** — Rasio konversi klik yang tidak normal dengan nilai pesanan rendah
- **Pemesanan duplikat** — Beberapa pesanan dari pelanggan/IP yang sama melalui tautan afiliasi yang sama
- **Ketidakcocokan geolokasi** — Afiliasi di Negara A menggerakkan penjualan eksklusif di Negara B
- **Chargebacks** — Tingkat chargeback tinggi pada pesanan yang dirujuk oleh afiliasi

Jika Anda mendeteksi penipuan, **tolak komisi tersebut** dan pertimbangkan untuk mengakhiri keanggotaan program afiliasi.

### Komunikasi dengan Afiliasi

- **Tetapkan ekspektasi** — Dokumentasikan kebijakan persetujuan komisi Anda secara jelas dalam syarat program
- **Jadilah transparan** — Jika Anda menolak komisi, pertimbangkan mengirimkan email ke afiliasi menjelaskan alasan (gunakan catatan sebagai referensi)
- **Tanggapi sengketa** — Jika afiliasi mempertanyakan penolakan, tinjau catatan dan detail pesanan
- **Publikasikan panduan** — Buat halaman "Kebijakan Persetujuan Komisi" di portal afiliasi Anda untuk menghindari kebingungan

## Tips

- Setujui komisi **setelah jendela pengembalian ditutup** (biasanya 14-30 hari) untuk menghindari menyetujui pesanan yang kemudian dikembalikan oleh pelanggan
- Gunakan **tindakan massal dengan penyaring** untuk memproses komisi dari afiliasi yang tepercaya secara efisien sambil meninjau secara manual afiliasi baru atau berisiko tinggi
- Dokumentasikan alasan penolakan di **bidang catatan** — ini melindungi Anda jika afiliasi memperdebatkan keputusan dan membantu Anda mengidentifikasi pola
- Perhatikan **self-referrals** — ini adalah pelanggaran umum di mana afiliasi menggunakan tautan mereka sendiri untuk mendapatkan komisi atas pembelian pribadi
- Tetapkan **ambang batas persetujuan minimum** — misalnya, otomatis setujui komisi di bawah $10 tetapi tinjau secara manual semua yang di atas $50 untuk menyeimbangkan efisiensi dengan risiko
- Buat **daftar periksa penipuan** — standarkan proses tinjauan Anda dengan daftar tanda merah (ketidakcocokan IP, pola pesanan mencurigakan, metode pembayaran berisiko tinggi)
- Pantau **tingkat penolakan berdasarkan afiliasi** — jika satu afiliasi memiliki banyak penolakan, mungkin menunjukkan penipuan atau kebutuhan pelatihan tambahan tentang syarat program