---
title: Mengelola Sinonim dan Redirect
---

Sinonim dan redirect membuat pencarian Anda lebih cerdas dengan menangani istilah yang setara dan mengarahkan pertanyaan spesifik ke halaman yang ditargetkan. Sinonim memperluas pencarian untuk mencakup istilah terkait ("laptop" juga menemukan "notebook"), sementara redirect mengirimkan pertanyaan seperti "sale" langsung ke halaman penjualan Anda. Panduan ini menjelaskan cara membuat dan mengelola fitur-fitur ini untuk meningkatkan relevansi pencarian dan pengalaman pelanggan.

Gunakan sinonim untuk kesetaraan istilah dan redirect untuk pintasan navigasi.

![Daftar Sinonim](/static/core/admin/img/help/managing-synonyms-redirects/synonym-list.webp)

## Memahami Sinonim

Sinonim memberi tahu sistem pencarian bahwa istilah tertentu harus dianggap setara. Ketika pelanggan mencari satu istilah, sistem secara otomatis mencakup hasil yang cocok dengan istilah sinonim.

**Contoh**: Buat peta sinonim "laptop" → "notebook", "portable computer". Sekarang ketika seseorang mencari "laptop", mereka juga mendapatkan hasil untuk produk yang mengandung "notebook" atau "portable computer" dalam nama atau deskripsi mereka.

Sinonim sangat bernilai untuk:
- Bahasa Inggris Britania vs Amerika (jumper/sweater, trainers/sneakers)
- Istilah merek vs umum (tissues/Kleenex)
- Kesalahan umum (accommodate/accomodate)
- Jargon industri vs bahasa umum (CPU/processor)

## Membuat Sinonim

Navigasi ke **Search > Synonyms** dan klik **+ Add Synonym**.

![Form Tambah Sinonim](/static/core/admin/img/help/managing-synonyms-redirects/synonym-form.webp)

**Term** - Istilah pencarian asli yang memicu ekspansi sinonim

**Sinonyms** - Array JSON dari istilah setara, contoh: `['sweater', 'pullover', 'jumper']`

**Bidirectional** - Default: Dicentang. Ketika diaktifkan, hubungan sinonim berfungsi dua arah:
- Cari "laptop" menemukan produk "notebook"
- Cari "notebook" menemukan produk "laptop"

Batalkan pemeriksaan untuk peta satu arah (lihat di bawah).

**Language** - Opsional. Batasi sinonim ini untuk pencarian dalam bahasa tertentu. Biarkan kosong untuk menerapkannya ke semua bahasa.

**Engine** - Opsional. Batasi sinonim ini ke mesin pencari tertentu. Biarkan kosong untuk menerapkannya secara global.

**Active** - Apakah sinonim ini saat ini digunakan. Batalkan pemeriksaan untuk menonaktifkan sementara tanpa menghapus.

## Contoh Sinonim Dua Arah

Sebagian besar sinonim harus dua arah - kesetaraan sebenarnya yang berfungsi dalam kedua arah:

| Term | Sinonyms | Use Case |
|------|----------|----------|
| laptop | notebook, portable computer | Bahasa Inggris Amerika/Britania + istilah umum |
| sofa | couch, settee | Variasi regional |
| trainers | sneakers, running shoes | Bahasa Inggris UK/US |
| mobile | cell phone, cellular | Variasi internasional |

Dengan bidirectional diaktifkan, semua istilah ini menemukan produk yang sama terlepas dari istilah yang digunakan pelanggan.

## Contoh Sinonim Satu Arah

Batalkan pemeriksaan "Bidirectional" untuk hubungan satu arah:

**Kasus Penggunaan Umum**:
- **Kesalahan Ejaan**: Term: "acco

mmodate" → Sinonyms: `['accommodate']` (satu arah sehingga ejaan yang benar tidak menemukan kesalahan ejaan)
- **Spesifik → Umum**: Term: "MacBook" → Sinonyms: `['laptop']` (MacBooks adalah laptop, tetapi tidak semua laptop adalah MacBooks)
- **Singkatan**: Term: "CPU" → Sinonyms: `['processor']` (CPU menemukan produk processor, tetapi pencarian processor tidak selalu mencakup CPU)

## Sinonim Berdasarkan Bahasa

Gunakan bidang Language untuk membuat sinonim yang sesuai dengan wilayah:

**Contoh**: Toko Bahasa Inggris Britania
- Term: "jumper", Sinonyms: `['sweater', 'pullover']`, Language: English (UK)
- Term: "trainers", Sinonyms: `['sneakers']`, Language: English (UK)

**Contoh**: Toko Multi-bahasa
- Term: "ordinateur portable", Sinonyms: `['laptop', 'notebook']`, Language: French
- Term: "zapatos", Sinonyms: `['shoes']`, Language: Spanish

Sinonim berdasarkan bahasa hanya berlaku ketika pelanggan menjelajah dalam bahasa tersebut.

## Sinonim Berdasarkan Mesin

Sebagian besar sinonim harus berlaku secara global (biarkan bidang Engine kosong). Gunakan sinonim berdasarkan mesin hanya ketika konteks pencarian yang berbeda memerlukan peta istilah yang berbeda:

**Contoh**: Anda memiliki mesin "shop" dan "blog" terpisah
- Sinonim blog: Term: "tutorial" → Sinonyms: `['guide', 'how-to']`, Engine: blog
- Sinonim ini hanya berlaku untuk pencarian blog, bukan pencarian produk

## Memahami Redirect

Redirect pencarian mengirimkan pertanyaan spesifik langsung ke halaman yang ditentukan, melewati hasil pencarian normal. Gunakan redirect ketika Anda tahu persis di mana pelanggan harus pergi.

**Contoh**: Buat redirect untuk "sale" → "/products/sale/". Sekarang ketika seseorang mencari "sale", mereka melewati hasil pencarian dan langsung mendarat di halaman penjualan Anda.

Redirect sangat cocok untuk:
- Pintasan navigasi umum ("returns" → halaman kebijakan pengembalian)
- Promosi musiman ("summer sale" → koleksi musim panas)
- Kategori populer ("laptops" → halaman kategori laptop)
- Halaman kebijakan ("shipping" → informasi pengiriman)

![Daftar Redirect](/static/core/admin/img/help/managing-synonyms-redirects/redirect-list.webp)

## Jenis Pemadanan

Redirect mendukung empat jenis pemadanan yang mengontrol seberapa ketat pencarian harus cocok:

**Exact** - Pemadanan tepat tanpa memperhatikan huruf besar-kecil. Pertanyaan harus tepat cocok dengan istilah (mengabaikan kapitalisasi).
- Term: "sale"
- Cocok: "sale", "SALE", "Sale"
- Tidak cocok: "summer sale", "on sale"

**Contains** - Pertanyaan mengandung istilah di mana saja.
- Term: "sizing"
- Cocok: "sizing guide", "help with sizing", "what sizing"
- Tidak cocok: "size chart" (kata berbeda)

**Starts With** - Pertanyaan dimulai dengan istilah.
- Term: "return"
- Cocok: "returns", "return policy", "returning items"
- Tidak cocok: "how to return" (tidak dimulai dengan istilah)

**Regex** - Pemadanan pola menggunakan ekspresi reguler. **⚠️ Peringatan kinerja** - pola regex yang kompleks memperlambat pencarian. Gunakan secara hati-hati.
- Pola: `^(laptop|notebook)s?$`
- Cocok: "laptop", "laptops", "notebook", "notebooks"
- Gunakan hanya jika jenis pemadanan lain tidak bekerja

## Membuat Redirect

Navigasi ke **Search > Redirects** dan klik **+ Add Redirect**.

![Form Tambah Redirect](/static/core/admin/img/help/managing-synonyms-redirects/redirect-form.webp)

**Term** - Pertanyaan pencarian yang cocok

**Match Type** - Exact, Contains, Starts With, atau Regex (lihat di atas)

**Redirect URL** - Ke mana pelanggan akan dikirim. Bisa relatif (`/products/sale/`) atau absolut (`https://example.com/page/`)

**Redirect Type** - Kode status HTTP:
- **302 (Sementara)**: Direkomendasikan. Browser tidak menyimpan cache, Anda dapat mengubah tujuan nanti
- **301 (Permanen)**: Browser dan mesin pencari menyimpan cache. Hanya gunakan untuk redirect permanen

**Engine** - Opsional. Batasi ke mesin pencari tertentu

**Hit Count** - Otomatis meningkat setiap kali redirect ini digunakan. Membantu mengidentifikasi pintasan navigasi yang paling digunakan.

**Active** - Aktifkan/matikan redirect ini

## Contoh Redirect

| Term | Match Type | URL | Use Case |
|------|-----------|-----|----------|
| sale | Exact | `/products/sale/` | Redirect pencarian "sale" ke halaman penjualan |
| clearance | Exact | `/clearance/` | Lewati pencarian untuk item diskon |
| sizing | Contains | `/pages/size-guide/` | Setiap pertanyaan tentang sizing pergi ke panduan |
| return | Starts With | `/pages/returns/` | Pertanyaan terkait pengembalian pergi ke kebijakan |

Semua menggunakan redirect 302 (sementara) untuk fleksibilitas.

## Jenis Redirect: 302 vs 301

**302 (Sementara)** - Direkomendasikan untuk sebagian besar redirect
- Browser membuat permintaan segar setiap kali
- Anda dapat mengubah URL tujuan kapan saja
- Pilihan yang lebih aman jika Anda tidak yakin

**301 (Permanen)** - Gunakan secara hati-hati
- Browser menyimpan redirect
- Mesin pencari memperbarui indeks mereka
- Lebih sulit untuk mengubah nanti

**Rekomendasi**: Gunakan 302 kecuali Anda yakin sekali bahwa redirect ini tidak akan pernah berubah.

## Analitik Hit Count

Bidang Hit Count otomatis meningkat setiap kali redirect ditembakkan. Gunakan ini untuk:
- Mengidentifikasi pintasan navigasi yang paling digunakan
- Menemukan redirect yang tidak pernah digunakan (pertimbangkan untuk menghapus)
- Menemukan pola pencarian populer

Ulas hit counts bulanan untuk mengoptimalkan strategi redirect Anda.

## Menemukan Kesempatan Sinonim

**Gunakan Pertanyaan Tanpa Hasil**: Navigasi ke **Search > Search Analytics** dan saring untuk pertanyaan tanpa hasil. Ini mengungkap:
- Istilah yang digunakan pelanggan yang tidak cocok dengan deskripsi produk Anda
- Variasi regional yang belum dipertimbangkan
- Kesalahan ejaan umum

**Workflow**:
1. Ulas pertanyaan tanpa hasil mingguan
2. Identifikasi pola (istilah yang muncul berulang kali)
3. Tambahkan sinonim untuk memetakan bahasa pelanggan ke nama produk Anda
4. Pantau apakah pertanyaan tanpa hasil berkurang

## Tips

- **Pantau pertanyaan tanpa hasil mingguan untuk ide sinonim** - Mereka mengungkap celah antara bahasa pelanggan dan deskripsi produk Anda
- **Mulai dengan sinonim umum, perluas berdasarkan data** - Mulai dengan variasi regional yang jelas, lalu tambahkan berdasarkan perilaku pencarian sebenarnya
- **Gunakan bidirectional untuk kesetaraan sebenarnya** - Sebagian besar sinonim harus berfungsi dua arah (laptop ↔ notebook)
- **Hindari pola regex yang kompleks** - Pemadanan regex lebih lambat daripada jenis pemadanan lain; gunakan hanya ketika diperlukan
- **Gunakan redirect 302 (sementara) secara default** - Memberi Anda fleksibilitas untuk mengubah tujuan nanti
- **Uji sinonim dengan pertanyaan nyata** - Cari istilah sinonim untuk memverifikasi bahwa mereka mengembalikan hasil yang diharapkan
- **Sinonim berdasarkan bahasa untuk toko multi-bahasa** - Buat peta istilah yang sesuai dengan wilayah untuk setiap bahasa yang didukung

Ingat: Pertahankan semua format markdown, jalur gambar, blok kode, dan istilah teknis tepat seperti yang ditunjukkan dalam aturan preservasi.