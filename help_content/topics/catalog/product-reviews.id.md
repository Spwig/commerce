---
title: Ulasan Produk
---

Ulasan produk memungkinkan pelanggan memberikan penilaian dan menulis tentang pengalaman mereka dengan suatu produk. Ulasan yang Anda setujui akan muncul di halaman produk di storefront Anda, di mana ulasan tersebut membantu pembeli lain memutuskan apa yang akan dibeli. Spwig memberikan Anda kendali penuh atas ulasan mana yang dipublikasikan — tidak ada yang diterbitkan sampai Anda menyetujuinya.

Ulasan berada di bawah **Produk > Ulasan** di bilah samping, yang terbuka sebagai grup: tautan atas membawa Anda ke **Dasbor Ulasan**, dan **Moderasi Ulasan** membawa Anda langsung ke daftar ulasan.

## Dasbor Ulasan

Navigasi ke **Produk > Ulasan** untuk membuka dasbor — ringkasan satu layar tentang bagaimana ulasan berkinerja di seluruh toko Anda.

![Dasbor Ulasan](/static/core/admin/img/help/product-reviews/reviews-dashboard.webp)

Di bagian atas, enam kartu KPI merangkum aktivitas ulasan Anda:

| Kartu | Apa yang ditampilkan |
|---|---|
| **Total Ulasan** | Semua ulasan yang pernah dikirim, disetujui atau tidak |
| **Rating Rata-rata** | Rata-rata rating bintang di seluruh ulasan |
| **Menunggu Moderasi** | Ulasan yang menunggu persetujuan atau penolakan Anda |
| **Tingkat Persetujuan** | Persentase semua ulasan yang telah Anda setujui |
| **Pembelian Terverifikasi** | Persentase ulasan yang ditinggalkan oleh pelanggan dengan pesanan terkonfirmasi untuk produk tersebut |
| **Baru (30 hari)** | Ulasan yang dikirim dalam 30 hari terakhir |

Di bawah KPI, tiga grafik memberikan detail lebih lanjut:

- **Distribusi Rating** — grafik batang tentang berapa banyak ulasan yang masuk ke setiap rating bintang (1–5). Sekelompok ulasan bintang 1 di sini layak diselidiki segera.
- **Volume Ulasan (12 minggu)** — grafik garis jumlah ulasan per minggu, sehingga Anda dapat melihat lonjakan setelah promosi atau penurunan yang perlu perhatian.
- **Saluran Pembelian Peninjau** — grafik donat saluran pemasaran (langsung, email, pencarian berbayar, media sosial organik, dan sebagainya) yang mendorong *pembelian* di balik setiap ulasan. Ini menggunakan kembali data atribusi Anda dan benar-benar berguna untuk melihat saluran mana yang membawa pelanggan yang kemudian meninggalkan ulasan — tetapi ini **bukan** catatan tentang bagaimana pelanggan menemukan formulir ulasan itu sendiri. Spwig tidak melacak itu secara terpisah; lihat "Apa yang dilakukan dan tidak dilakukan oleh perjalanan" lebih jauh di panduan ini.

Dua daftar melengkapi dasbor:

- **Produk Paling Banyak Diulas** — produk Anda yang paling banyak diulas, masing-masing dengan jumlah ulasan dan rating rata-rata, yang menautkan langsung ke produk.
- **Menunggu Moderasi** — ulasan tertunda terbaru Anda, sehingga Anda dapat langsung masuk ke apa pun yang membutuhkan keputusan tanpa meninggalkan dasbor.

## Daftar ulasan

Klik **Moderasi Ulasan** (atau **Produk > Ulasan > Moderasi Ulasan**) untuk melihat setiap ulasan sebagai kartu, dengan filter di atas daftar.

![Daftar Ulasan Produk dengan filter dan kartu ulasan tertunda](/static/core/admin/img/help/product-reviews/review-list.webp)

Setiap kartu menampilkan thumbnail produk, judul ulasan, rating bintang, lencana **Disetujui**/**Tertunda**, lencana **Pembelian Terverifikasi** jika berlaku, pratinjau komentar, dan siapa yang menulisnya serta kapan.

### Memfilter ulasan

Gunakan panel filter untuk menyempitkan daftar:

- **Pencarian** — mencocokkan nama produk, nama pengguna pelanggan, atau judul ulasan
- **Rating** — tampilkan hanya ulasan dengan rating bintang tertentu (berguna untuk menyelidiki keluhan bintang 1)
- **Persetujuan** — memisahkan ulasan disetujui dari tertunda dengan cepat
- **Terverifikasi** — filter ke ulasan dari pelanggan dengan pesanan terkonfirmasi untuk produk tersebut

Pemfilteran berjalan secara instan tanpa memuat ulang halaman.

## Menyetujui dan menolak ulasan

Ulasan tidak terlihat di storefront Anda sampai Anda menyetujuinya. Anda dapat menyetujui atau menolak ulasan secara individual atau massal.

### Aksi massal

1. Di daftar ulasan, centang kotak centang di samping ulasan yang ingin Anda proses
2. Pilih **Setujui ulasan terpilih** atau **Tolak ulasan terpilih** dari dropdown aksi
3. Klik **Pergi**

Ini adalah cara tercepat untuk memproses sekumpulan ulasan baru.

### Ulasan individual

1.

Klik ikon edit pada kartu ulasan, atau judulnya, untuk membuka ulasan
2.

Pada tab **Review**, centang atau nonaktifkan **Apakah disetujui**
3.

Klik tombol centang di bagian header untuk menyimpan

## Halaman edit ulasan

Membuka ulasan memberi Anda tampilan dashboard yang dibangun sekitar ulasan ini — bagian atas dengan nama produk, peringkat bintang, badge **Disetujui**/**Menunggu**, badge **Pembelian Diverifikasi** jika berlaku, siapa yang menulis ulasan dan kapan, serta baris statistik (**Peringkat**, **Pilihan Bermanfaat**, **Pesanan Pelanggan**, **Pengeluaran Sepanjang Masa**). Di bawahnya, detailnya diatur dalam empat tab.

![Halaman edit ulasan — Tab Review dengan galeri gambar](/static/core/admin/img/help/product-reviews/review-edit-review-tab.webp)

### Tab Review

Ini tempat Anda memoderasi ulasan itu sendiri:

- **Gambar Ulasan** — jika pelanggan melampirkan foto, mereka muncul di sini sebagai galeri thumbnail; klik thumbnail mana pun untuk membuka gambar ukuran penuh di tab baru. Ulasan foto adalah tanda kepercayaan yang kuat bagi pembeli, jadi ini layak dilihat sebelum Anda menyetujui ulasan.
- **Peringkat**, **Judul**, **Komentar** — konten yang telah dikirimkan pelanggan
- **Apakah disetujui** — mengontrol apakah ulasan tersebut terlihat di toko Anda
- **Apakah pembelian diverifikasi** — menandai ulasan sebagai berasal dari pembeli yang diverifikasi; Spwig mengatur ini secara otomatis ketika terdapat pesanan yang selesai untuk produk tersebut (lihat tab **Pembelian**), tetapi Anda dapat menimpanya di sini jika diperlukan
- **Gambar** — daftar URL gambar di balik galeri di atas; biasanya Anda tidak perlu menyentuhnya, tetapi tetap bisa diedit untuk kasus-kasus khusus (misalnya, menghapus satu foto dari ulasan berfoto banyak)

Anda tidak dapat mengedit kata-kata ulasan — menyetujui atau menolak, dan mengelola gambar, adalah seluruh yang dapat Anda kendalikan di sini.

### Tab Pelanggan & Perjalanan

![Halaman edit ulasan — Tab Pelanggan & Perjalanan](/static/core/admin/img/help/product-reviews/review-edit-customer-tab.webp)

Tab ini memberi Anda konteks tentang siapa yang menulis ulasan: jumlah pesanan keseluruhan, berapa banyak ulasan yang telah ditulis, rata-rata peringkat yang diberikan, seberapa lama mereka menjadi pelanggan, dan detail kontaknya, dengan tautan untuk membuka catatan pelanggan lengkapnya.

Di bawahnya terdapat **perjalanan sumber lalu lintas** — saluran, kampanye, dan referrer yang membawa pelanggan ini ke toko Anda, yang diambil dari data atribusi Anda dan ditampilkan sebagai timeline.

#### Yang dilakukan dan tidak dilakukannya 'perjalanan'

Bacalah timeline ini sebagai **perjalanan kedatangan dan pembelian** pelanggan — bagaimana mereka menemukan toko Anda dan kemudian membeli. Ini **bukan** catatan kunjungan di mana mereka menulis ulasan ini. Spwig tidak melacak di mana pelanggan berada, atau perangkat atau sesi apa yang digunakan saat mereka mengirimkan ulasan. Jika timeline menunjukkan 

- Periksa daftar **Menunggu Moderasi** di dasbor terlebih dahulu — ini adalah cara tercepat untuk melihat apa yang perlu diputuskan tanpa membuka daftar ulasan lengkap
- Sekelompok ulasan 1 bintang pada produk yang sama di grafik **Distribusi Rating** adalah sinyal jelas untuk menyelidiki kemasan, kualitas produk, atau salinan daftar Anda
- Gunakan filter **Terverifikasi** saat memutuskan cara menangani ulasan yang berada di ambang batas — umpan balik dari pelanggan dengan pesanan yang dikonfirmasi memiliki bobot lebih besar dalam sengketa apa pun
- Setujui ulasan dengan cepat, termasuk yang kritis — ulasan negatif yang terlihat tanpa tanggapan dapat terlihat lebih buruk daripada keluhan yang ditangani, dan ulasan yang lambat muncul dapat membuat pelanggan enggan memberikan umpan balik di masa depan
- Jangan terlalu menafsirkan **Perjalanan sumber lalu lintas** atau grafik **Saluran Pembelian Peninjau** di dasbor — keduanya menggambarkan bagaimana pelanggan tiba dan membeli, bukan bagaimana mereka tiba untuk menulis ulasan
- Ulasan dengan foto layak mendapat perhatian lebih sebelum disetujui; foto produk dari pelanggan asli adalah salah satu konten paling meyakinkan di etalase Anda