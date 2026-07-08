---
title: Gambaran Program Afiliasi
---

Fitur program afiliasi Spwig memungkinkan Anda merekrut mitra yang mempromosikan produk Anda sebagai imbalan komisi. Saluran pemasaran ini memperluas jangkauan Anda melalui pengaruh, blogger, pembuat konten, dan duta merek yang berbagi tautan pelacakan unik dengan audiens mereka. Ketika seseorang mengklik tautan afiliasi dan melakukan pembelian, afiliasi tersebut mendapatkan komisi dan Anda mendapatkan pelanggan.

Gambaran ini menjelaskan apa itu program afiliasi, siapa yang cocok, dan bagaimana pedagang menggunakan program ini untuk membangun jaringan mitra yang mendorong penjualan.

![Dashboard Pedagang](/static/core/admin/img/help/affiliate-program-overview/merchant-dashboard.webp)

## Konsep Utama

Memahami istilah inti ini akan membantu Anda mengonfigurasi dan mengelola program afiliasi Anda:

| Istilah | Definisi |
|--------|---------|
| **Afiliasi** | Mitra yang mempromosikan produk Anda dan mendapatkan komisi dari penjualan yang dirujuk |
| **Program** | Struktur komisi dengan tingkat, aturan, dan pengaturan (Anda dapat membuat beberapa program) |
| **Tautan Pelacakan** | URL unik yang berisi kode afiliasi (misalnya, `yourstore.com/?ref=CODE`) |
| **Komisi** | Pembayaran yang diterima afiliasi untuk penjualan yang dirujuk, dihitung berdasarkan aturan program |
| **Umur Cookie** | Seberapa lama (dalam hari) cookie pelacakan bertahan setelah pelanggan mengklik tautan afiliasi |
| **Pembayaran** | Pembayaran dalam jumlah besar yang menyelesaikan beberapa komisi yang disetujui sekaligus |
| **Dashboard Pedagang** | Antarmuka admin Anda untuk mengelola program, afiliasi, komisi, dan pembayaran |
| **Portal Afiliasi** | Dashboard yang menghadap ke publik di mana afiliasi melihat pendapatan mereka, mendapatkan tautan pelacakan, dan meminta pembayaran |

## Cara Kerjanya

Alur kerja afiliasi mengikuti empat tahap utama:

### 1. Mendaftar
Afiliasi menemukan program Anda dan mengajukan aplikasi melalui portal afiliasi publik di `/affiliate/` di toko Anda. Anda dapat mengaktifkan **persetujuan otomatis** untuk program terbuka atau **ulasan manual** untuk kemitraan undangan.

### 2. Menyetujui
Anda meninjau aplikasi yang menunggu di **Pemasaran > Afiliasi**. Periksa situs web, kehadiran media sosial, dan kesesuaian audiens setiap pelamar sebelum menyetujui. Setelah disetujui, afiliasi menerima kredensial login dan dapat mengakses dashboard mereka.

### 3. Mempromosikan
Afiliasi yang disetujui mendapatkan tautan rujukan unik dari portal mereka. Mereka berbagi tautan ini dalam posting blog, media sosial, surat kabar email, atau di mana pun mereka terhubung dengan audiens mereka. Spwig menetapkan cookie pelacakan ketika seseorang mengklik tautan tersebut.

### 4. Membuat Keuntungan
Ketika pelanggan yang dirujuk menyelesaikan pembelian dalam masa berlaku cookie, Spwig membuat catatan komisi. Anda meninjau dan menyetujui komisi di **Pemasaran > Komisi**, lalu memproses pembayaran ketika afiliasi mencapai ambang batas pembayaran minimum.

## Ringkasan Alur Kerja Pedagang

Sebagai pedagang, Anda mengelola seluruh siklus program dari panel admin Anda:

### Membuat Program
Mulailah dengan membuat satu atau beberapa program afiliasi di **Pemasaran > Program Afiliasi**. Setiap program memiliki struktur komisi, umur cookie, dan pengaturan persetujuan sendiri. Anda mungkin membuat program terpisah untuk pengaruh (komisi lebih tinggi) dibandingkan mitra umum (komisi lebih rendah).

### Meninjau Aplikasi
Aplikasi afiliasi baru muncul di **Pemasaran > Afiliasi** dengan status **Menunggu**. Tinjau setiap aplikasi untuk memverifikasi mitra adalah pilihan yang baik untuk merek Anda. Setujui untuk mengaktifkan akun mereka atau tolak dengan alasan.

### Menyetujui Komisi
Ketika afiliasi menghasilkan penjualan, komisi muncul di **Pemasaran > Komisi** dengan status **Menunggu**. Tinjau pesanan terkait untuk memverifikasi bahwa pesanan tersebut sah (bukan rujukan diri, bukan pesanan yang dikembalikan), lalu setujui atau tolak sesuai.

### Memproses Pembayaran
Setelah afiliasi mengumpulkan komisi yang disetujui di atas ambang pembayaran minimum Anda, proses pembayaran dalam jumlah besar di **Pemasaran > Pembayaran**. Spwig terintegrasi dengan PayPal dan Airwallex untuk pembayaran otomatis, atau Anda dapat mencatat transfer bank manual.

## Ringkasan Alur Kerja Afiliasi

Memahami bagaimana afiliasi mengalami program Anda membantu Anda merancang onboarding dan dukungan yang lebih baik:

### Mendaftar
Afiliasi mengunjungi portal afiliasi Anda, membaca detail program (tingkat komisi, umur cookie, ketentuan pembayaran), dan mengajukan aplikasi dengan informasi kontak mereka dan saluran promosi.

### Membuat Tautan
Setelah disetujui, afiliasi masuk ke dashboard mereka untuk membuat tautan pelacakan. Mereka dapat membuat tautan toko umum atau tautan ke produk/kategori spesifik yang ingin mereka promosikan.

### Mempromosikan
Afiliasi berbagi tautan pelacakan mereka di mana pun mereka terhubung dengan pelanggan potensial — posting blog, video YouTube, cerita Instagram, surat kabar email, atau situs perbandingan.

### Meminta Pembayaran
Afiliasi melacak pendapatan mereka secara real time melalui dashboard portal afiliasi. Ketika saldo mereka yang disetujui mencapai ambang pembayaran minimum, mereka dapat meminta pembayaran.

## Di Mana Menemukan Setiap Fitur

| Fitur | Lokasi Admin | Deskripsi |
|------|--------------|----------|
| **Program** | Pemasaran > Program Afiliasi | Membuat dan mengonfigurasi struktur komisi |
| **Afiliasi** | Pemasaran > Afiliasi | Meninjau aplikasi, mengelola akun afiliasi |
| **Komisi** | Pemasaran > Komisi | Meninjau dan menyetujui komisi yang menunggu |
| **Pembayaran** | Pemasaran > Pembayaran | Memproses pembayaran dalam jumlah besar kepada afiliasi |
| **Pengaturan** | Pemasaran > Pengaturan Afiliasi | Pengaturan global, penyedia pembayaran, personalisasi portal |
| **Dashboard** | Pemasaran > Dashboard Afiliasi | Ringkasan analitik dengan klik, pesanan, dan total komisi |

Portal yang menghadap ke afiliasi secara otomatis tersedia di `/affiliate/` pada URL publik toko Anda.

## Kasus Penggunaan Umum

Berikut adalah empat cara terbukti pedagang menggunakan program afiliasi Spwig untuk memperluas bisnis mereka:

### Kemitraan Pengaruh
Kolaborasi dengan pengaruh media sosial yang memiliki audiens yang terlibat di bidang Anda. Tawarkan tingkat komisi yang lebih tinggi (15–20%) untuk menarik pengaruh berkualitas yang dapat mengarahkan lalu lintas yang signifikan. Gunakan tautan pelacakan untuk mengukur ROI untuk setiap kemitraan.

### Duta Merek
Bangun jaringan pelanggan setia yang menjadi duta merek. Tawarkan akun afiliasi kepada pelanggan berulang sehingga mereka dapat memperoleh komisi ketika mereka merujuk teman dan keluarga. Ini bekerja terutama baik untuk produk niche dengan komunitas yang bersemangat.

### Pembuat Konten
Rekrut blogger, YouTuber, dan podcaster yang membuat panduan pembelian, ulasan, atau konten perbandingan. Afiliasi dengan konten yang abadi dapat menghasilkan rujukan konsisten bulan demi bulan.

### Jaringan Referensi
Izinkan pelanggan yang ada untuk bergabung dengan program Anda dan mendapatkan komisi dengan berbagi produk yang mereka sukai. Ini menciptakan loop virall di mana pelanggan yang puas menjadi promotor, membawa masuk pelanggan baru yang mungkin juga menjadi afiliasi.

## Tips

- **Mulai dengan satu program** — Buat program mitra umum dengan tingkat komisi 10% dan umur cookie 30 hari. Anda dapat menambahkan program khusus nanti setelah Anda memahami mitra mana yang bekerja terbaik.
- **Tetapkan ekspektasi yang jelas** — Dokumentasikan proses persetujuan, jadwal komisi, dan jadwal pembayaran di portal afiliasi. Transparansi membangun kepercayaan dan mengurangi permintaan dukungan.
- **Pantau untuk penipuan** — Tinjau komisi dengan hati-hati untuk tanda merah seperti rujukan diri (afiliasi membeli dari tautan mereka sendiri), tingkat pengembalian yang tidak biasa tinggi, atau pola klik mencurigakan. Tolak komisi yang curang segera.
- **Komunikasikan secara teratur** — Kirim pembaruan bulanan kepada afiliasi Anda dengan berita program, penekanan kalender promosi, dan pengakuan penampil terbaik. Komunikasi aktif menjaga afiliasi tetap terlibat dan mempromosikan.
- **Optimalkan untuk mobile** — Sebagian besar afiliasi berbagi tautan di media sosial di mana sebagian besar klik berasal dari perangkat mobile. Uji alur checkout Anda di ponsel untuk memastikan pengalaman yang mulus bagi pelanggan yang dirujuk.
- **Sediakan aset kreatif** — Buat mudah bagi afiliasi untuk mempromosikan produk Anda dengan menyediakan gambar banner, foto produk, dan salinan yang sudah ditulis yang dapat mereka gunakan dalam konten mereka.

Ingat: Pertahankan semua format markdown, jalur gambar, blok kode, dan istilah teknis tepat seperti yang ditunjukkan dalam aturan preservasi.