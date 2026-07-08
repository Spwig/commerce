---
title: Optimasi Kinerja Pencarian
---

Kinerja pencarian secara langsung memengaruhi pengalaman pelanggan dan konversi. Pencarian yang lambat menyebabkan kekecewaan pelanggan dan meningkatkan tingkat keluar. Panduan komprehensif ini mengidentifikasi hambatan kinerja umum dalam sistem pencarian bertenaga database Spwig, menyediakan strategi optimasi, dan menetapkan target kinerja. Gunakan panduan ini ketika waktu respons pencarian melebihi ambang batas yang dapat diterima atau Anda sedang merencanakan pertumbuhan katalog.

Waktu respons target: <200ms autocomplete, <500ms pencarian penuh. Ikuti daftar pemeriksaan optimasi di bawah ini untuk mencapai target ini.

## Memahami Metrik Kinerja

Pantau metrik ini di **Pencarian > Analitik Pencarian**:

**Waktu Respons** - Milidetik untuk menjalankan query pencarian (hanya sisi server, tidak termasuk latensi jaringan)

**Persentase Cache Hit** - Persentase pencarian yang disajikan dari cache vs database

**Jumlah Query** - Jumlah query database per pencarian (semakin sedikit semakin baik)

**Waktu Query Database** - Waktu yang dihabiskan di database vs kode aplikasi

## Target Kinerja

| Jenis Query | Target | Dapat Diterima | Memerlukan Optimasi |
|------------|--------|------------|----------------------|
| Autocomplete | <200ms | 200-300ms | >300ms secara konsisten |
| Pencarian Penuh | <500ms | 500-800ms | >800ms secara konsisten |
| Pencarian Admin | <1000ms | 1000-1500ms | >1500ms secara konsisten |

Jika rata-rata waktu respons Anda melebihi ambang batas 'Memerlukan Optimasi', terapkan strategi di bawah ini.

## Memantau Kinerja

**Rata-rata Waktu Respons Dashboard Analitik**

Navigasikan ke **Pencarian > Analitik Pencarian** untuk melihat rata-rata waktu respons untuk semua pencarian. Ini adalah metrik utama pemantauan kinerja Anda.

**Kapan Harus Diinvestigasi**: Rata-rata waktu respons >300ms untuk autocomplete atau >800ms untuk pencarian penuh secara konsisten selama beberapa hari.

**Pemantauan Mingguan**: Tinjau analitik setiap Senin untuk menangkap degradasi kinerja sejak dini.

## Hambatan Kinerja yang Diketahui

Pencarian bertenaga database Spwig memiliki beberapa hambatan yang terdokumentasi untuk dihindari:

### Perhitungan CTR N+1 Query

**Apa Itu**: Perhitungan tingkat klik (CTR) di AnalyticsService menjalankan query terpisah untuk setiap item hasil agregasi.

**Dampak**: Sangat berdampak pada toko dengan lalu lintas tinggi yang memiliki banyak query yang dilacak.

**Lokasi Kode**: `search/services/analytics_service.py` - metode `get_click_through_rate()`

**Pengurangan Dampak**: Hindari memanggil perhitungan CTR di produksi. Ini sebagian besar fitur analitik admin yang harus dihitung secara asinkron, bukan selama permintaan menghadap ke pelanggan.

### Agregasi Stok

**Apa Itu**: `with_stock_totals()` menghitung jumlah on_hand di semua gudang per produk.

**Dampak**: Mahal untuk katalog >1.000 produk. Dipanggil ketika filter `in_stock` digunakan atau status stok ditampilkan dalam autocomplete.

**Pemicu**: **Pengaturan Pencarian > Autocomplete** - opsi 'Tampilkan Status Stok'

**Rekomendasi**: JANGAN AKTIFKAN status stok dalam autocomplete untuk katalog besar. Menambahkan 200-500ms per permintaan.

### Penggabungan Variant

**Apa Itu**: Pencarian SKU memicu JOIN pada tabel variant untuk mencari SKU variant.

**Dampak**: 2-3x lebih lambat pada produk dengan banyak variant (10+ variant per produk).

**Pengurangan Dampak**: Menggunakan `.distinct()` untuk menghindari duplikat, yang menambahkan beban. Diperlukan untuk fungsi SKU - jangan matikan kecuali SKU tidak digunakan.

### Jumlah Produk dalam Autocomplete

**Apa Itu**: Hasil autocomplete kategori/merek menampilkan jumlah produk ('Elektronik (234)').

**Dampak**: Setiap jenis konten dengan jumlah yang diaktifkan menambahkan 2 query tambahan. Query termasuk penggabungan dan agregasi.

**Pemicu**: **Pengaturan Pencarian > Autocomplete** - 'Tampilkan Jumlah Produk' untuk kategori/merek

**Rekomendasi**: Matikan jumlah produk. Menyimpan 2-4 query per permintaan autocomplete. Optimasi autocomplete terbesar.

### Indeks Dokumen

**Apa Itu**: Ekstraksi teks dari file PDF/DOCX/XLSX selama query pencarian.

**Dampak**: Sangat mahal (I/O file + ekstraksi teks). Operasi penguncian sinkron.

**Pemicu**: **Pengaturan Pencarian > Indeks Mendalam** - 'Indeks Dokumen'

**Rekomendasi**: Hampir tidak pernah sepadan dengan biaya kinerja. AKTIFKAN HANYA JIKA KATALOG PRODUK DIGITAL KECIL (<500 produk) setelah pengujian menyeluruh.

## Konfigurasi Cache

Caching adalah optimasi kinerja paling efektif tunggal.

**Cache Autocomplete** - Default: 60s
- **Rentang Direkomendasikan**: 45-90s
- **TTL Lebih Tinggi (90-120s)**: Kinerja lebih baik jika perubahan inventaris jarang terjadi
- **TTL Lebih Rendah (30-45s)**: Hasil lebih mutakhir jika menambahkan produk setiap jam

**Cache Hasil** - Default: 300s (5 menit)
- **Rentang Direkomendasikan**: 180-600s
- **TTL Lebih Tinggi (600s/10menit)**: Peningkatan kinerja signifikan untuk katalog statis
- **TTL Lebih Rendah (180s)**: Lebih mutakhir jika sering memperbarui data produk

**Strategi Optimasi**: Jika pencarian lambat, gandakan TTL cache sebelum menonaktifkan fitur. Beralih dari 60s → 120s cache autocomplete mengurangi beban database sebesar setengah.

## Daftar Pemeriksaan Optimasi Autocomplete

Terapkan perubahan ini pada pengaturan autocomplete untuk kinerja maksimal:

**1. Tingkatkan Debounce ke 300-400ms**
- Lokasi: **Pengaturan Pencarian > Autocomplete** - 'Debounce Delay'
- Dampak: Mengurangi panggilan API dengan menunggu lebih lama antara ketik
- Pertukaran: Sedikit kurang responsif (tidak terlihat oleh sebagian besar pengguna)

**2. Kurangi Max Results dari 8 menjadi 5-6**
- Lokasi: **Pengaturan Pencarian > Autocomplete** - 'Max Results Per Type'
- Dampak: Himpunan hasil yang lebih kecil = query lebih cepat dan payload JSON lebih kecil
- Pertukaran: Opsi yang ditampilkan lebih sedikit (biasanya cukup)

**3. Matikan Jumlah Produk (KEUNTUNGAN TERBESAR)**
- Lokasi: **Pengaturan Pencarian > Autocomplete** - Hilangkan centang 'Tampilkan Jumlah Produk' untuk kategori/merek
- Dampak: Menyimpan 2-4 query per permintaan autocomplete
- Pertukaran: Tidak ada jumlah produk dalam dropdown (jarang diperlukan)

**4. Matikan Status Stok**
- Lokasi: **Pengaturan Pencarian > Autocomplete** - Hilangkan centang 'Tampilkan Status Stok'
- Dampak: Menghilangkan agregasi stok yang mahal
- Pertukaran: Tidak ada badge stok (tidak kritis dalam konteks autocomplete)

**5. Matikan Deskripsi Produk**
- Lokasi: **Pengaturan Pencarian > Autocomplete** - Hilangkan centang 'Tampilkan Deskripsi'
- Dampak: Mengurangi pemrosesan teks dan ukuran payload
- Pertukaran: Teks pratinjau lebih sedikit (nama produk biasanya cukup)

**6. Tingkatkan TTL Cache ke 90s**
- Lokasi: **Pengaturan Pencarian > Caching** - 'Autocomplete Cache TTL'
- Dampak: Lebih banyak permintaan yang dilayani dari cache
- Pertukaran: Hasil hingga 90 detik tidak mutakhir (diterima untuk sebagian besar toko)

**Peningkatan yang Diharapkan**: Menerapkan semua 6 optimisasi biasanya mengurangi waktu respons autocomplete sebesar 50-70%.

## Optimasi Indeks Mendalam

Setiap opsi indeks mendalam menambahkan beban. Nonaktifkan berdasarkan ukuran katalog:

| Ukuran Katalog | Indeks Mendalam yang Direkomendasikan |
|--------------|---------------------------|
| **<1.000 produk** | Semua AKTIF (dampak minimal) |
| **1.000-10.000** | Pertahankan SKU, Atribut, Bidang Kustom AKTIF; Nonaktifkan Ulasan |
| **10.000-20.000** | Pertahankan SKU, Atribut AKTIF; Nonaktifkan Bidang Kustom, Ulasan |
| **20.000-50.000** | Pertahankan SKU AKTIF hanya; Nonaktifkan semua yang lain |
| **>50.000** | Pertahankan SKU AKTIF; Pertimbangkan migrasi ke Elasticsearch |

**Indeks Dokumen**: SELALU MATIKAN kecuali kritis (produk digital dengan dokumen yang dapat dicari DAN <500 produk total).

## Optimasi Jenis Konten

Nonaktifkan jenis konten yang tidak digunakan di **Pengaturan Pencarian > Jenis Konten**:

- **Tidak ada blog?** Nonaktifkan 'Pos Blog' - menghemat query
- **Tidak ada penyaring merek?** Nonaktifkan 'Merek' - menghemat query
- **Toko hanya berbelanja?** Nonaktifkan 'Kategori' dan 'Pos Blog'

Setiap jenis konten yang dinonaktifkan menghilangkan query database dari setiap pencarian.

## Optimasi Database

Spwig membuat indeks yang diperlukan melalui migrasi. Percayalah pada mereka - jangan buat indeks tambahan tanpa profiling.

**Pemeliharaan PostgreSQL** (jika menggunakan PostgreSQL):
- Jalankan `VACUUM ANALYZE` mingguan untuk memperbarui statistik perencana query
- Katalog besar manfaat dari `VACUUM FULL` bulanan (memerlukan downtime)

**Pantau Waktu Query Database**: Selama pengembangan, identifikasi query lambat menggunakan alat profiling. Sebagian besar optimasi query sudah diimplementasikan:
- `.select_related('brand', 'category')` pada produk
- `.prefetch_related('images')` untuk thumbnail
- `.distinct()` untuk pencarian variant

## Kinerja Pemadanan Fuzzy

Jarak Levenshtein secara komputasi mahal (kompleksitas O(m*n)):

**Optimasi Ambang Batas**:
- **Ambang batas lebih tinggi (0,85 vs 0,80)**: Lebih cepat tetapi menangkap lebih sedikit ejaan salah
- **Ambang batas lebih rendah (0,75 vs 0,80)**: Lebih lambat tetapi lebih toleran

**Optimasi Maksimal Edits**:
- **Maksimal edits lebih rendah (1 vs 2)**: Lebih cepat tetapi melewatkan lebih banyak ejaan salah
- **Maksimal edits lebih tinggi (2 vs 3)**: Lebih lambat tetapi menangkap lebih banyak ejaan salah

**Kinerja Perpustakaan**: Spwig menggunakan `rapidfuzz` jika tersedia (10x lebih cepat daripada Python murni). Pastikan terinstal: `pip install rapidfuzz`

## Kinerja Sinonim dan Redirect

**Ekspansi Query Sinonim**: Setiap sinonim menambahkan klausa OR ke query pencarian. Batasi hingga 10-20 sinonim per istilah maksimal.

**Jenis Pemadanan Regex**: Redirect regex lebih lambat daripada exact/contains/starts_with. Hindari pola kompleks.

**Rekomendasi**: Gunakan jenis pemadanan sederhana sebisa mungkin. Cadangkan regex untuk kasus di mana jenis pemadanan lain tidak berfungsi.

## Optimasi Katalog Besar (>10.000 produk)

Strategi khusus untuk katalog besar:

**1. Caching Agresif**
- Autocomplete: TTL 90-120s
- Hasil: TTL 600s (10menit)
- Terima ketidakmutakhiran untuk kinerja

**2. Indeks Mendalam Minimal**
- Hanya SKU (nonaktifkan atribut, bidang kustom, ulasan)
- Uji kinerja dengan/ tanpa atribut

**3. Hasil Autocomplete yang Dikurangi**
- Maksimal 5 hasil per jenis (dari 8)
- Mengurangi beban query

**4. Matikan Status Stok di Semua Tempat**
- Di autocomplete
- Di hasil pencarian jika ditampilkan

**5. Pertimbangkan Elasticsearch di >50K Produk**
- Pencarian bertenaga database cocok hingga sekitar 50.000 produk
- Di luar itu, Elasticsearch direkomendasikan untuk:
  - Pencarian berbasis facet kompleks
  - Beban pencarian bersamaan tinggi (>100 pencarian per detik)
  - Waktu respons konsisten >500ms meskipun optimisasi

## Kinerja Multi-Bahasa

Indeks JSONField JSONB (PostgreSQL) membuat multi-bahasa efisien:

- **1-3 bahasa**: Overhead minimal (5-10ms)
- **5+ bahasa**: Peningkatan kecil dalam kompleksitas query (20-40ms)
- **10+ bahasa**: Overhead yang terlihat (50-100ms)

Overhead meningkat secara linear dengan jumlah bahasa.

## Perbaikan Kinerja Darurat

Jika pencarian sangat lambat (>2s waktu respons), terapkan perbaikan segera berikut ini dalam urutan:

**Segera** (terapkan sekarang):
1. Matikan indeks dokumen
2. Matikan jumlah produk dalam autocomplete
3. Tingkatkan TTL cache ke 120s autocomplete / 600s hasil

**Cepat** (terapkan dalam 24 jam):
4. Matikan status stok dalam autocomplete
5. Kurangi jumlah maksimal autocomplete ke 5
6. Matikan deskripsi produk dalam autocomplete

**Sedang** (terapkan dalam seminggu):
7. Matikan indeks ulasan jika >20K produk
8. Tinjau dan nonaktifkan jenis konten yang tidak digunakan
9. Tingkatkan debounce ke 400ms

**Peningkatan yang Diharapkan**: 9 perbaikan ini biasanya mengurangi waktu respons sebesar 60-80% pada katalog besar.

## Tips

- **Pantau waktu respons mingguan** - Menangkap degradasi kinerja sejak dini
- **Peningkatan cache adalah optimasi pertama** - Menggandakan TTL cache adalah kemenangan tercepat
- **Jumlah produk dalam autocomplete = mahal** - Pembunuh kinerja autocomplete terbesar
- **Indeks dokumen hampir tidak pernah sepadan** - Biaya kinerja jarang membenarkan manfaat
- **Uji satu perubahan sekaligus** - Tidak dapat mengidentifikasi sebab/akibat dengan perubahan bersamaan
- **Benchmark dengan volume data yang realistis** - Uji dengan katalog ukuran produksi
- **Agregasi stok mematikan kinerja pada katalog besar** - Hindari menampilkan stok dalam autocomplete
- **Pertimbangkan Elasticsearch pada 50K+ produk** - Pencarian bertenaga database memiliki batasan

Ingat: Pertahankan semua format markdown, jalur gambar, blok kode, dan istilah teknis persis seperti yang ditunjukkan dalam aturan preservasi.