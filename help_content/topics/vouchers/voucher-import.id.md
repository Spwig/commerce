---
title: Impor Voucher dalam Batch
---

Wizard impor voucher memungkinkan Anda membuat ratusan kode voucher sekaligus dengan mengunggah spreadsheet CSV atau XLSX. Ini ideal ketika Anda memiliki kode yang sudah dicetak sebelumnya, kode program loyalitas dari sistem pihak ketiga, atau sekadar ingin meluncurkan kampanye besar tanpa menambahkan setiap kode secara manual.

![Daftar voucher dengan tombol Impor](/static/core/admin/img/help/voucher-import/voucher-list-import-button.webp)

## Memulai impor

Navigasikan ke **Pemasaran > Voucher** dan klik tombol **Impor** di area kanan atas halaman. Ini akan membuka wizard impor tiga langkah.

## Langkah 1: Unggah file Anda dan atur pengaturan batch

![Form unggah impor](/static/core/admin/img/help/voucher-import/import-upload.webp)

Halaman pertama memiliki dua bagian: unggah file dan pengaturan diskon batch.

### Menyiapkan file Anda

Unggah file `.csv` atau `.xlsx` hingga 5 MB. File harus memiliki baris header sebagai baris pertama. Persyaratan minimum adalah satu kolom yang berisi kode voucher — kolom lainnya bersifat opsional.

Importer mengenali nama kolom umum secara otomatis. Jika file Anda menggunakan nama-nama berikut, Spwig akan memilih peta yang benar secara otomatis di halaman berikutnya tanpa klik tambahan:

| Nama kolom Anda | Dipetakan ke |
|-----------------|-------------|
| `code`, `voucher_code`, `coupon_code`, `promo_code` | Kode voucher |
| `name`, `title`, `campaign` | Nama internal |
| `description`, `details`, `note` | Deskripsi yang ditujukan ke pelanggan |
| `external_id`, `member_id`, `reference` | ID eksternal |

**Tips:** Unduh template XLSX terlebih dahulu (lihat [Mengekspor voucher sebagai template](#exporting-vouchers-as-a-template) di bawah) — template ini menggunakan nama kolom yang tepat yang diharapkan oleh importer, sehingga pemetaan kolom menjadi otomatis.

### Batas file

- Ukuran file maksimum: **5 MB**
- Jumlah baris maksimum per impor: **5.000 kode**

### Mengatur pengaturan diskon batch

Setiap voucher dalam batch akan berbagi pengaturan diskon yang sama yang Anda konfigurasikan di halaman ini. Isi bidang-bidangnya seperti saat Anda membuat satu voucher:

**Bagian diskon**

| Bidang | Deskripsi |
|-------|-------------|
| **Jenis diskon** | Persentase, Jumlah Tetap, atau Pengiriman Gratis |
| **Nilai diskon** | Persentase (0–100) atau jumlah tetap yang akan dikurangi |
| **Nilai diskon maksimum** | Batas opsional untuk diskon persentase (misalnya, batasi diskon 20% hingga $50) |
| **Cakupan penerapan** | Seluruh Keranjang, Produk Tertentu, atau Kategori Tertentu |

**Bagian validitas**

| Bidang | Deskripsi |
|-------|-------------|
| **Tanggal mulai** | Kapan kode menjadi aktif (default ke sekarang jika dibiarkan kosong) |
| **Tanggal akhir** | Kapan kode berakhir (biarkan kosong untuk tidak berakhir) |
| **Jumlah hari valid** | Alternatif untuk tanggal akhir — kode berakhir setelah jumlah hari ini sejak pembuatan |

**Bagian batas penggunaan**

| Bidang | Deskripsi |
|-------|-------------|
| **Jumlah penggunaan total maksimum** | Total penarikan yang diizinkan untuk semua pelanggan (kosong = tidak terbatas) |
| **Jumlah penggunaan per pelanggan maksimum** | Berapa kali satu pelanggan dapat menggunakan kode dari batch ini |
| **Nilai pesanan minimum** | Nilai total keranjang minimum yang diperlukan sebelum kode diterapkan |

**Keterbatasan**

Pilih kombinasi apa pun dari:
- **Tidak dapat diterapkan pada barang diskon** — mencegah kode dari tumpuk dengan produk yang sudah didiskon
- **Tidak dapat dikombinasikan dengan voucher lain** — mencegah pelanggan menggunakan dua kode pada pesanan yang sama
- **Tidak dapat dikombinasikan dengan barang diskon** — mirip dengan di atas tetapi ditujukan pada barang harga diskon
- **Hanya untuk pelanggan baru** — membatasi kode hanya untuk pelanggan tanpa pesanan sebelumnya yang selesai
- **Aktif segera** — biarkan dicentang untuk membuat kode langsung aktif saat mereka diimpor

Ketika Anda puas dengan pengaturan, klik **Lanjutkan ke pratinjau**.

## Langkah 2: Peta kolom dan tinjau

![Halaman peta kolom dan pratinjau](/static/core/admin/img/help/voucher-import/import-preview.webp)

Halaman pratinjau menampilkan empat penghitung ringkasan di bagian atas:

- **Baris yang diparse** — total baris data yang ditemukan dalam file Anda

- **Akan diimpor** — kode baru yang akan dibuat

- **Duplikat** — kode yang sudah ada di katalog Anda

- **Akan dilewati (tidak valid)** — baris yang ditolak karena kesalahan validasi (kode kosong, kode terlalu panjang, dll.)

### Pemetaan kolom

Tabel **Pemetaan Kolom** memungkinkan Anda memberi tahu Spwig kolom mana di file Anda yang sesuai dengan setiap bidang voucher. Spwig secara otomatis mendeteksi nama header umum (lihat tabel di atas), tetapi Anda dapat mengubah pemetaan apa pun menggunakan dropdown di setiap baris.

Hanya kolom **Kode Voucher** yang diperlukan. Bidang lainnya — **Nama Internal**, **Deskripsi yang Dilihat Pelanggan**, dan **ID Eksternal** — bersifat opsional. Jika Anda melewatkan mereka, Spwig akan menggunakan nilai default yang masuk akal (nama internal defaultnya adalah "Imported voucher {code}").

### Strategi kode duplikat

Jika ada kode di file Anda sudah ada di katalog Anda, Anda harus memilih cara menangani mereka:

| Strategi | Apa yang terjadi |

|----------|-------------|

| **Lewati duplikat** | Kode yang sudah ada tetap seperti semula. Hanya kode baru yang dibuat. |

| **Tulis ulang pengaturan** | Kode yang sudah ada diperbarui dengan pengaturan diskon dari batch ini. Kode, jumlah penggunaan, dan tanggal pembuatan mereka tetap dipertahankan. |

| **Gagalkan impor** | Seluruh impor dibatalkan jika bahkan satu duplikat ditemukan. Gunakan ini ketika Anda membutuhkan jaminan bahwa tidak ada kode yang sudah ada yang terpengaruh. |

Setiap kode duplikat yang ditemukan akan ditampilkan dalam panel yang dapat diperluas sehingga Anda dapat meninjau mereka sebelum memutuskan.

### Tabel pratinjau data

Bagian bawah halaman menampilkan 20 baris pertama dari file Anda sehingga Anda dapat memastikan pemetaan kolom terlihat benar sebelum mengonfirmasi. Baris yang cocok dengan kode yang sudah ada diberi penekanan.

Ketika semuanya terlihat benar, klik **Impor N voucher** untuk mengonfirmasi batch tersebut.

## Langkah 3: Tinjau hasil

![Halaman hasil impor](/static/core/admin/img/help/voucher-import/import-result.webp)

Setelah impor selesai, Anda akan melihat ringkasan yang menunjukkan:

- **Diimpor** — kode yang berhasil dibuat

- **Dilewati** — kode yang tidak dibuat (duplikat atau baris tidak valid)

- **Baris yang diproses** — total baris dari file Anda yang dievaluasi

- **Gagal** — baris yang mengalami kesalahan tak terduga

Klik **Lihat voucher yang diimpor** untuk membuka daftar voucher yang disaring hanya untuk kode dari batch ini, sehingga memudahkan Anda untuk memeriksa hasil atau mengaktifkan secara massal kode baru.

Jika ada yang terlihat salah — misalnya jenis diskon yang salah diterapkan — Anda dapat menggunakan strategi **Tulis ulang pengaturan** pada impor ulang untuk memperbaiki batch tanpa harus menghapus dan membuat ulang kode tersebut.

Klik **Impor batch lain** untuk memulai unggah baru, atau **Kembali ke daftar voucher** untuk kembali ke katalog lengkap Anda.

## Mengekspor voucher sebagai template

Daftar voucher mendukung aksi ekspor XLSX yang menghasilkan file dalam urutan kolom yang persis sama yang diharapkan oleh importer. Ini adalah cara termudah untuk mendapatkan template yang benar formatnya:

1. Navigasikan ke **Pemasaran > Voucher**

2. Pilih voucher yang ingin Anda ekspor (atau pilih semua)

3. Pilih **Ekspor voucher yang dipilih ke XLSX** dari dropdown **Aksi**

4. Klik **Go**

File yang diunduh memiliki semua 21 kolom yang dipahami oleh importer, termasuk bidang yang bersifat level batch dalam wizard impor (jenis diskon, tanggal, batas penggunaan, dll.). Anda dapat menggunakan file ini sebagai referensi atau mengirim ulang kode yang sudah ada melalui siklus edit → impor ulang menggunakan strategi **Tulis ulang pengaturan**.

## Tips

Pertahankan semua format markdown, jalur gambar, blok kode, dan istilah teknis.

- Unduh ekspor XLSX terlebih dahulu untuk digunakan sebagai template — nama kolomnya sudah diformat sebelumnya sehingga pemetaan otomatis dapat mengenali mereka tanpa perubahan apa pun di halaman pratinjau.
- Jalankan batch uji kecil dengan 5–10 kode sebelum mengimpor ratusan untuk memverifikasi pemetaan kolom dan pengaturan batch Anda sudah benar.
- Gunakan **Days valid** daripada **End date** tetap ketika kode akan didistribusikan secara bertahap — masa berlaku setiap kode kemudian dihitung dari saat kode tersebut diimpor, bukan dari tanggal kalender tunggal.
- Jika Anda menerima kode dari sistem loyalitas pihak ketiga, peta referensi anggota atau pelanggan pemasok ke kolom **External ID** sehingga Anda dapat menyelesaikan pembatalan penggunaan nanti.
- Setelah mengimpor secara besar-besaran, klik **View imported vouchers** di halaman hasil untuk menyaring daftar hanya ke batch baru — Anda kemudian dapat mengedit secara massal, mengaktifkan, atau menonaktifkan mereka sebagai kelompok.
- Impor yang gagal (menggunakan strategi duplikat **Fail**) tidak mengubah katalog Anda, sehingga aman untuk memperbaiki file dan mencoba kembali sebanyak yang diperlukan.