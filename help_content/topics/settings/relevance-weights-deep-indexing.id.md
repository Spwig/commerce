---
title: Bobot Relevansi dan Pemetaan Mendalam
---

Bobot relevansi dan pemetaan mendalam mengontrol bagaimana hasil pencarian dirangking dan data produk apa yang dicari. Bobot adalah pengali penting - bobot 2,0 berarti cocok di bidang tersebut dua kali lebih penting daripada bobot 1,0. Pemetaan mendalam menentukan apakah pencarian melihat lebih jauh dari nama produk dasar ke SKU, atribut, ulasan, bahkan konten dokumen. Panduan ini menjelaskan kedua sistem, kapan menyesuaikannya, dan implikasi kinerja kritis.

Default bekerja dengan baik untuk sebagian besar toko e-commerce. Hanya sesuaikan jika Anda memiliki kebutuhan peringkat atau pemetaan khusus.

![Tab Bobot](/static/core/admin/img/help/search-settings-overview/search-settings-weights.webp)

## Memahami Bobot

Bobot adalah pengali (skala 0,0-2,0) yang diterapkan saat cocok teks ditemukan di bidang berbeda. Bobot yang lebih tinggi berarti cocok di bidang tersebut dirangking lebih tinggi dalam hasil.

**Contoh**: Jika produk memiliki "laptop" di nama (bobot 1,50) dan deskripsi (bobot 0,80):
- Cocok nama berkontribusi 1,50 ke skor relevansi
- Cocok deskripsi berkontribusi 0,80
- Skor gabungan menentukan peringkat vs produk lain

Bobot memungkinkan Anda untuk memprioritaskan bidang tertentu dibandingkan bidang lain saat merangking hasil pencarian.

## Kategori Bobot dan Default

Navigasi ke **Pengaturan Pencarian > Tab Bobot** untuk melihat semua pengaturan bobot:

| Bidang | Bobot Default | Alasan |
|-------|---------------|-----------|
| **weight_name** | 1,50 | Nama produk paling penting - pelanggan mengharapkan cocok nama eksak di puncak |
| **weight_sku** | 1,20 | SKU adalah identifikasi spesifik - penting untuk B2B dan pelanggan kembali |
| **weight_description** | 0,80 | Deskripsi menyediakan konteks tetapi kurang penting daripada cocok nama eksak |
| **weight_categories** | 0,80 | Cocok kategori membantu untuk menjelajah tetapi tidak sebesar nama/SKU |
| **weight_attributes** | 0,70 | Pencarian warna, ukuran, bahan - berguna tetapi informasi pendukung |
| **weight_brands** | 0,70 | Penyaring merek penting tetapi bukan kriteria utama pencarian untuk sebagian besar toko |
| **weight_blog_posts** | 0,60 | Konten blog kurang penting dalam pencarian berorientasi e-commerce (prioritas terendah) |
| **weight_reviews** | 0,50 | Konten yang dibuat pengguna paling tidak terkontrol - bobot terendah |

Default ini mengasumsikan toko e-commerce umum di mana penemuan produk adalah tujuan pencarian utama.

## Kapan Menyesuaikan Bobot

Sesuaikan bobot saat prioritas toko Anda berbeda dari pola e-commerce umum:

**Toko Berbasis SKU (B2B, Eceran Besar)** - Tingkatkan `weight_sku` ke 1,8-2,0 sehingga pencarian kode produk mendominasi hasil. Pelanggan B2B sering mencari dengan SKU eksak.

**Toko Berbasis Merek** - Tingkatkan `weight_brands` ke 1,2-1,5 saat pelanggan utamanya berbelanja berdasarkan merek (pakaian desainer, barang mewah).

**Toko Berbasis Konten** - Tingkatkan `weight_blog_posts` ke 0,9-1,2 jika Anda adalah penerbit konten atau toko pendidikan di mana posting blog seberharga produk.

**Toko Berbasis Atribut (Fashion)** - Tingkatkan `weight_attributes` ke 1,0-1,2 saat pelanggan sering mencari berdasarkan atribut warna, ukuran, gaya.

## Contoh Penyesuaian Bobot

| Jenis Toko | Penyesuaian yang Direkomendasikan |
|-----------|------------------------|
| **B2B Eceran Besar** | weight_sku: 2,0, weight_name: 1,3, weight_description: 0,6 - Prioritaskan kode produk |
| **Boutique Pakaian** | weight_attributes: 1,2, weight_brands: 1,2, weight_name: 1,4 - Warna/gaya/merek penting |
| **Penerbit Konten** | weight_blog_posts: 1,2, weight_name: 1,3, weight_reviews: 0,7 - Konten seberharga produk |
| **E-commerce Umum** | Gunakan default - Seimbang untuk toko online umum |

Sesuaikan satu bobot pada satu waktu dan uji sebelum membuat perubahan tambahan.

## Ringkasan Pemetaan Mendalam

⚠️ **PERINGATAN KINERJA** - Setiap opsi pemetaan mendalam menambah kompleksitas dan beban kueri.

Pemetaan mendalam memperluas pencarian di luar nama/deskripsi produk dasar ke data tambahan:

![Tab Pemetaan Mendalam](/static/core/admin/img/help/search-settings-overview/search-settings-deep-indexing.webp)

Navigasi ke **Pengaturan Pencarian > Tab Pemetaan Mendalam** untuk mengonfigurasi.

## Indeks SKU

**Default**: ON, **Dampak Kinerja**: Rendah

Termasuk SKU produk dan variasi dalam indeks pencarian. Memicu JOIN variasi (biaya kecil).

**Kapan menonaktifkan**: Tidak pernah, kecuali Anda benar-benar tidak memiliki SKU yang ditetapkan. Dampak kinerja sangat kecil.

## Indeks Atribut

**Default**: ON, **Dampak Kinerja**: Sedang

Termasuk atribut produk (warna, ukuran, bahan, atribut kustom) dalam indeks pencarian. Bergabung ke tabel atribut.

**Kapan menonaktifkan**: Katalog >20.000 produk dengan banyak atribut per produk mungkin melihat 50-100ms beban tambahan. Hanya nonaktifkan jika kinerja kritis dan pelanggan tidak mencari berdasarkan atribut.

## Indeks Bidang Kustom

**Default**: ON, **Dampak Kinerja**: Sedang

Termasuk bidang kustom yang didefinisikan oleh pedagang dari JSONField dalam pencarian. Memerlukan perjalanan JSONField.

**Kapan menonaktifkan**: Jika Anda tidak menggunakan bidang kustom, atau bidang kustom berisi data yang tidak dapat dicari (catatan internal, kode akuntansi). Menonaktifkan menghemat beban pemrosesan JSONField.

## Indeks Ulasan

**Default**: ON, **Dampak Kinerja**: Sedang-Tinggi

Termasuk judul dan komentar ulasan yang disetujui dalam pencarian. Bergabung ke tabel ulasan dan menambahkan beban pencarian teks.

**Kapan menonaktifkan**: Katalog >20.000 produk atau toko dengan banyak ulasan per produk. Menambahkan 100-200ms beban tambahan pada katalog besar.

## Indeks Dokumen

**Default**: OFF, **Dampak Kinerja**: SANGAT TINGGI 🚨

**JANGAN AKTIFKAN SECARA SEMBARANG** - Fitur pencarian paling mahal.

Indeks dokumen mengekstrak teks dari file PDF, DOCX, dan XLSX yang terlampir ke produk digital, membuat konten file dapat dicari.

**Detail Teknis**:
- Menggunakan library PyPDF2, python-docx, dan openpyxl
- I/O file sinkron dan ekstraksi teks pada pencarian
- Melacak file melalui checksum MD5 (hanya mereindex saat file berubah)
- Potensi timeout pada file besar (>10MB PDFs)

**Dampak Kinerja**:
- Sangat mahal untuk indeks awal (menit hingga jam untuk perpustakaan besar)
- Beban kueri signifikan (latensi tambahan 100-500ms)
- Intensif memori untuk dokumen besar

**Hanya aktifkan jika**:
- Anda menjual produk digital dengan dokumen yang dapat dicari (buku elektronik, laporan, manual)
- Katalog kecil (<500 produk digital)
- Server memiliki sumber daya yang cukup
- Anda telah menguji dampak secara menyeluruh

**Untuk toko produk digital**: Pertimbangkan apakah pelanggan benar-benar membutuhkan untuk mencari konten dokumen, atau apakah mencari nama/deskripsi produk sudah cukup.

## Tabel Dampak Kinerja

| Fitur | Default | Dampak | Gunakan Saat |
|---------|---------|--------|----------|
| Indeks SKU | ON | Rendah | Selalu (Esensial untuk B2B) |
| Indeks Atribut | ON | Sedang | Produk yang dapat dikonfigurasi |
| Indeks Bidang Kustom | ON | Sedang | Menggunakan bidang kustom |
| Indeks Ulasan | ON | Sedang-Tinggi | Toko berbasis ulasan |
| Indeks Dokumen | OFF | Sangat Tinggi | Hanya untuk produk digital (uji terlebih dahulu) |

Dampak diasumsikan katalog umum. Katalog besar (>50.000 produk) mengalami beban tambahan yang proporsional lebih tinggi.

## Uji Perubahan Bobot

Ketika menyesuaikan bobot, ikuti alur pengujian berikut:

1. **Ubah satu bobot pada satu waktu** - Jangan sesuaikan beberapa bobot secara bersamaan; Anda tidak akan tahu perubahan apa yang menyebabkan hasil
2. **Peningkatan kecil** - Sesuaikan dengan ±0,2 pada satu waktu (misalnya, 1,0 → 1,2, bukan 1,0 → 1,8)
3. **Uji dengan kueri nyata** - Gunakan istilah pencarian pelanggan sebenarnya dari analitik, bukan uji acak
4. **Pantau analitik** - Bandingkan relevansi hasil sebelum/demikian menggunakan kueri teratas
5. **Tunggu 1-2 minggu** - Beri waktu pelanggan untuk berinteraksi dengan peringkat baru
6. **Ukur tingkat klik-through** - Apakah pelanggan mengklik hasil lebih/lebih sedikit daripada sebelumnya?

## Kompromi Kinerja vs Akurasi

Lebih banyak indeks = hasil pencarian yang lebih baik tetapi kinerja yang lebih lambat:

**Skenario: Katalog Kecil (<1.000 produk)**
- Aktifkan semua opsi indeks (SKU, atribut, bidang kustom, ulasan)
- Dampak kinerja minimal
- Kemampuan pencarian menyeluruh

**Skenario: Katalog Menengah (1.000-10.000 produk)**
- Biarkan SKU, atribut, bidang kustom tetap aktif
- Pertimbangkan menonaktifkan ulasan jika rata-rata >10 ulasan per produk
- Pantau waktu respons

**Skenario: Katalog Besar (>10.000 produk)**
- Biarkan SKU aktif (dampak rendah)
- Nonaktifkan indeks ulasan (dampak tinggi)
- Nonaktifkan bidang kustom jika tidak digunakan
- JANGAN AKTIFKAN indeks dokumen
- Pertimbangkan Elasticsearch pada >50.000 produk

Seimbangkan berdasarkan ukuran katalog dan sumber daya server Anda.

## Penyesuaian Bobot Berdasarkan Mesin

Ketika membuat mesin pencarian melalui wizard (Langkah 3), Anda dapat menyesuaikan bobot global untuk mesin tersebut.

**Kasus Penggunaan**: Mesin berbasis blog
- Buat mesin "blog"
- Ubah `weight_blog_posts` ke 1,5 (vs global 0,60)
- Konten blog sekarang dirangking lebih tinggi dalam pencarian mesin blog

Sebagian besar mesin TIDAK boleh menyesuaikan bobot - biarkan kosong untuk mewarisi pengaturan global.

## Tips

- **JANGAN aktifkan indeks dokumen kecuali sangat kritis** - Biaya kinerja tertinggi dari fitur pencarian apa pun
- **Toko B2B: Tingkatkan weight_sku ke 2,0** - Kode produk adalah metode pencarian utama
- **Uji perubahan bobot selama jam lalu lintas rendah** - Amati dampak kinerja sebelum jam sibuk
- **Pantau waktu respons setelah mengaktifkan indeks** - Periksa dashboard analitik untuk perlambatan
- **Nonaktifkan indeks ulasan pada katalog >20K produk** - Dampak kinerja signifikan
- **Sesuaikan satu bobot pada satu waktu untuk pengujian** - Tidak bisa menentukan sebab/akibat dengan perubahan bersamaan
- **Ekstraksi dokumen memerlukan PyPDF2/docx/openpyxl** - Verifikasi library ini terinstal sebelum mengaktifkan indeks dokumen

Ingat: Pertahankan semua format markdown, jalur gambar, blok kode, dan istilah teknis tepat seperti yang ditunjukkan dalam aturan preservasi.