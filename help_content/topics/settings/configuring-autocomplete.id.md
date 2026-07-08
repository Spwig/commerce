---
title: Mengatur Otomatisasi Pencarian
---

Otomatisasi pencarian, juga disebut pencarian prediktif atau pencarian saat mengetik, menampilkan hasil saat pelanggan mengetikkan pertanyaan mereka. Ini secara dramatis meningkatkan pengalaman pengguna dengan membantu pelanggan menemukan produk lebih cepat dan mengurangi pencarian tanpa hasil. Panduan ini menjelaskan cara mengonfigurasi perilaku otomatisasi pencarian, pengaturan tampilan, dan kompromi kinerja.

Otomatisasi pencarian diaktifkan secara default dengan pengaturan yang masuk akal. Hanya ubah jika Anda memiliki kekhawatiran kinerja atau preferensi tampilan tertentu.

![Pengaturan Otomatisasi Pencarian](/static/core/admin/img/help/configuring-autocomplete/autocomplete-settings-main.webp)

## Mengaktifkan Otomatisasi Pencarian

Navigasikan ke **Search > Search Settings** dan klik tab **Autocomplete**.

**Enable Autocomplete** - Toggle utama untuk pencarian prediktif. Saat diaktifkan, input pencarian menampilkan dropdown hasil saat pelanggan mengetik.

**Max Results Per Type** - Default: 8 item. Berapa banyak hasil yang ditampilkan untuk setiap jenis konten (produk, kategori, merek, posting blog). Nilai yang lebih rendah (5-6) mengurangi ukuran payload API dan mempercepat rendering. Nilai yang lebih tinggi (10-12) memberi pelanggan lebih banyak pilihan tetapi memperlambat respons.

## Waktu Debounce

⚠️ **PERINGATAN KINERJA** - Waktu debounce memengaruhi beban server secara signifikan.

**Debounce Delay** - Default: 300ms. Berapa lama menunggu setelah tombol terakhir diketik sebelum memicu permintaan otomatisasi pencarian.

Pengaturan ini menyeimbangkan responsif dengan beban server:

| Delay | Pengalaman Pengguna | Dampak Server |
|-------|------------------|---------------|
| **100ms** | Sangat responsif | 3x lebih banyak panggilan API daripada 300ms - beban tinggi |
| **200ms** | Responsif | 1.5x lebih banyak panggilan API daripada 300ms |
| **300ms** | Keseimbangan yang baik (direkomendasikan) | Baseline |
| **400ms** | Sedikit lambat | Lebih sedikit panggilan API - beban lebih rendah |
| **500ms** | Terasa tertunda | 50% lebih sedikit panggilan tetapi terasa lambat |

**Rekomendasi**: Pertahankan antara 250-350ms. Hanya tingkatkan di atas 350ms jika server Anda kesulitan dengan beban otomatisasi pencarian. Jangan pernah turunkan di bawah 200ms kecuali Anda memiliki server yang sangat cepat dan katalog kecil.

## Pengaturan Tampilan untuk Produk

Toggle ini mengontrol informasi apa yang muncul dalam hasil otomatisasi pencarian produk:

**Show Thumbnail** - Default: ON. Menampilkan gambar produk di sebelah hasil. **Dampak kinerja**: Menambahkan query gambar dan meningkatkan ukuran payload JSON. Nonaktifkan untuk otomatisasi pencarian yang lebih cepat pada koneksi lambat.

**Show Description** - Default: OFF. Menampilkan deskripsi pendek produk. **Dampak kinerja**: Menambahkan pemrosesan teks dan meningkatkan ukuran payload secara signifikan. Pertahankan nonaktif kecuali deskripsi sangat penting untuk pemilihan produk.

**Show Price** - Default: ON. Menampilkan harga produk. **Dampak kinerja**: Rendah - data harga sudah dimuat dengan produk. Aman untuk tetap diaktifkan.

**Show SKU** - Default: ON. Menampilkan SKU produk. **Dampak kinerja**: Rendah - SKU sudah diindeks. Penting untuk toko B2B.

**Show Stock Status** - Default: OFF. **⚠️ PERINGATAN KINERJA MAJOR**

Menampilkan badge 'In Stock', 'Low Stock', atau 'Out of Stock'. **JANGAN AKTIFKAN PADA KATALOG BESAR**.

Status stok memerlukan agregasi `with_stock_totals()` - menghitung jumlah on_hand di semua gudang untuk setiap produk dalam hasil otomatisasi pencarian. Ini menambahkan:
- Beban database yang signifikan (query agregasi)
- Latensi tambahan 200-500ms pada katalog >1.000 produk
- Potensi timeout pada katalog >10.000 produk

Hanya aktifkan jika sangat kritis dan Anda memiliki <500 produk.

## Pengaturan Tampilan untuk Posting Blog

**Show Featured Image** - Default: ON. Gambar utama posting blog dalam hasil otomatisasi pencarian.

**Show Excerpt** - Default: ON. Teks pratinjau singkat dari konten posting.

**Excerpt Length** - Default: 60 karakter. Berapa banyak teks pratinjau yang ditampilkan.

Pengaturan ini memiliki dampak kinerja minimal karena posting blog biasanya sedikit dibandingkan produk.

## Pengaturan Tampilan untuk Kategori dan Merek

**Show Thumbnail/Logo** - Default: ON. Gambar kategori atau merek dalam hasil.

**Show Product Count** - Default: OFF. **⚠️ PERINGATAN KINERJA**

Menampilkan jumlah produk dalam setiap kategori atau merek (misalnya, 'Electronics (234)').

**JANGAN AKTIFKAN PADA KATALOG BESAR**. Jumlah produk dihitung ulang pada setiap permintaan otomatisasi pencarian:
- Setiap jenis konten dengan counts aktif menambahkan 2 query tambahan
- Query termasuk join dan agregasi
- Latensi tambahan 100-300ms biasa
- Meningkat secara linear dengan jumlah kategori/merek

Hanya aktifkan jika Anda memiliki <50 kategori/merek DAN <1.000 produk total.

## Penyanggaan (Caching)

**Autocomplete Cache TTL** - Default: 60 detik (dihubungkan dengan tab Penyanggaan).

Hasil otomatisasi pencarian disimpan dalam cache untuk meningkatkan kinerja. TTL 60 detik berarti:
- Pelanggan pertama yang mencari 'laptop' memicu query database
- Selama 59 detik berikutnya, semua pencarian 'laptop' mengembalikan hasil yang disimpan dalam cache
- Setelah 60 detik, cache kedaluwarsa dan pencarian berikutnya memperbarui data

**Rekomendasi untuk TTL**:
- **45-60s**: Keseimbangan yang baik untuk sebagian besar toko (default)
- **90-120s**: Kinerja yang lebih baik jika inventaris produk jarang berubah
- **30s**: Hasil yang lebih baru jika Anda sering menambahkan produk

Meningkatkan TTL cache adalah cara termudah untuk meningkatkan kinerja otomatisasi pencarian.

## Otomatisasi Pencarian Multi-Bahasa

Jika Anda memiliki beberapa bahasa yang dikonfigurasi, otomatisasi pencarian secara otomatis mencari konten yang diterjemahkan yang disimpan dalam bidang JSONField terjemahan.

**Bagaimana cara kerjanya**:
- Pelanggan mencari dalam bahasa Spanyol: 'zapatos'
- Sistem mencari terjemahan nama produk dalam bahasa Spanyol
- Hasil menampilkan nama produk dalam bahasa Spanyol dari data JSONField
- Kembali ke bahasa dasar jika terjemahan Spanyol tidak tersedia

**Kinerja**: Overhead minimal untuk 1-3 bahasa. Dengan 5+ bahasa, sedikit peningkatan kompleksitas query.

## Menguji Otomatisasi Pencarian

Setelah mengonfigurasi pengaturan, uji pengalaman otomatisasi pencarian:

1. **Buka halaman utama toko Anda** dalam jendela incognito
2. **Klik kotak pencarian** untuk memfokuskan
3. **Ketik nama produk umum** secara perlahan (misalnya, 'laptop')
4. **Amati**:
   - Seberapa cepat hasil muncul setelah Anda berhenti mengetik (apakah debounce bekerja?)
   - Informasi apa yang ditampilkan (thumbnail, harga, SKU sesuai konfigurasi)
   - Apakah hasilnya relevan (periksa bobot relevansi jika tidak)
5. **Uji di perangkat mobile** - Pastikan dropdown mudah diakses dan terbaca

## Tips

- **Nonaktifkan deskripsi produk untuk kecepatan** - Deskripsi meningkatkan ukuran payload secara signifikan dengan nilai minimal dalam konteks otomatisasi pencarian
- **JANGAN AKTIFKAN STATUS STOK PADA KATALOG BESAR** - Agregasi stok menghancurkan kinerja otomatisasi pencarian
- **Uji di perangkat mobile dengan target sentuh** - Hasil otomatisasi pencarian harus mudah diklik di ponsel
- **Pantau waktu respons mingguan** - Targetkan <200ms untuk permintaan otomatisasi pencarian
- **Tingkatkan TTL cache jika lambat** - Optimasi kinerja termudah
- **Jumlah produk mahal - nonaktifkan kecuali kritis** - Setiap jumlah kategori/merek menambahkan 2 query ke setiap permintaan otomatisasi pencarian