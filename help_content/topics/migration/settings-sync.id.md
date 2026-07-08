---
title: Sinkronisasi Pengaturan
---

Sinkronisasi Pengaturan memungkinkan Anda menyalin konfigurasi toko antara dua instalasi Spwig. Ini ideal untuk mempertahankan lingkungan staging dan produksi, di mana Anda mengonfigurasi dan menguji perubahan di lingkungan staging sebelum mendeploynya ke toko Anda yang aktif.

## Kapan Menggunakan Sinkronisasi Pengaturan

- **Staging ke Produksi**: Konfigurasikan pengaturan di toko staging Anda, lalu kirimkan ke produksi
- **Produksi ke Staging**: Tarik pengaturan produksi ke staging untuk memulai dengan lingkungan yang cocok
- **Backup Konfigurasi**: Tarik pengaturan dari produksi ke instance backup sebagai perlindungan

Sinkronisasi Pengaturan hanya menangani data konfigurasi -- tidak mentransfer produk, pelanggan, pesanan, atau file media. Untuk transfer data lengkap, gunakan Migrasi Sistem Penuh.

## Apa yang Dapat Disinkronkan

Sinkronisasi Pengaturan mendukung kategori berikut:

| Kelompok | Kategori |
|-------|-----------|
| **Pengaturan** | Pengaturan Situs, Pajak & Mata Uang, Tarif Pajak, Bahasa, Pengaturan Blog, Berbagi Sosial, Wilayah & Gudang Penjualan, Konfigurasi Pencarian, Bidang Kustom, Peran Staf, Analitik Pelanggan |
| **Desain** | Desain & Tema, Header/Footer/Menus |
| **Pemasok** | Email, SMS/WhatsApp, Pemasok Pembayaran, Pengiriman, Pemasok SEO, Feeds Produk, Konektor Sosial Blog, Konfigurasi POS |
| **Konten** | Halaman & Template, Posting Blog, Pengumuman, Formulir, Koleksi Produk |
| **Perdagangan** | Aturan Perdagangan (Voucher, Promosi, Keanggotaan, Langganan), Program Afiliasi, Webhook & Integrasi |

> **Catatan:** Kategori yang berisi kredensial (pemasok pembayaran, akun pengiriman, dll.) ditandai dengan ikon kunci. Kunci API dan rahasia ditransfer secara aman tetapi mungkin perlu dimasukkan kembali untuk integrasi berbasis OAuth.

## Panduan Langkah Demi Langkah

### Langkah 1: Buat Koneksi

1. Navigasikan ke **Migrasi Data > Sinkronisasi Spwig ke Spwig** di bilah sisi admin
2. Klik **Mulai Sinkronisasi Pengaturan**
3. Pilih koneksi yang disimpan atau buat yang baru:
   - Masukkan URL toko jarak jauh (misalnya, `https://staging.yourstore.com`)
   - Tempelkan token sinkronisasi yang dihasilkan di toko jarak jauh
   - Beri nama koneksi yang deskriptif
   - Tetapkan peran (Staging, Produksi, Backup, atau Lainnya)
4. Klik **Uji Koneksi** untuk memverifikasi bahwa berfungsi
5. Klik **Lanjutkan** untuk melanjutkan

### Langkah 2: Pilih Kategori dan Arah

**Arah:**
- **Tarik** -- Menyalin pengaturan dari toko terhubung ke toko ini
- **Kirim** -- Menyalin pengaturan dari toko ini ke toko terhubung

**Mode Sinkronisasi:**
- **Tambah & Perbarui** -- Menambahkan item baru dan memperbarui yang sudah ada, tetapi tidak pernah menghapus apa pun. Ini adalah opsi teraman.
- **Salinan Eksak** -- Membuat target cocok dengan sumber secara eksak, termasuk menghapus item yang ada di target tetapi tidak ada di sumber. Gunakan dengan hati-hati.

Pilih kategori yang ingin Anda sertakan, lalu klik **Lanjutkan**.

### Langkah 3: Pratinjau Perubahan

Sebelum perubahan diterapkan, Anda akan melihat pratinjau terperinci yang menunjukkan secara tepat apa yang akan ditambahkan, dimodifikasi, atau dihapus untuk setiap kategori. Periksa ini secara hati-hati.

Jika mengirim ke koneksi produksi, Anda perlu mengonfirmasi bahwa Anda memahami perubahan akan memengaruhi toko Anda yang aktif.

Klik **Mulai Sinkronisasi** ketika siap.

### Langkah 4: Pantau Kemajuan

Sinkronisasi berjalan di latar belakang. Anda dapat aman meninggalkan halaman kemajuan -- sinkronisasi akan terus berjalan.

Halaman kemajuan menampilkan:
- Persentase penyelesaian secara keseluruhan dengan estimasi waktu tersisa
- Kemajuan per kategori dengan jumlah keberhasilan/gagal
- Log aktivitas langsung yang dapat diperluas untuk output rinci

## Rollback

Setelah sinkronisasi selesai, Anda memiliki **24 jam** untuk mengembalikan perubahan. Rollback memulihkan keadaan sebelumnya dari semua pengaturan yang terpengaruh.

Untuk rollback:
1. Pergi ke **Dashboard Sinkronisasi**
2. Cari pekerjaan yang selesai
3. Klik **Rollback** dan konfirmasi

Setelah 24 jam, opsi rollback berakhir dan perubahan menjadi permanen.

## Tips

Jaga semua format markdown, jalur gambar, blok kode, dan istilah teknis.

- **Uji coba di lingkungan staging terlebih dahulu**: Selalu sinkronkan ke lingkungan staging terlebih dahulu untuk memverifikasi hasil sebelum mendorong ke produksi
- **Gunakan mode Add & Update**: Ini adalah mode yang paling aman karena tidak pernah menghapus data yang sudah ada
- **Periksa preview dengan hati-hati**: Preview perbedaan menunjukkan secara tepat apa yang akan berubah sebelum sesuatu diterapkan
- **Koneksi produksi menampilkan peringatan**: Saat mendorong ke koneksi yang ditandai sebagai Produksi, konfirmasi keamanan tambahan diperlukan