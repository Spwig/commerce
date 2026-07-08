---
title: Membuat Program Afiliasi
---

Program afiliasi mendefinisikan cara mitra Anda memperoleh komisi ketika mereka merujuk pelanggan ke toko Anda. Setiap program memiliki struktur komisi, aturan pelacakan, dan ambang batas pembayaran sendiri. Anda dapat membuat beberapa program untuk melayani segmen afiliasi yang berbeda — seperti pengaruh, pembuat konten, atau mitra referensi dalam jumlah besar.

![Daftar Program](/static/core/admin/img/help/creating-affiliate-programs/programs-list.webp)

## Komponen Program

Setiap program afiliasi terdiri dari:

- **Nama dan Deskripsi** — Mengidentifikasi program dan menjelaskannya kepada afiliasi
- **Struktur Komisi** — Seberapa banyak afiliasi memperoleh per penjualan (persentase atau jumlah tetap)
- **Umur Cookie** — Seberapa lama pelacakan referensi berlangsung setelah klik (1-365 hari)
- **Otomatis Persetujuan** — Apakah afiliasi baru bergabung secara otomatis atau memerlukan tinjauan manual
- **Ambang Batas Pembayaran Minimum** — Seberapa banyak afiliasi harus memperoleh sebelum meminta pembayaran
- **Status** — Aktif, dijeda, atau diarsipkan

## Jenis Komisi

Pilih antara dua model komisi saat membuat program Anda:

| Jenis | Cara Kerjanya | Kapan Digunakan | Perhitungan Contoh |
|------|-------------|-------------|---------------------|
| **Persentase** | Afiliasi memperoleh persentase dari subtotal pesanan | Hadiah yang dapat berkembang seiring nilai pesanan | 10% dari pesanan $150 = komisi $15 |
| **Jumlah Tetap** | Afiliasi memperoleh jumlah tetap per penjualan | Biaya yang dapat diprediksi; terbaik untuk produk volume tinggi, margin rendah | $25 per penjualan tanpa memandang nilai pesanan |

**Komisi persentase** berkembang secara alami — afiliasi memperoleh lebih banyak ketika mereka merujuk pelanggan bernilai tinggi. Ini menyelaraskan insentif mereka dengan Anda dan merupakan model yang paling umum (biasanya 5–15%).

**Komisi tetap** bekerja dengan baik untuk layanan, langganan, atau program referensi dalam jumlah besar di mana Anda ingin biaya per penjualan yang dapat diprediksi. Mereka mudah dipahami dan dibuat anggaran, tetapi mungkin memberi kompensasi yang kurang untuk afiliasi yang membawa pesanan besar.

## Membuat Program

Navigasikan ke **Pemasaran > Program Afiliasi** dan klik **+ Tambah Program**.

### Pengaturan Langkah Demi Langkah

1. **Nama Program**
   Masukkan nama deskriptif yang terlihat oleh afiliasi (misalnya, "Program Mitra" atau "Tingkat Pengaruh").

2. **Slug**
   Identifikasi yang ramah URL dihasilkan secara otomatis dari nama. Digunakan dalam URL dan referensi internal. Anda dapat menyesuaikannya jika diperlukan.

3. **Deskripsi**
   Teks opsional menjelaskan manfaat dan ketentuan program. Afiliasi melihat ini saat meninjau program yang dapat mereka gabung.

4. **Jenis Komisi**
   Pilih **Persentase** atau **Jumlah Tetap**.

5. **Nilai Komisi**
   - Untuk persentase: Masukkan nilai antara 0 dan 100 (misalnya, `10` untuk 10%)
   - Untuk jumlah tetap: Masukkan jumlah dolar per penjualan (misalnya, `25.00` untuk $25)

6. **Umur Cookie dalam Hari**
   Seberapa lama cookie pelacakan berlangsung (1–365). Lihat bagian di bawah untuk panduan.

7. **Otomatis Persetujuan Afiliasi**
   - **Dicentang** — Afiliasi baru bergabung secara otomatis
   - **Tidak dicentang** — Anda meninjau dan menyetujui setiap aplikasi secara manual

8. **Pembayaran Minimum**
   Saldo minimum yang harus dikumpulkan afiliasi sebelum meminta pembayaran (misalnya, `50.00` untuk $50).

9. **Status**
   Atur ke **Aktif** untuk menerima afiliasi baru dan melacak referensi.

10. **Simpan** program.

## Penjelasan Umur Cookie

Umur cookie menentukan seberapa lama Spwig mengingat bahwa seorang pelanggan mengklik tautan referensi afiliasi.

### Cara Kerjanya

1. Seorang pelanggan mengklik tautan afiliasi
2. Spwig mengatur cookie pelacakan di browser pelanggan
3. Jika pelanggan menyelesaikan pembelian **dalam masa berlaku cookie**, pesanan dikreditkan ke afiliasi
4. Jika cookie kedaluwarsa sebelum pembelian, afiliasi tidak memperoleh komisi

### Memilih Durasi

| Durasi | Kasus Penggunaan | Skenario Tipe |
|----------|----------|------------------|
| **1–7 hari** | Pembelian impulsif, penjualan kilat | Barang konsumsi cepat, tawaran terbatas waktu |
| **30 hari** | E-commerce standar | Penjualan online umum, rekomendasi default |
| **60–90 hari** | Pembelian yang dipertimbangkan | Item berharga, B2B, layanan |
| **180+ hari** | Siklus penjualan yang panjang | Perangkat lunak perusahaan, langganan, barang mewah |

**Standar industri adalah 30 hari.** Ini menyeimbangkan atribusi yang adil untuk afiliasi dengan batas pelacakan yang praktis. Masa berlaku yang lebih pendek memfavoritkan pelanggan yang cepat berubah; masa berlaku yang lebih panjang memberi pelanggan waktu untuk meneliti dan kembali menyelesaikan pembelian mereka.

### Catatan Teknis

Umur cookie hanya memengaruhi **atribusi**. Komisi yang disetujui tetap valid selamanya — umur cookie hanya menentukan apakah pesanan dikreditkan ke afiliasi pada awalnya.

## Pengaturan Otomatis Persetujuan

Pengaturan otomatis persetujuan mengontrol apakah aplikasi afiliasi baru memerlukan tinjauan manual.

### Kapan Mengaktifkan Otomatis Persetujuan

- **Program umum** — Anda ingin memperluas basis afiliasi Anda secara cepat tanpa hambatan
- **Produk berisiko rendah** — Risiko penipuan atau merek minimal
- **Program volume tinggi** — Anda mengharapkan banyak aplikasi dan tidak dapat meninjau setiap aplikasi secara manual

### Kapan Memerlukan Tinjauan Manual

- **Program undangan saja** — Anda hanya menerima mitra yang telah diverifikasi sebelumnya
- **Program premium** — Tingkat komisi tinggi atau manfaat eksklusif
- **Produk yang sensitif merek** — Anda perlu memastikan afiliasi selaras dengan nilai merek Anda
- **Pencegahan penipuan** — Anda ingin menyaring akun yang mencurigakan

### Pertimbangan Keamanan

Meninjau afiliasi secara manual membantu mencegah:
- Skema referensi diri (afiliasi membuat akun palsu untuk memperoleh komisi)
- Pelanggaran merek (afiliasi memasang iklan untuk istilah merek Anda dalam pencarian berbayar)
- Ketidaksesuaian merek (afiliasi mempromosikan produk Anda dalam konteks yang tidak tepat)

Untuk sebagian besar toko, mulai dengan **persetujuan manual** lebih aman. Anda selalu dapat mengaktifkan otomatis persetujuan nanti setelah Anda membangun pola kepercayaan.

## Ambang Batas Pembayaran Minimum

Ambang batas pembayaran minimum mencegah beban administratif dari memproses banyak pembayaran kecil.

### Mengapa Menetapkan Ambang Batas

- **Mengurangi biaya transaksi** — Pemroses pembayaran mengenakan biaya per transaksi, sehingga menggabungkan pembayaran menghemat uang
- **Menyederhanakan akuntansi** — Pembayaran yang lebih sedikit berarti lebih sedikit pekerjaan rekonsiliasi
- **Standar industri** — Sebagian besar program afiliasi memiliki ambang batas ($25–$100)

### Ambang Batas Tipe

| Ambang Batas | Kasus Penggunaan |
|-----------|----------|
| **$25–$50** | Program volume tinggi di mana afiliasi mencapai ambang batas dengan cepat |
| **$50–$100** | Ambang batas standar untuk sebagian besar program |
| **$100–$200** | Program premium atau pembayaran internasional dengan biaya pemrosesan tinggi |

### Menyeimbangkan Kepuasan Afiliasi

Menetapkan ambang batas **terlalu tinggi** menyebabkan afiliasi frustrasi yang mungkin harus menunggu bulan untuk menerima pembayaran pertama mereka. Menetapkan ambang batas **terlalu rendah** menciptakan beban administratif dan mengurangi margin Anda dengan biaya.

**Rekomendasi:** Mulai dari $50. Ini cukup rendah sehingga afiliasi aktif mencapainya dalam beberapa penjualan pertama mereka, tetapi cukup tinggi untuk menggabungkan pembayaran secara efisien.

### Tidak Ada Batas Maksimum

Tidak ada batas maksimum — afiliasi dapat mengumpulkan pendapatan secara tak terbatas sebelum meminta pembayaran. Beberapa afiliasi lebih suka menggabungkan permintaan mereka setiap kuartal atau tahunan untuk perencanaan pajak.

## Manajemen Status Program

Program dapat berada dalam salah satu dari tiga status:

| Status | Deskripsi | Perilaku |
|--------|-------------|----------|
| **Aktif** | Program sedang berjalan | Menerima afiliasi baru, melacak referensi, menghitung komisi |
| **Dijeda** | Didesak sementara | Afiliasi yang ada tetap berada, tetapi tidak ada pendaftaran baru; cookie referensi yang ada masih berfungsi |
| **Diarsipkan** | Ditutup secara permanen | Tidak ada afiliasi baru, tidak ada referensi baru yang dilacak; data historis disimpan untuk pelaporan |

### Kapan Mendaftarkan Program

- Anda sedang merevisi tingkat komisi atau ketentuan
- Anda melebihi anggaran pembayaran afiliasi untuk kuartal ini
- Anda sedang menguji struktur program baru dan ingin mencegah afiliasi baru bergabung dengan struktur lama

Program yang dijeda masih mematuhi cookie pelacakan yang ada dan komisi yang belum selesai — Anda hanya mencegah afiliasi baru bergabung.

### Kapan Mengarsipkan Program

- Anda telah menggantikan program dengan struktur baru
- Program tersebut memiliki batas waktu (misalnya, kampanye musiman)
- Anda sedang menggabungkan beberapa program menjadi satu

Program yang diarsipkan tetap ada di database untuk pelaporan historis tetapi dihapus dari tampilan manajemen aktif.

## Contoh Program

### Contoh 1: Program Pengaruh (Persentase)

| Bidang | Nilai |
|-------|-------|
| Nama | Program Pengaruh |
| Jenis Komisi | Persentase |
| Nilai Komisi | 10 |
| Umur Cookie dalam Hari | 30 |
| Otomatis Persetujuan | Tidak dicentang (tinjauan manual) |
| Ambang Batas Pembayaran Minimum | 50.00 |
| Status | Aktif |

**Kasus Penggunaan:** Rekrut pengaruh media sosial dan pembuat konten. Komisi 10% berkembang seiring nilai pesanan, memperbaiki afiliasi yang menarik pelanggan dengan pengeluaran tinggi. Persetujuan manual memastikan Anda meninjau audiens dan keselarasan merek setiap pengaruh.

### Contoh 2: Program Referensi dalam Jumlah Besar (Jumlah Tetap)

| Bidang | Nilai |
|-------|-------|
| Nama | Program Mitra Referensi |
| Jenis Komisi | Jumlah Tetap |
| Nilai Komisi | 25.00 |
| Umur Cookie dalam Hari | 7 |
| Otomatis Persetujuan | Dicentang |
| Ambang Batas Pembayaran Minimum | 100.00 |
| Status | Aktif |

**Kasus Penggunaan:** Bermitra dengan situs penawaran, agregator kupon, dan jaringan referensi yang mendorong volume tinggi. Komisi tetap $25 menjaga biaya prediktabel, dan masa berlaku cookie pendek (7 hari) menargetkan konversi cepat. Otomatis persetujuan diaktifkan karena mitra ini biasanya melayani diri sendiri.

### Contoh 3: Mitra Premium (Persentase Tinggi)

| Bidang | Nilai |
|-------|-------|
| Nama | Tingkat Mitra Premium |
| Jenis Komisi | Persentase |
| Nilai Komisi | 15 |
| Umur Cookie dalam Hari | 90 |
| Otomatis Persetujuan | Tidak dicentang |
| Ambang Batas Pembayaran Minimum | 200.00 |
| Status | Aktif |

**Kasus Penggunaan:** Program eksklusif untuk afiliasi top-performing atau mitra strategis. Komisi yang lebih tinggi (15%) memperbaiki lalu lintas kualitas mereka, dan masa berlaku cookie 90 hari menampung siklus pertimbangan yang lebih lama. Hanya persetujuan manual — ini adalah tingkat undangan saja.

## Tips

- Mulai dengan **komisi persentase** (5–15%) untuk sebagian besar program — lebih mudah dijelaskan kepada afiliasi dan berkembang secara alami seiring nilai pesanan.
- Gunakan **masa berlaku cookie 30 hari** sebagai dasar — ini adalah standar industri dan menyeimbangkan atribusi yang adil dengan batas pelacakan yang praktis.
- Aktifkan **persetujuan manual** awalnya untuk meninjau afiliasi, lalu beralih ke otomatis persetujuan setelah Anda membangun pola kepercayaan dan kontrol penipuan.
- Tetapkan **ambang batas pembayaran** Anda ke $50–$100 untuk menyeimbangkan kepuasan afiliasi (tidak terlalu tinggi untuk mencapai) dengan efisiensi administratif (tidak terlalu banyak pembayaran kecil).
- Buat **program terpisah** untuk segmen afiliasi yang berbeda (pengaruh, situs konten, agregator penawaran) sehingga Anda dapat melacak kinerja dan menyesuaikan komisi secara independen.
- Pantau **dashboard analitik** secara teratur untuk menemukan afiliasi berkinerja tinggi dan menyesuaikan tingkat komisi untuk mempertahankan mitra terbaik.

Ingat: Pertahankan semua format markdown, jalur gambar, blok kode, dan istilah teknis secara tepat seperti yang ditunjukkan dalam aturan preservasi.