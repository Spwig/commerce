---
title: Migrasi Sistem Penuh
---

Migrasi Sistem Penuh memindahkan seluruh toko Anda -- pengaturan, produk, pelanggan, pesanan, file media, dan semua data lainnya -- dari satu instalasi Spwig ke instalasi lainnya. Gunakan ini saat pindah ke server baru atau membuat salinan lengkap toko Anda.

## Kapan Menggunakan Migrasi Penuh

- **Pemindahan server**: Memindahkan toko Anda ke penyedia hosting atau server baru
- **Membuat salinan staging**: Menyiapkan lingkungan staging lengkap dari produksi
- **Pemulihan bencana**: Memulihkan toko lengkap dari instance cadangan

Migrasi Penuh mencakup segala sesuatu yang dilakukan oleh Sinkronisasi Pengaturan, ditambah semua data transaksional (produk, pelanggan, pesanan, ulasan, stok, media, dll.).

## Apa yang Dikirimkan

Migrasi Penuh dapat mentransfer semua kategori pengaturan plus kategori data berikut:

| Kategori | Deskripsi |
|----------|-------------|
| **Komponen Terinstal** | Tema, integrasi penyedia, dan komponen utilitas beserta file paketnya |
| **Produk, Kategori & Merek** | Produk, variasi, gambar, kategori, merek, dan atribut |
| **Perpustakaan Media** | Semua file media yang diunggah dan aset |
| **Pelanggan & Alamat** | Akun pelanggan, profil, dan alamat |
| **Riwayat Pesanan** | Pesanan, item pesanan, dan catatan transaksi |
| **Ulasan Produk** | Ulasan dan penilaian pelanggan |
| **Tingkat Stok** | Kuantitas inventaris per gudang dan titik pesan ulang |
| **Produk Digital & Lisensi** | Aset digital, template lisensi, dan kolam lisensi |
| **Kartu Hadiah & Penggunaan Voucher** | Saldo kartu hadiah dan catatan penggunaan voucher |
| **Kredit Toko & Dompet** | Saldo dompet pelanggan dan riwayat transaksi |
| **Anggota Program Keanggotaan** | Anggota keanggotaan, poin, transaksi, dan badge |
| **Langganan Aktif** | Rencana langganan, langganan aktif, dan riwayat pembayaran |
| **Pengiriman & Pelacakan** | Catatan pengiriman dan acara pelacakan |
| **Pengembalian, Pengembalian & Catatan Pesanan** | Catatan pengembalian, permintaan pengembalian, dan catatan |
| **Anggota Afiliasi** | Akun afiliasi, kode referensi, dan riwayat komisi |

## Panduan Langkah Demi Langkah

### Langkah 1: Koneksi ke Instance Sumber

1. Navigasikan ke **Data Migration > Spwig-to-Spwig Sync** di bilah sisi admin
2. Klik **Mulai Migrasi Penuh**
3. Koneksi ke toko sumber (toko yang Anda migrasikan **dari**):
   - Masukkan URL toko sumber
   - Tempelkan token sinkronisasi dari toko sumber
   - Beri nama koneksi (misalnya, "Old Production Server")
4. Klik **Uji Koneksi** untuk memverifikasi
5. Klik **Lanjutkan**

> **Penting:** Migrasi Penuh selalu **menarik** data dari toko yang terhubung ke toko ini. Jalankan wizard di **tujuan** (toko baru).

### Langkah 2: Pilih Ruang Lingkup

Pilih kategori data mana yang akan dimasukkan dalam migrasi. Kategori dikelompokkan menjadi grup:

- **Pengaturan**: Konfigurasi toko, tema, penyedia, konten
- **Data**: Produk, pelanggan, pesanan, media, dan data transaksional lainnya

Beberapa kategori memiliki ketergantungan (misalnya, Pesanan bergantung pada Pelanggan dan Produk). Ketergantungan secara otomatis dimasukkan saat Anda memilih kategori.

Kategori dengan indikator khusus:
- **Ikon kunci**: Mengandung kredensial yang ditransfer secara aman
- **Ikon file**: Termasuk file biner (gambar, media, paket)
- **Ikon peringatan**: Pertimbangan khusus untuk lingkungan produksi

### Langkah 3: Pemeriksaan Pra-Penerapan

Sebelum migrasi dimulai, pemeriksaan pra-penerapan otomatis memverifikasi:

- **Kesehatan koneksi**: Toko sumber dapat diakses dan terautentikasi
- **Kompatibilitas versi**: Kedua toko berjalan pada versi Spwig yang kompatibel
- **Ruangan disk**: Penyimpanan yang cukup tersedia untuk file media
- **Kesiapan database**: Database tujuan dapat menerima data

Jika ada pemeriksaan yang gagal, Anda akan melihat panduan khusus tentang cara menyelesaikan masalah sebelum melanjutkan.

### Langkah 4: Kemajuan Migrasi

Migrasi berjalan di latar belakang. Anda dapat aman berpindah halaman -- proses akan terus berjalan.

Halaman progres menampilkan:
- Persentase keseluruhan dengan estimasi waktu tersisa
- Status penyelesaian per kategori
- Log aktivitas langsung dengan detail transfer
- Statistik transfer media (file dan byte yang ditransfer) untuk kategori media

Untuk toko besar dengan banyak produk dan file media, migrasi mungkin memakan waktu. Fase transfer media biasanya yang paling lama.

### Langkah 5: Hasil

Setelah migrasi selesai, halaman hasil menampilkan:

- Statistik ringkasan (item yang telah dimigrasikan, dilewati, gagal)
- Pemecahan per kategori dengan status
- Detail kesalahan untuk item yang gagal

## Daftar Pemeriksaan Pasca-Migrasi

Setelah migrasi berhasil, lengkapi langkah-langkah berikut di toko baru Anda:

1. **Aktifkan lisensi Anda** di instalasi baru
2. **Masukkan kembali kredensial penyedia pembayaran** yang dilewati selama migrasi (kunci sandbox/test tidak ditransfer ke produksi)
3. **Konfigurasikan DNS** untuk mengarahkan domain Anda ke server baru
4. **Uji alur checkout** dengan pesanan uji
5. **Verifikasi pengiriman email** berfungsi dengan benar
6. **Periksa file media** dan gambar apakah memuat dengan baik

## Rollback

Setelah migrasi penuh selesai, Anda memiliki **24 jam** untuk melakukan rollback. Rollback menghapus semua data yang telah dimigrasikan dari toko tujuan, mengembalikannya ke keadaan sebelum migrasi.

Untuk rollback:
1. Pergi ke halaman hasil atau Dashboard Sinkronisasi
2. Klik **Rollback Migration** dan konfirmasi
3. Tunggu hingga rollback selesai

> **Peringatan:** Rollback menghapus permanen semua data yang telah dimigrasikan. Perubahan apa pun yang dibuat di toko tujuan setelah migrasi (pesanan baru, pendaftaran pelanggan, dll.) juga akan terdampak.

Setelah 24 jam, opsi rollback berakhir.

## Tips

- **Lakukan di toko tujuan**: Wizard Migrasi Penuh harus dijalankan di **toko baru**, menarik data dari toko lama
- **Migrasikan ke instalasi bersih**: Untuk hasil terbaik, jalankan migrasi di instalasi Spwig yang bersih sebelum diluncurkan
- **Periksa ruang disk**: Pastikan tujuan memiliki cukup penyimpanan untuk semua file media
- **Biarkan sumber tetap berjalan**: Jangan matikan toko sumber sampai Anda memverifikasi semuanya berfungsi di tujuan
- **Rencanakan transisi DNS**: Setelah memverifikasi migrasi, perbarui catatan DNS Anda untuk mengarahkan ke server baru