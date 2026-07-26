---
title: Token API
---

Token API adalah kunci aman yang memungkinkan layanan eksternal dan integrasi berkomunikasi dengan toko Anda. Ketika layanan pihak ketiga atau alat memerlukan akses ke data toko Anda atau memicu tindakan, ia mengirimkan token API bersama setiap permintaan agar toko Anda dapat memverifikasi bahwa permintaan tersebut telah disetujui. Anda menciptakan dan mengelola semua token, termasuk bagian toko mana saja yang dapat diakses oleh token tersebut, dari bagian Token API di admin Anda.

## Kapan Anda memerlukan token API

Anda biasanya memerlukan membuat token API ketika:

- Menghubungkan layanan eksternal atau alat otomatisasi yang memerlukan membaca dari atau menulis ke toko Anda
- Menyiapkan penerima webhook yang memerlukan otentikasi terhadap panggilan masuk
- Mengkonfigurasi Sistem Bantuan Spwig untuk instalasi Anda
- Membangun integrasi khusus menggunakan API Spwig
- Menyinkronkan data antara toko Spwig Anda dan sistem lain

Setiap integrasi sebaiknya memiliki token sendiri agar Anda dapat membatalkan akses untuk satu layanan tanpa memengaruhi layanan lain.

## Jenis token

Ketika membuat token, Anda memilih jenis yang menggambarkan tujuannya. Jenis ini untuk referensi Anda dan membantu Anda melacak apa yang dilakukan setiap token.

| Jenis | Tujuan |
|------|---------|
| **Sistem Bantuan** | Digunakan oleh sistem dokumentasi bantuan Spwig |
| **Integrasi Eksternal** | Layanan pihak ketiga, alat otomatisasi (misalnya, Zapier), atau alat sinkronisasi data |
| **Webhook** | Otentikasi untuk penerima webhook atau akhir titik |
| **Khusus** | Tujuan lain apa pun yang tidak cocok dengan kategori di atas |
| **Sinkronisasi Instansi** | Sinkronisasi antara instalasi Spwig atau layanan Spwig eksternal |

## Cakupan API: mengontrol bagian mana yang dapat diakses oleh token

Setiap token juga memiliki bagian **Cakupan API** yang menentukan secara tepat bagian mana dari toko Anda yang diperbolehkan untuk dipanggil. Sebaliknya dari token memiliki akses penuh ke segala sesuatu, Anda memberikan akses satu area pada satu waktu—dan pada tingkat yang sebenarnya dibutuhkan oleh integrasi.

**Token tanpa cakupan yang dipilih tidak dapat mengakses API apa pun**, bahkan jika token tersebut secara lain aktif dan valid. Ini adalah pengaturan default untuk token baru, sehingga integrasi tidak akan berfungsi sampai Anda secara sengaja memberikan akses kepadanya.

Untuk setiap cakupan, Anda memilih salah satu dari tiga tingkat akses:

| Tingkat Akses | Apa yang diizinkan |
|--------------|-----------------|
| **Tidak ada akses** | Token tidak dapat memanggil endpoint apa pun di area ini |
| **Baca** | Token dapat mengambil data dari area ini, tetapi tidak dapat mengubah apa pun |
| **Baca & Tulis** | Token dapat mengambil data dan juga menciptakan, memperbarui, atau menghapusnya |

Cakupan dikelompokkan untuk cocok dengan area admin Anda:

| Kelompok | Cakupan | Tersedia Baca & Tulis? | Memberi akses ke |
|-------|-------|:---:|-------------------|
| Analitik | **Analitik Penjualan** | Hanya Baca | Dashboard penjualan, KPI, analitik produk/pelanggan/kategori, perbandingan dan ekspor |
| Analitik | **Analitik Web** | Hanya Baca | Analitik pengunjung dan lalu lintas: ringkasan, tren, halaman teratas, geografi dan pengarah |
| Katalog | **Produk** | Ya | Produk, variasi, gambar, penyesuaian stok dan penugasan atribut |
| Katalog | **Kategori** | Ya | Kategori produk, termasuk gambar dan banner |
| Katalog | **Merek** | Ya | Merek produk |
| Katalog | **Atribut** | Ya | Definisi atribut produk |
| Katalog | **Stok** | Ya | Dashboard stok, kecepatan stok, pergerakan, saran pembelian ulang dan pengaturan stok |
| Pesanan | **Pesanan** | Ya | Pesanan, catatan pesanan, pembaruan status/tracking, pembatalan, pengembalian dan dokumen pesanan |
| Pelanggan | **Pesan Pelanggan** | Ya | Pesan pelanggan dari formulir kontak dan catatan pesanan, termasuk pembaruan status dan balasan |
| Toko & Pengaturan | **Pengaturan Toko** | Ya | Pengaturan toko, bahasa yang tersedia dan branding (nama, warna, logo) |
| Pengguna & Akses | **Staf & Peran** | Ya | Akun staf, undangan, peran dan katalog izin |

Dua cakupan **Analitik** selalu hanya baca—data pelaporan tidak memiliki konsep "tulis", sehingga pemilih hanya menawarkan **Tidak ada akses** atau **Baca** untuk mereka.

[![Pemilih Ruang Lingkup API, dengan catatan akses di atas kelompok ruang lingkup Analitik dan Katalog](/static/core/admin/img/help/api-tokens/api-token-scope-picker.webp)]

Di bawah pemilih ruang lingkup, ringkasan **"Token ini dapat mengakses:"** yang hanya dapat dibaca akan menampilkan setiap ruang lingkup yang telah Anda berikan beserta tingkatnya, sehingga Anda dapat memeriksa kembali akses token secara cepat tanpa perlu mendekode pemilih tersebut.

![Ringkasan "Token ini dapat mengakses" yang menampilkan setiap ruang lingkup yang diberikan beserta tingkat Baca atau Baca & Tulis](/static/core/admin/img/help/api-tokens/api-token-scope-summary.webp)

### Hak akses yang sebenarnya digunakan oleh token

Ruang lingkup token menggambarkan *batas* dari apa yang dapat dilakukan oleh token — tetapi token juga mewarisi hak akses dunia nyata dari staf yang menciptakannya:

- Token tidak pernah dapat bertindak dengan kekuatan **superuser**, bahkan jika staf yang menciptakannya adalah superuser.
- **Baca & Tulis** pada ruang lingkup hanya berfungsi jika peran staf yang menciptakannya juga memperbolehkan akses tulis ke area tersebut. Jika peran mereka hanya untuk melihat, misalnya, Produk, token yang mereka buat dengan "Produk: Baca & Tulis" tetap hanya dapat membaca — peran bertindak sebagai pintu kedua di atas ruang lingkup.
- Jika staf yang menciptakan token dihapus atau akunnya dinonaktifkan, token segera kehilangan akses API, terlepas dari ruang lingkupnya — tidak ada lagi pengguna yang diperbolehkan untuk bertindak sebagai token tersebut.

Ini berarti cara teraman untuk membatasi ruang lingkup token adalah dengan menciptakannya saat Anda masuk sebagai staf yang perannya sudah sesuai dengan akses yang ingin dimiliki oleh token tersebut.

## Membuat Token API

1. Navigasikan ke **Pengaturan > Token API**
2. Klik **+ Tambahkan Token API**
3. Masukkan **Nama** yang jelas menggambarkan tujuan token (misalnya, `Zapier Synchronisasi Produk` atau `API Sistem Bantuan`)
4. Pilih **Jenis Token** yang sesuai
5. Secara opsional tambahkan **Deskripsi** dengan detail tambahan tentang integrasi
6. Di **Ruang Lingkup API**, pilih **Tidak ada akses**, **Baca**, atau **Baca & Tulis** untuk setiap area yang dibutuhkan oleh integrasi — biarkan semua ruang lingkup lain tetap pada **Tidak ada akses**
7. Konfigurasikan status **Aktif**, **Tanggal Kadaluarsa**, dan **IP yang Diperbolehkan** sesuai kebutuhan (lihat di bawah)
8. Klik **Simpan**

Setelah disimpan, nilai token lengkap ditampilkan pada halaman detail. **Salin segera** — token akan disembunyikan dalam tampilan daftar untuk keamanan dan tidak dapat diambil kembali secara utuh setelah Anda meninggalkan halaman ini.

![Detail Token API](/static/core/admin/img/help/api-tokens/api-token-detail.webp)

## Keamanan Nilai Token

Spwig hanya menampilkan nilai token lengkap sekali: segera setelah Anda menyimpan token baru. Setelah itu, tampilan daftar hanya menampilkan versi yang terkunci (misalnya, `spw_••••••••••••••••••••3f8a`).

Jika Anda kehilangan nilai token, Anda tidak dapat memulihkannya. Anda harus menghapus token lama dan membuat token baru, lalu memperbarui integrasi yang menggunakan token tersebut.

**Jangan pernah berbagi nilai token dalam email, pesan chat, atau kode sumber.** Anggap mereka seperti kata sandi.

## Menetapkan tanggal kadaluarsa

Bidang **Berakhir Pada** menetapkan tanggal dan waktu setelah itu token akan berhenti berfungsi secara otomatis. Biarkan kosong untuk token yang tidak boleh berakhir.

Tanggal kadaluarsa berguna untuk:

- Integrasi sementara dengan tanggal akhir tetap
- Token yang diberikan kepada pihak ketiga di mana Anda ingin penghapusan akses otomatis
- Menambahkan lapisan keamanan tambahan untuk integrasi dengan privasi tinggi

Ketika token berakhir, permintaan yang menggunakan token tersebut akan ditolak. Anda dapat memperpanjang akses dengan memperbarui tanggal **Berakhir Pada** atau membuat token pengganti.

## Membatasi ke alamat IP tertentu

Bidang **IP yang Diperbolehkan** menerima daftar alamat IP. Ketika daftar tidak kosong, token hanya berfungsi ketika permintaan berasal dari salah satu alamat tersebut.

Misalnya, jika alat analitik Anda berjalan di server `203.0.113.42`, menambahkan alamat IP tersebut berarti token tidak dapat disalahgunakan dari lokasi lain, bahkan jika token tersebut bocor.

Biarkan **IP yang Diperbolehkan** kosong untuk memungkinkan permintaan dari alamat IP mana pun.

**Kadaluarsa dan pembatasan IP diperiksa secara independen dari cakupan.** Token yang sudah kedaluwarsa atau tidak ada dalam daftar izin akan ditolak sebelum cakupannya bahkan dipertimbangkan, dan token dengan cakupan yang luas tetap ditolak begitu token tersebut kedaluwarsa atau dipanggil dari IP yang tidak terdaftar.

## Memanggil API dengan token

Integrasi mengautentikasi ke API admin Spwig dengan mengirimkan token dalam header `Authorization`:

```
Authorization: Bearer <your-token-value>
```

Setiap endpoint API admin berada di bawah `/api/admin/...`. Pengembang yang membangun integrasi Anda memutuskan endpoint mana yang akan dipanggil — tugas Anda sebagai merchant adalah memastikan **Cakupan API** token mencakup endpoint tersebut. Jika permintaan ditolak dengan kesalahan izin, hal pertama yang perlu diperiksa adalah apakah token tersebut diberi cakupan yang benar pada tingkat akses yang benar.

### Contoh: membaca analitik lalu lintas web

Spwig menyediakan endpoint `GET /api/admin/analytics/traffic/` yang mengembalikan analitik lalu lintas dan pengunjung toko Anda — gambaran tentang kunjungan dan pengunjung unik, tren seiring waktu, halaman teratas, geografi pengunjung, dan sumber rujukan. Untuk memungkinkan alat pelaporan atau dashboard membaca data ini:

1. Buat token (atau edit token yang sudah ada) untuk integrasi tersebut
2. Di **Cakupan API**, atur **Analitik Web** menjadi **Baca**
3. Simpan token dan berikan kepada integrasi

Karena **Analitik Web** adalah cakupan hanya baca, tidak ada opsi "Baca & Tulis" yang dapat dipilih — integrasi hanya dapat mengambil data analitik, tidak pernah mengubah konfigurasi toko Anda.

## Memantau penggunaan token

Daftar token menampilkan:

- **Jumlah Penggunaan** — jumlah total kali token digunakan
- **Terakhir Digunakan** — kapan token terakhir digunakan untuk membuat permintaan

Field-field ini membantu Anda mengidentifikasi token yang tidak digunakan (kandidat untuk pencabutan) dan mendeteksi aktivitas yang tidak terduga. Lonjakan tiba-tiba dalam jumlah penggunaan mungkin menunjukkan token tersebut digunakan oleh pihak lain selain integrasi yang dimaksud.

## Mencabut token

Untuk segera menghentikan token dari bekerja tanpa menghapusnya:

1. Klik nama token
2. Hilangkan centang **Aktif**
3. Simpan

Token tetap ada dalam daftar Anda untuk referensi tetapi akan ditolak pada permintaan berikutnya. Ini berguna ketika Anda perlu sementara menangguhkan integrasi sementara menyelidiki masalah.

Untuk menghapus token secara permanen:

1. Pilih kotak centangnya dalam daftar
2. Pilih **Hapus token API yang dipilih** dari menu aksi
3. Konfirmasi penghapusan

Setelah dihapus, token tidak dapat dipulihkan. Jika integrasi masih membutuhkan akses, buat token baru dan perbarui konfigurasi integrasi.

## Contoh: mengatur integrasi Zapier

**Skenario:** Anda ingin menghubungkan toko Anda ke Zapier untuk mengotomatisasi notifikasi pesanan.

| Field | Value |
|-------|-------|
| Name | `Zapier Order Automation` |
| Token Type | External Integration |
| Description | Digunakan oleh Zapier untuk membaca pesanan baru dan memicu notifikasi |
| API Scopes | **Orders**: Read & Write |
| Active | Yes |
| Expires At | *(biarkan kosong)* |
| Allowed IPs | *(biarkan kosong — Zapier menggunakan IP dinamis)* |

Hanya cakupan **Orders** yang diberikan, sehingga bahkan jika token ini terungkap, tidak akan memengaruhi produk, pesan pelanggan, akun staf, atau bagian lain dari toko Anda. Setelah disimpan, salin nilai token lengkap dan tempelkan ke pengaturan integrasi Spwig di Zapier.

- Beri setiap token nama yang jelas dan spesifik — `Shopify Sync v2` jauh lebih berguna daripada `Token 3` ketika Anda sedang menyelesaikan masalah bulan-bulan kemudian
- Buat satu token per integrasi — jika sebuah integrasi terancam, Anda dapat membatalkan hanya token tersebut tanpa mengganggu integrasi lainnya
- **Berikan hanya cakupan (scope) yang benar-benar dibutuhkan oleh integrasi** — alat pelaporan hanya membutuhkan akses Baca terhadap Analitik Penjualan atau Analitik Web, bukan Baca & Tulis pada Produk atau Staf & Peran
- Periksa ringkasan **"This token can access:"** pada formulir perubahan sebelum menyerahkan token kepada pihak ketiga — ini adalah cara tercepat untuk memastikan Anda tidak memberikan akses lebih dari yang dimaksudkan
- Ingat bahwa akses tulis juga bergantung pada peran staf yang menciptakan token tersebut — jika sebuah cakupan menunjukkan Baca & Tulis tetapi tulisan masih gagal, periksa izin peran pengguna tersebut juga
- Tetapkan tanggal kedaluwarsa untuk token yang digunakan dalam proyek satu kali atau integrasi sementara — ini mengurangi risiko token yang terlupakan tetap aktif selamanya
- Tinjau daftar token Anda setiap beberapa bulan dan nonaktifkan token dengan tanggal **Last Used** yang tidak terduga tua, karena mungkin termasuk integrasi yang sudah tidak berjalan lagi
- Jika Anda mencurigai token telah terpapar, nonaktifkan segera, buat penggantinya, dan perbarui integrasi yang terkena sebelum mengaktifkan kembali akses