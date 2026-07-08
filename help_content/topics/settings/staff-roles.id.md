---
title: Peran & Izin Staf
---

Peran staf memungkinkan Anda mengontrol secara tepat apa yang dapat dilihat dan dilakukan oleh setiap anggota tim — baik di panel admin maupun di terminal POS. Definisikan peran dengan izin tertentu, lalu berikan peran tersebut kepada anggota staf. Seorang pengguna dapat memiliki beberapa peran, dan izin efektif mereka adalah kombinasi dari semua peran yang ditugaskan.

![Peran staf](/static/core/admin/img/help/staff-roles/role-list.webp)

## Cara Kerjanya

1. Anda membuat **peran** yang mendefinisikan himpunan izin (misalnya, "Manajer Pesanan", "Kasir")
2. Setiap peran mengontrol dua jenis akses: **izin panel admin** dan **izin POS**
3. Anda **menugaskan peran** kepada anggota staf dari halaman profil mereka
4. Izin efektif seorang anggota staf adalah **gabungan** dari semua peran mereka — jika ada peran yang memberikan akses, pengguna memiliki akses tersebut
5. Izin **dikachir** untuk kinerja dan secara otomatis diperbarui saat peran berubah

## Peran Bawaan

Spwig menyertakan 7 peran bawa-in yang mencakup struktur tim yang paling umum. Peran ini tidak dapat dihapus, tetapi Anda dapat membuat peran kustom untuk kebutuhan yang lebih spesifik.

| Peran | Akses | Deskripsi |
|------|--------|-------------|
| **Pemilik Toko** | Admin + POS | Akses penuh ke semua hal. Untuk administrator utama toko. |
| **Manajer Toko** | Admin + POS | Operasi sehari-hari — akses penuh ke produk, pesanan, pelanggan, pemasaran, dan pencarian. Hanya dapat melihat desain, email, pembayaran, dan pengaturan. |
| **Editor Konten** | Admin | Mengelola halaman, posting blog, desain, dan media. Hanya dapat melihat produk. |
| **Manajer Pesanan** | Admin | Menangani pesanan, pengiriman, pengembalian, dan layanan pelanggan. Hanya dapat melihat produk. |
| **Manajer Pemasaran** | Admin | Mengelola promosi, voucher, afiliasi, loyalitas, dan program rujukan. Hanya dapat melihat produk, pelanggan, dan media. |
| **Kasir** | Hanya POS | Staf POS di garis depan. Dapat memproses penjualan dan memeriksa saldo kartu hadiah. Tidak ada diskon, pengembalian, atau manajemen uang tunai. |
| **Kasir Senior** | Hanya POS | Staf POS berpengalaman. Dapat memproses pengembalian, menerapkan diskon (sampai 25%), mengelola uang tunai, dan menutup shift. |

## Membuat Peran Kustom

Navigasikan ke **Pengaturan > Peran Staf** dan klik **Tambahkan Peran**.

### Pengaturan Umum

| Pengaturan | Deskripsi |
|---------|-------------|
| **Nama Tampilan** | Nama peran yang ditampilkan di admin (misalnya, "Staf Gudang") |
| **Deskripsi** | Penjelasan singkat tentang apa tujuan peran ini |
| **Urutan Penyortiran** | Mengontrol urutan tampilan dalam daftar peran |
| **Ikon** | Pilih dari 20 ikon untuk mengidentifikasi peran secara visual |
| **Warna Badge** | Warna yang digunakan untuk badge peran (Biru, Hijau, Oranye, Merah, Teal, Abu-abu) |
| **Panel Admin** | Toggle apakah peran ini memberikan akses ke backend admin |
| **Terminal POS** | Toggle apakah peran ini memberikan akses ke terminal POS |

### Kategori Izin Admin

Tab izin admin mengelompokkan semua fitur platform ke dalam 13 kategori. Untuk setiap kategori, Anda menetapkan salah satu dari tiga tingkat akses:

- **Tidak Ada** — Tidak ada akses ke area ini (item menu disembunyikan)
- **Lihat** — Akses hanya baca (dapat melihat data tetapi tidak mengubahnya)
- **Penuh** — Akses lengkap (dapat melihat, membuat, mengedit, dan menghapus)

![Kategori izin](/static/core/admin/img/help/staff-roles/permission-categories.webp)

| Kategori | Apa yang dikontrol |
|----------|-----------------|
| **Katalog Produk** | Produk, kategori, merek, atribut, stok, gudang, aset digital |
| **Pesanan & Penukaran** | Pesanan, pengembalian, pengembalian, pengiriman, konfigurasi pengiriman |
| **Pelanggan** | Profil pelanggan, segmen, analitik |
| **Konten & Halaman** | Halaman, posting blog, pengumuman, formulir |
| **Desain & Tema** | Tema, template header/footer, menu, token desain, CSS kustom |
| **Pemasaran & Promosi** | Promosi, voucher, afiliasi, loyalitas, rujukan, feed produk |
| **Perpustakaan Media** | Gambar, video, folder, tag |
| **Sistem Email** | Akun email, template, antrian pengiriman |
| **Pembayaran & Tagihan** | Penyedia pembayaran, transaksi, webhooks, langganan, kurs valuta asing |
| **Pencarian** | Pengaturan pencarian, sinonim, pengalihan, analitik |
| **Pengaturan Toko** | Pengaturan situs, geolokasi, peta negara, aturan bisnis |
| **Manajemen POS** | Terminal POS, shift, pergerakan uang tunai, template struk |
| **Pengguna & Peran** | Akun pengguna staf, peran, token API |

Ketika seorang pengguna memiliki beberapa peran, tingkat akses **tertinggi** menang. Misalnya, jika Peran A memberikan "Lihat" ke Produk dan Peran B memberikan "Penuh", pengguna mendapatkan akses "Penuh".

### Bendera Izin POS

Jika peran memberikan akses POS, tab Izin POS memungkinkan Anda menyetel secara tepat apa yang dapat dilakukan operator POS. Ini terpisah dari izin admin dan diperiksa di terminal POS.

![Izin POS](/static/core/admin/img/help/staff-roles/pos-permissions.webp)

| Kelompok | Izin | Deskripsi |
|-------|-----------|-------------|
| **Umum** | Akses POS | Dapat menggunakan sistem POS secara keseluruhan |
| **Penjualan & Diskon** | Diskon Manual | Dapat menerapkan diskon item per item atau tingkat keranjang |
| | Persentase Diskon Maksimal | Persentase diskon tertinggi yang diizinkan (0–100) |
| | Override Harga | Dapat mengganti harga produk di kasir |
| **Pengembalian & Penghapusan** | Proses Pengembalian | Dapat memproses pengembalian pada pesanan POS |
| | Penghapusan Pesanan | Dapat menghapus pesanan POS dari shift saat ini |
| **Kartu Hadiah** | Terbitkan Kartu Hadiah | Dapat menerbitkan kartu hadiah baru di kasir |
| | Periksa Saldo Kartu Hadiah | Dapat melihat saldo kartu hadiah |
| **Manajemen Uang Tunai** | Manajemen Uang Tunai | Dapat melakukan operasi masuk dan keluar uang tunai |
| | Buka Laci Uang | Dapat membuka laci uang tanpa penjualan |
| | Tutup Shift | Dapat menutup shift dan melakukan rekonsiliasi uang tunai |
| **Laporan** | Lihat Laporan POS | Dapat melihat laporan shift dan ringkasan penjualan |
| **Persediaan** | Penyesuaian Stok | Dapat menyesuaikan tingkat stok (terima, kerusakan, hitung ulang, kembalikan) |

Untuk izin boolean, jika **apa pun** dari peran pengguna mengaktifkannya, pengguna memiliki izin tersebut. Untuk Persentase Diskon Maksimal, nilai **tertinggi** dari semua peran berlaku.

## Mengelola Anggota Staf

Navigasikan ke **Pengaturan > Manajemen Staf** untuk melihat dan mengelola tim Anda.

### Daftar Staf

Daftar staf menampilkan semua pengguna dengan akses staf. Untuk setiap anggota, Anda dapat melihat:
- **Nama dan email**
- **Peran yang ditugaskan** (ditampilkan sebagai badge berwarna)
- **Tipe akses** — Hanya Admin, Hanya POS, atau Keduanya
- **Status 2FA** — Apakah autentikasi dua faktor diaktifkan
- **Status Aktif/Nonaktif**

Gunakan filter untuk menyaring berdasarkan peran, tipe akses, atau status 2FA.

### Menugaskan Peran ke Staf

1. Klik pada anggota staf untuk membuka profil mereka
2. Di bagian **Peran**, Anda akan melihat kartu untuk setiap peran yang tersedia
3. Klik toggle pada kartu peran apa pun untuk menugaskan atau menghapusnya
4. Perubahan berlaku segera — tidak diperlukan tombol simpan
5. Ringkasan **Izin Efektif** di bawah menunjukkan hasil gabungan dari semua peran yang ditugaskan

### Menambahkan Anggota Staf Baru

1. Navigasikan ke **Pengaturan > Manajemen Staf** dan klik **Tambahkan Anggota Staf**
2. Masukkan email, nama depan, dan nama belakang pengguna
3. Tetapkan kata sandi sementara
4. Tugaskan satu atau beberapa peran
5. Pengguna sekarang dapat masuk dengan akses yang diberikan peran mereka

## Menyalin Peran

Untuk membuat peran baru berdasarkan peran yang ada:

1. Buka peran yang ingin Anda salin
2. Klik **Salin Peran** di bagian bawah halaman
3. Sebuah peran baru dibuat dengan semua izin yang sama
4. Ubah nama dan sesuaikan izin jika diperlukan
5. Simpan peran baru

Ini berguna ketika Anda membutuhkan peran yang mirip dengan peran yang ada tetapi dengan sedikit perbedaan — misalnya, "Manajer Junior" berbasis "Manajer Toko" tetapi dengan izin yang lebih sedikit.

## Cara Izin Diterapkan

### Panel Admin

- **Keterlihatan menu** — Bagian sidebar disembunyikan untuk kategori di mana pengguna memiliki akses "Tidak Ada"
- **Akses halaman** — Mencoba mengunjungi halaman terbatas menampilkan kesalahan izin
- **Pembatasan aksi** — Dengan akses "Lihat", tombol edit dan hapus disembunyikan dan aksi simpan diblokir
- **Bypass superuser** — Akun superuser selalu memiliki akses penuh tanpa memandang penugasan peran

### Terminal POS

- **Gerbang login** — Hanya pengguna dengan setidaknya satu peran yang memiliki "Terminal POS" diaktifkan yang dapat masuk ke POS
- **Toggle fitur** — Tombol dan aksi POS (pengembalian, diskon, penghapusan, dll.) ditampilkan atau disembunyikan berdasarkan izin POS yang digabungkan pengguna
- **Batas diskon** — Persentase Diskon Maksimal menerapkan batas keras seberapa besar diskon operator POS dapat menerapkannya
- **Pengenalan API** — Semua izin POS diperiksa di lapisan API di sisi server, bukan hanya di UI

## Tips

- **Mulai dengan peran bawa-in** — 7 peran bawa-in mencakup sebagian besar struktur tim. Buat peran kustom hanya ketika Anda membutuhkan kontrol akses yang lebih spesifik.
- **Gunakan fitur salin** — Ketika Anda membutuhkan peran yang mirip dengan peran yang ada, salin dan sesuaikan daripada membangun dari awal.
- **Tugaskan beberapa peran ketika diperlukan** — Seorang anggota staf yang menangani pesanan dan pemasaran dapat ditugaskan peran "Manajer Pesanan" dan "Manajer Pemasaran". Izin digabungkan secara otomatis.
- **Pisahkan akses admin dan POS** — Kasir biasanya tidak memerlukan akses admin, dan staf kantor tidak memerlukan akses POS. Gunakan toggle akses untuk menjaga hal ini bersih.
- **Atur batas diskon untuk staf POS** — Persentase Diskon Maksimal mencegah kasir dari menerapkan diskon berlebihan. Atur ke 0 untuk tidak ada diskon, atau batas wajar seperti 10–25% untuk staf senior.
- **Periksa peran secara berkala** — Seiring tim Anda berkembang, tinjau penugasan peran untuk memastikan staf memiliki akses minimum yang diperlukan untuk pekerjaan mereka. Hapus peran ketika orang berubah posisi.
- **Aktifkan 2FA untuk peran sensitif** — Staf yang memiliki akses ke pembayaran, pengaturan, atau manajemen pengguna harus memiliki autentikasi dua faktor diaktifkan untuk keamanan.