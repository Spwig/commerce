---
title: Token API
---

Token API adalah kunci aman yang memungkinkan layanan eksternal dan integrasi berkomunikasi dengan toko Anda. Ketika layanan pihak ketiga atau alat membutuhkan akses ke data toko Anda atau memicu tindakan, alat tersebut mengirimkan token API bersama setiap permintaan sehingga toko Anda dapat memverifikasi apakah permintaan tersebut sah. Anda membuat dan mengelola semua token dari bagian Token API di admin Anda.

## Kapan Anda membutuhkan token API

Anda biasanya membutuhkan membuat token API ketika:

- Menghubungkan layanan eksternal atau alat otomatisasi yang membutuhkan membaca dari atau menulis ke toko Anda
- Menyiapkan penerima webhook yang membutuhkan otentikasi panggilan masuk
- Mengonfigurasi Sistem Bantuan Spwig untuk instalasi Anda
- Membangun integrasi khusus menggunakan API Spwig
- Menyinkronkan data antara toko Spwig Anda dan sistem lain

Setiap integrasi sebaiknya memiliki token sendiri sehingga Anda dapat membatalkan akses untuk satu layanan tanpa memengaruhi layanan lainnya.

## Jenis token

Ketika membuat token, Anda memilih jenis yang menggambarkan tujuannya. Jenis ini untuk referensi Anda dan membantu Anda melacak apa yang dilakukan setiap token.

| Jenis | Tujuan |
|------|---------|
| **Sistem Bantuan** | Digunakan oleh sistem dokumentasi bantuan Spwig |
| **Integrasi Eksternal** | Layanan pihak ketiga, alat otomatisasi (misalnya, Zapier), atau alat sinkronisasi data |
| **Webhook** | Otentikasi untuk penerima webhook atau akhir titik |
| **Kustom** | Tujuan lain apa pun yang tidak cocok dengan kategori di atas |
| **Sinkronisasi Instansi** | Sinkronisasi antara instalasi Spwig atau layanan Spwig eksternal |

## Membuat token API

1. Navigasi ke **Pengaturan > Token API**
2. Klik **+ Tambahkan Token API**
3. Masukkan **Nama** yang jelas menggambarkan tujuan token tersebut (misalnya, `Sinkronisasi Produk Zapier` atau `API Sistem Bantuan`)
4. Pilih **Jenis Token** yang sesuai
5. Secara opsional tambahkan **Deskripsi** dengan detail tambahan tentang integrasi tersebut
6. Konfigurasikan status **Aktif**, **Tanggal Kadaluarsa**, dan **IP yang Diperbolehkan** sesuai kebutuhan (lihat di bawah)
7. Klik **Simpan**

Setelah disimpan, nilai token lengkap ditampilkan di halaman detail. **Salin segera** — token tersebut ditutupi dalam tampilan daftar untuk keamanan dan tidak dapat diambil kembali secara utuh setelah Anda meninggalkan halaman ini.

![Detail Token API](/static/core/admin/img/help/api-tokens/api-token-detail.webp)

## Keamanan nilai token

Spwig hanya menampilkan nilai token lengkap sekali: segera setelah Anda menyimpan token baru. Setelah itu, tampilan daftar hanya menampilkan versi yang ditutupi (misalnya, `spw_••••••••••••••••••••3f8a`).

Jika Anda kehilangan nilai token, Anda tidak dapat memulihkannya. Anda perlu menghapus token lama dan membuat token baru, lalu memperbarui integrasi yang menggunakan token tersebut.

**Jangan pernah berbagi nilai token dalam email, pesan chat, atau kode sumber.** Anggap mereka seperti kata sandi.

## Menetapkan tanggal kadaluarsa

Bidang **Berakhir Pada** menetapkan tanggal dan waktu setelah itu token akan berhenti berfungsi secara otomatis. Biarkan kosong untuk token yang tidak boleh berakhir.

Tanggal kadaluarsa berguna untuk:

- Integrasi sementara dengan tanggal akhir tetap
- Token yang diberikan ke pihak ketiga di mana Anda ingin penghapusan akses otomatis
- Menambahkan lapisan keamanan tambahan untuk integrasi dengan privasi tinggi

Ketika token berakhir, permintaan yang menggunakan token tersebut ditolak. Anda dapat memperpanjang akses dengan memperbarui tanggal **Berakhir Pada** atau membuat token pengganti.

## Membatasi ke alamat IP tertentu

Bidang **IP yang Diperbolehkan** menerima daftar alamat IP. Ketika daftar tidak kosong, token hanya berfungsi ketika permintaan berasal dari salah satu alamat tersebut.

Misalnya, jika alat analitik Anda berjalan di server `203.0.113.42`, menambahkan alamat IP tersebut berarti token tidak dapat disalahgunakan dari lokasi lain, bahkan jika bocor.

Biarkan **IP yang Diperbolehkan** kosong untuk memungkinkan permintaan dari alamat IP apa pun.

## Memantau penggunaan token

Daftar token menampilkan:

- **Jumlah Penggunaan** — jumlah total kali token tersebut telah digunakan
- **Terakhir Digunakan** — kapan token tersebut terakhir digunakan untuk membuat permintaan

Bidang-bidang ini membantu Anda mengidentifikasi token yang tidak digunakan (kandidat untuk pembatalan) dan mendeteksi aktivitas yang tidak terduga.

Lonjakan tiba-tiba dalam jumlah penggunaan mungkin menunjukkan bahwa token tersebut digunakan oleh seseorang selain integrasi yang dimaksudkan.

## Membatalkan token

Untuk segera menghentikan token dari bekerja tanpa menghapusnya:

1. Klik nama token
2. Hilangkan centang pada **Active**
3. Simpan

Token tetap ada dalam daftar Anda untuk referensi tetapi akan ditolak pada permintaan berikutnya. Ini berguna ketika Anda perlu sementara menangguhkan integrasi sementara menyelidiki masalah.

Untuk menghapus token secara permanen:

1. Pilih kotak centangnya dalam daftar
2. Pilih **Delete selected API tokens** dari menu aksi
3. Konfirmasi penghapusan

Setelah dihapus, token tidak dapat dipulihkan. Jika integrasi masih membutuhkan akses, buat token baru dan perbarui konfigurasi integrasi.

## Contoh: mengatur integrasi Zapier

**Skenario:** Anda ingin menghubungkan toko Anda ke Zapier untuk mengotomatisasi pemberitahuan pesanan.

| Field | Value |
|-------|-------|
| Name | `Zapier Order Automation` |
| Token Type | External Integration |
| Description | Digunakan oleh Zapier untuk membaca pesanan baru dan memicu pemberitahuan |
| Active | Yes |
| Expires At | *(biarkan kosong)* |
| Allowed IPs | *(biarkan kosong — Zapier menggunakan IP dinamis)* |

Setelah disimpan, salin nilai token lengkap dan tempelkan ke pengaturan integrasi Spwig di Zapier.

## Tips

- Beri setiap token nama yang jelas dan spesifik — `Shopify Sync v2` jauh lebih berguna daripada `Token 3` ketika Anda sedang meneliti masalah beberapa bulan kemudian
- Buat satu token per integrasi — jika integrasi terkena kerusakan, Anda dapat membatalkan hanya token tersebut tanpa mengganggu integrasi lainnya
- Tetapkan tanggal kedaluwarsa untuk token yang digunakan dalam proyek satu kali atau integrasi sementara — ini mengurangi risiko token yang terlupakan tetap aktif selamanya
- Tinjau daftar token Anda setiap beberapa bulan dan nonaktifkan token dengan tanggal **Last Used** yang tidak terduga tua, karena mungkin termasuk integrasi yang tidak lagi berjalan
- Jika Anda mencurigai token telah terungkap, nonaktifkan segera, buat pengganti, dan perbarui integrasi yang terkena sebelum mengaktifkan akses kembali