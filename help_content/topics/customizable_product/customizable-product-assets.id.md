---
title: Clipart dan Font untuk Produk yang Dapat Disesuaikan
---

Editor desain dilengkapi dengan dua jenis aset kreatif yang dapat Anda sediakan untuk pelanggan: **clipart** (grafik siap pakai yang dapat mereka tambahkan ke desain mereka) dan **font khusus** (di luar font sistem standar). Membangun perpustakaan aset yang tercurah dengan baik membuat editor lebih berguna dan membantu pelanggan membuat desain yang lebih baik lebih cepat.

## Perpustakaan Clipart

Clipart memberikan pelanggan perpustakaan grafik siap pakai yang dapat mereka tambahkan ke desain mereka hanya dengan satu klik. Sebaliknya dari meminta pelanggan untuk mencari dan mengunggah gambar mereka sendiri untuk elemen umum seperti ikon, border, atau grafik dekoratif, Anda menyediakan mereka siap pakai.

### Membuat kategori clipart

Clipart diorganisir ke dalam kategori yang dapat dibaca oleh pelanggan. Kategori membantu pelanggan menemukan apa yang mereka butuhkan dengan cepat.

1. Navigasikan ke **Produk yang Dapat Disesuaikan > Kategori Clipart**
2. Klik **+ Tambah Kategori Clipart**
3. Isi:
   - **Nama Kategori** — Apa yang dilihat pelanggan (misalnya, "Olahraga", "Border", "Liburan")
   - **Slug** — Dihasilkan secara otomatis dari nama
   - **Ikon** — Kelas ikon Font Awesome untuk tab kategori (misalnya, `fas fa-football-ball`)
   - **Urutan Pengurutan** — Mengontrol urutan kategori muncul di editor
4. Klik **Simpan**

**Contoh kategori untuk toko kaos:**

| Kategori | Ikon | Contoh clipart |
|----------|------|-----------------|
| Olahraga | `fas fa-football-ball` | Logo tim, peralatan olahraga, simbol olahraga |
| Humor | `fas fa-laugh` | Meme, kutipan lucu, karakter kartun |
| Alam | `fas fa-leaf` | Hewan, bunga, pemandangan |
| Geometris | `fas fa-shapes` | Pola, bentuk abstrak, desain suku |

**Contoh kategori untuk toko cetak/poster:**

| Kategori | Ikon | Contoh clipart |
|----------|------|-----------------|
| Border | `fas fa-border-all` | Bingkai dekoratif, ornamen sudut |
| Musiman | `fas fa-snowflake` | Ikon liburan, motif musiman |
| Ikon | `fas fa-icons` | Bintang, hati, panah, tanda centang |
| Latar Belakang | `fas fa-image` | Tekstur, gradien, pola |

### Menambahkan aset clipart

Setiap aset clipart adalah file gambar (PNG atau SVG) yang dapat ditempatkan oleh pelanggan di kanvas mereka.

1. Navigasikan ke **Produk yang Dapat Disesuaikan > Aset Clipart**
2. Klik **+ Tambah Aset Clipart**
3. Isi:
   - **Nama** — Nama deskriptif (misalnya, "Bintang Emas", "Helm Sepak Bola")
   - **Kategori** — Pilih dari kategori clipart Anda
   - **Aset Gambar** — Klik untuk membuka Perpustakaan Media dan pilih atau unggah file gambar
   - **Cakupan** — Pilih ketersediaan (lihat di bawah)
   - **Tag** — Kata kunci yang dapat dicari untuk clipart ini (misalnya, `['star', 'gold', 'decoration']`)
   - **Urutan Pengurutan** — Mengontrol posisi dalam kategori
4. Klik **Simpan**

### Memahami cakupan clipart

Setiap aset clipart memiliki cakupan yang mengontrol di mana ia tersedia:

| Cakupan | Deskripsi | Kasus penggunaan |
|-------|-------------|----------|
| **Tersedia untuk Semua Produk** | Muncul di browser clipart untuk setiap produk yang dapat disesuaikan | Grafik umum seperti bintang, border, dan ikon umum |
| **Hanya untuk Produk Tertentu** | Muncul hanya untuk satu produk yang dipilih | Grafik khusus produk seperti logo merek atau seni berbasis tema produk |

Untuk sebagian besar aset, gunakan **Tersedia untuk Semua Produk**. Cadangkan cakupan produk khusus untuk aset yang hanya masuk akal dalam konteks satu produk — contohnya, logo tim khusus untuk produk merchandise tim.

### Panduan file clipart

- **Format:** Gunakan PNG untuk grafik raster dan SVG untuk grafik vektor. File SVG dapat diukur tanpa kehilangan kualitas, membuatnya ideal untuk clipart yang mungkin diubah ukurannya secara signifikan oleh pelanggan
- **Resolusi:** File PNG harus setidaknya 500x500 piksel untuk kualitas cetak yang baik
- **Latar Belakang:** Gunakan latar belakang transparan (PNG dengan saluran alpha atau SVG) sehingga clipart menyatu secara alami dengan desain
- **Ukuran File:** Pertahankan file clipart individu di bawah 500KB untuk memuat cepat di editor

## Font Khusus

Font khusus memperluas pemilih font di editor desain di luar font sistem standar.

Ini memungkinkan Anda menawarkan tipografi yang disusun khusus yang sesuai dengan merek atau gaya produk Anda.

### Menambahkan font kustom

1. Navigasikan ke **Produk yang Dapat Disesuaikan > Font Kustom**
2. Klik **+ Tambahkan Font Kustom**
3. Isi:
   - **Nama Font** — Nama tampilan yang ditampilkan di pemilih font (misalnya, "Playfair Display")
   - **Font Family** — Nama font-family CSS yang digunakan secara internal (misalnya, `PlayfairDisplay`)
   - **Biasa** — Klik untuk mengunggah file font berat biasa melalui Perpustakaan Media (WOFF2 atau TTF)
   - **Bold** — Variasi berat bold opsional
   - **Italic** — Variasi miring opsional
   - **Bold Italic** — Variasi bold miring opsional
4. Klik **Simpan**

**Berat biasa** diperlukan untuk font kustom. Variasi bold, miring, dan bold miring adalah opsional — jika tidak disediakan, browser akan mencoba mensintesis gaya-gaya ini dari font biasa, meskipun hasilnya mungkin tidak terlihat sehalus file font khusus.

### Font sistem vs font kustom

Anda juga dapat mendaftarkan font sistem yang sudah terinstal di sebagian besar perangkat:

1. Tambahkan entri font kustom baru
2. Centang **Font Sistem**
3. Masukkan nama font family tepat seperti yang muncul dalam CSS (misalnya, `Georgia`, `Courier New`)
4. Tidak diperlukan unggah file untuk font sistem

Font sistem dimuat secara instan karena sudah ada di perangkat pelanggan. Font yang diunggah kustom perlu diunduh terlebih dahulu, yang menambahkan sedikit penundaan saat font pertama kali dipilih.

### Rekomendasi font berdasarkan jenis produk

**Untuk kemeja dan pakaian:**
- Font bold yang menonjol bekerja terbaik: Impact, Anton, Bebas Neue, Oswald
- Huruf blok dan font sans-serif paling terbaca pada kain
- Hindari font tipis atau halus yang mungkin tidak mencetak dengan baik pada permukaan ber tekstur

**Untuk poster dan produk cetak:**
- Font serif yang elegan untuk desain formal: Playfair Display, Merriweather, Lora
- Font script untuk undangan dan kartu: Great Vibes, Dancing Script, Pacifico
- Font sans-serif yang bersih untuk desain modern: Montserrat, Raleway, Open Sans

### Format file font

| Format | Ekstensi | Rekomendasi |
|--------|-----------|----------------|
| WOFF2 | `.woff2` | Disarankan — ukuran file terkecil, pemuatan tercepat |
| TrueType | `.ttf` | Pilihan yang baik — kompatibel secara luas |

File WOFF2 biasanya 30-50% lebih kecil daripada file TTF, sehingga dimuat lebih cepat di editor pelanggan. Gunakan WOFF2 jika tersedia.

## Mengelola perpustakaan aset Anda

### Mengorganisasi untuk pelanggan

Urutan aset yang muncul di editor dikontrol oleh bidang **Urutan Pengurutan** pada kategori dan aset individu. Angka yang lebih rendah muncul lebih dulu. Gunakan ini untuk:

- Menempatkan kategori clipart paling populer Anda di bagian atas
- Menempatkan clipart terbaik dan paling serbaguna di bagian atas setiap kategori
- Mengurutkan font dengan opsi yang paling sering digunakan di bagian atas

### Menjaga perpustakaan tetap segar

- Tambahkan clipart musiman sebelum hari raya (Halloween, Natal, Hari Valentine) dan non-aktifkan setelahnya
- Gunakan kotak centang **Aktif** untuk menyembunyikan aset secara sementara tanpa menghapusnya
- Pantau clipart dan font yang paling sering digunakan pelanggan dan perluas kategori tersebut

## Tips

- Mulailah dengan kecil — 20-30 clipart berkualitas tinggi di 3-4 kategori lebih baik daripada ratusan opsi yang biasa. Anda selalu bisa menambahkan lebih banyak saat Anda belajar apa yang pelanggan inginkan.
- Gunakan format SVG untuk clipart jika memungkinkan. File SVG lebih kecil, skalabel sempurna ke ukuran apa pun, dan menghasilkan cetakan yang lebih tajam daripada gambar raster.
- Uji setiap font yang diunggah di editor desain untuk memastikan semua karakter ditampilkan dengan benar, terutama karakter khusus dan aksen jika pelanggan menggunakan beberapa bahasa.
- Beri tag clipart secara menyeluruh — pelanggan mencari berdasarkan kata kunci, jadi tag deskriptif seperti "emas", "bintang", "5-titik", "dekorasi" membantu mereka menemukan aset yang tepat dengan cepat.
- Kelompokkan clipart terkait ke dalam kategori yang sama. Jika Anda menjual merchandise tim, buat kategori per olahraga daripada satu kategori besar "Olahraga".
- Periksa perpustakaan clipart Anda secara teratur dari perspektif pelanggan dengan mengunjungi editor desain di toko online.