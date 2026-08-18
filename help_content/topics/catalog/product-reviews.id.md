---
title: Ulasan Produk
---

Ulasan produk memungkinkan pelanggan untuk menilai dan menulis pengalaman mereka terhadap suatu produk. Ulasan yang Anda setujui akan muncul di halaman produk di toko Anda, di mana mereka membantu pembeli lain memutuskan apa yang akan dibeli. Spwig memberi Anda kendali penuh atas ulasan mana yang diterbitkan — tidak ada yang dipublikasikan hingga Anda menyetujui atau menolaknya.

Ulasan berada di bawah **Produk > Ulasan** di bilah sisi, yang terbuka sebagai kelompok: tautan paling atas membawa Anda ke **Dashboard Ulasan**, dan **Pantau Ulasan** membawa Anda langsung ke daftar ulasan.

## Dashboard Ulasan

Navigasi ke **Produk > Ulasan** untuk membuka dashboard — sebuah gambaran keseluruhan satu layar tentang bagaimana ulasan berkinerja di seluruh toko Anda.

![Dashboard Ulasan](/static/core/admin/img/help/product-reviews/reviews-dashboard.webp)

Pada bagian atas, enam kartu KPI merangkum aktivitas ulasan Anda:

| Kartu | Apa yang ditunjukkan |
|---|---|
| **Total Ulasan** | Semua ulasan yang pernah diajukan, termasuk yang belum disetujui |
| **Rata-rata Penilaian** | Rata-rata penilaian bintang di seluruh ulasan |
| **Menunggu Pemantauan** | Ulasan yang menunggu persetujuan atau penolakan Anda |
| **Tingkat Persetujuan** | Bagian dari semua ulasan yang telah Anda setujui |
| **Pembelian yang Diverifikasi** | Bagian dari ulasan yang ditulis oleh pelanggan dengan pesanan yang dikonfirmasi untuk produk tersebut |
| **Baru (30 hari terakhir)** | Ulasan yang diajukan dalam 30 hari terakhir |

Di bawah KPI, tiga grafik memberi detail lebih lanjut:

- **Distribusi Penilaian** — diagram batang tentang berapa banyak ulasan yang masuk ke setiap penilaian bintang (1-5). Kumpulan ulasan 1-bintang di sini perlu diteliti segera.
- **Volume Ulasan (12 minggu)** — diagram garis jumlah ulasan minggu per minggu, sehingga Anda dapat mengenali lonjakan setelah promosi atau penurunan yang perlu diperhatikan.
- **Saluran Pembelian Pengulas** — diagram donut dari saluran pemasaran (langsung, email, pencarian berbayar, media sosial organik, dan seterusnya) yang membawa *pembelian* di balik setiap ulasan. Ini menggunakan data atribusi Anda dan sangat berguna untuk melihat saluran mana yang membawa pelanggan yang kemudian meninggalkan ulasan — tetapi ini **bukan** catatan bagaimana pelanggan menemukan formulir ulasan itu sendiri. Spwig tidak melacaknya secara terpisah; lihat "Apa yang dilakukan dan tidak dilakukan oleh perjalanan tersebut" di bagian bawah panduan ini.

Dua daftar melengkapi dashboard:

- **Produk yang Paling Banyak Diulas** — produk yang paling banyak diulas, masing-masing dengan jumlah ulasan dan rata-rata penilaiannya, yang langsung terhubung ke produk tersebut.
- **Menunggu Pemantauan** — ulasan terbaru yang tertunda, sehingga Anda dapat langsung beralih ke apa pun yang memerlukan keputusan tanpa meninggalkan dashboard.

## Daftar Ulasan

Klik **Pantau Ulasan** (atau **Produk > Ulasan > Pantau Ulasan**) untuk melihat setiap ulasan sebagai kartu, dengan filter di atas daftar.

![Daftar Ulasan Produk dengan filter dan kartu ulasan yang tertunda](/static/core/admin/img/help/product-reviews/review-list.webp)

Setiap kartu menunjukkan thumbnail produk, judul ulasan, penilaian bintang, badge **Disetujui**/**Menunggu**, badge **Pembelian yang Diverifikasi** ketika berlaku, pratinjau komentar, serta siapa yang menulisnya dan kapan.

### Memfilter ulasan

Gunakan panel filter untuk menyempitkan daftar:

- **Pencarian** — cocokkan nama produk, username pelanggan, atau judul ulasan
- **Penilaian** — tampilkan hanya ulasan dengan penilaian bintang tertentu (berguna untuk menyelidiki keluhan 1-bintang)
- **Persetujuan** — segera memisahkan ulasan yang disetujui dari yang tertunda
- **Diverifikasi** — filter untuk ulasan dari pelanggan dengan pesanan yang dikonfirmasi untuk produk tersebut

Penggunaan filter berjalan instan tanpa mengisi ulang halaman.

## Menyetujui dan menolak ulasan

Ulasan tidak terlihat di toko Anda hingga Anda menyetujui mereka. Anda dapat menyetujui atau menolak ulasan secara individual atau dalam jumlah besar.

### Tindakan dalam jumlah besar

1. Di daftar ulasan, centang kotak centang di sebelah ulasan yang ingin Anda tindaki
2. Pilih **Setujui ulasan yang dipilih** atau **Tolak ulasan yang dipilih** dari dropdown tindakan
3. Klik **Pergi**

Ini adalah cara tercepat untuk menyelesaikan sejumlah besar ulasan baru.

### Ulasan individual

1.

Klik ikon sunting pada kartu ulasan, atau judulnya, untuk membuka ulasan
2.

Jaga semua format markdown, jalur gambar, blok kode, dan istilah teknis.

Pada tab **Review**, centang atau nonaktifkan **Apakah disetujui**
3.

Klik tombol centang di bagian atas untuk menyimpan

## Halaman edit ulasan

Membuka ulasan memberi Anda tampilan dashboard yang dibangun sekitar ulasan ini — bagian atas dengan nama produk, peringkat bintang, badge **Disetujui**/**Menunggu**, badge **Pembelian Terverifikasi** ketika berlaku, siapa yang menulis ulasan dan kapan, serta baris statistik (**Peringkat**, **Pilihan Bermanfaat**, **Pesanan Pelanggan**, **Pengeluaran Sepanjang Masa**). Di bawahnya, detailnya diatur dalam empat tab.

![Halaman edit ulasan — Tab Review dengan galeri gambar](/static/core/admin/img/help/product-reviews/review-edit-review-tab.webp)

### Tab Review

Ini tempatnya Anda memoderasi ulasan itu sendiri:

- **Gambar Ulasan** — jika pelanggan melampirkan foto, mereka muncul di sini sebagai galeri thumbnail; klik thumbnail mana pun untuk membuka gambar ukuran penuh di tab baru. Ulasan foto adalah tanda kepercayaan yang kuat bagi pembeli, jadi ini layak dilihat sebelum Anda menyetujui ulasan.
- **Peringkat**, **Judul**, **Komentar** — konten yang dikirimkan pelanggan
- **Apakah disetujui** — mengontrol apakah ulasan tersebut terlihat di toko Anda
- **Apakah pembelian terverifikasi** — menandai ulasan sebagai berasal dari pembeli yang diverifikasi; Spwig mengatur ini secara otomatis ketika ada pesanan yang selesai untuk produk tersebut (lihat tab **Pembelian**), tetapi Anda dapat menimpanya di sini jika diperlukan
- **Gambar** — daftar URL gambar di balik galeri di atas; biasanya Anda tidak perlu menyentuhnya, tetapi tetap dapat diedit untuk kasus-kasus khusus (misalnya, menghapus satu foto dari ulasan berfoto banyak)

Anda tidak dapat mengedit kata-kata ulasan — menyetujui atau menolak, dan mengelola gambar, adalah seluruh yang dapat Anda kendalikan di sini.

### Tab Pelanggan & Perjalanan

![Halaman edit ulasan — Tab Pelanggan & Perjalanan](/static/core/admin/admin/img/help/product-reviews/review-edit-customer-tab.webp)

Tab ini memberi Anda konteks tentang siapa yang menulis ulasan: jumlah pesanan keseluruhan, berapa banyak ulasan yang telah ditulis, rata-rata peringkat yang diberikan, seberapa lama mereka menjadi pelanggan, dan detail kontak mereka, dengan tautan untuk membuka catatan pelanggan lengkap mereka.

Di bawahnya adalah **perjalanan sumber lalu lintas** — saluran, kampanye, dan referrer yang membawa pelanggan ini ke toko Anda, yang dikumpulkan dari data atribusi dan ditampilkan sebagai timeline.

#### Yang dilakukan dan tidak dilakukannya 'perjalanan'

Bacalah timeline ini sebagai **perjalanan kedatangan dan pembelian** pelanggan — bagaimana mereka menemukan toko Anda dan kemudian membeli. Ini **bukan** catatan kunjungan di mana mereka menulis ulasan ini. Spwig tidak melacak di mana pelanggan berada, atau perangkat atau sesi apa yang digunakan saat mereka mengirimkan ulasan. Jika timeline menunjukkan 

- Periksa daftar **Menunggu Pemeriksaan** di dashboard terlebih dahulu — ini cara tercepat untuk melihat apa yang perlu diputuskan tanpa membuka daftar ulasan lengkap
- Kumpulan ulasan 1-bintang pada produk yang sama dalam grafik **Distribusi Rating** adalah tanda jelas untuk mengecek kemasan, kualitas produk, atau salinan penawaran Anda
- Gunakan filter **Diverifikasi** saat menentukan cara menangani ulasan yang mendekati batas — umpan balik dari pelanggan dengan pesanan yang diverifikasi memiliki bobot yang lebih besar dalam setiap perselisihan
- Setujui ulasan secara cepat, termasuk yang negatif — ulasan negatif yang terlihat bersamaan dengan tidak ada respons bisa terlihat lebih buruk daripada keluhan yang ditangani, dan ulasan yang terlambat muncul mengurangi minat pelanggan untuk memberi umpan balik di masa depan
- Jangan terlalu menganalisis **perjalanan sumber lalu lintas** atau grafik **Saluran Pembelian Penulis Ulasan** di dashboard — keduanya menjelaskan bagaimana pelanggan tiba dan membeli, bukan bagaimana mereka tiba untuk menulis ulasan
- Ulasan dengan foto memerlukan peninjauan yang lebih mendalam sebelum disetujui; foto produk dari pelanggan nyata adalah salah satu konten paling meyakinkan di toko Anda