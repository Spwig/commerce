---
title: POS Store Groups
---

Grup toko mengorganisir beberapa lokasi ritel dengan konfigurasi yang berbagi. Sebaliknya dari mengonfigurasi setiap terminal secara individual, kelompokkan terminal berdasarkan wilayah, franchise, atau jenis lokasi dan terapkan pengaturan pada tingkat kelompok. Grup mendukung pewarisan pengaturan—mata uang, bahasa, zona waktu, template struk, dan konten promosi berjatuhan dari kelompok ke toko individu. Ini menyederhanakan manajemen untuk pedagang multi-lokasi sambil mempertahankan fleksibilitas untuk penimbalan khusus toko ketika diperlukan.

Gunakan grup toko ketika Anda mengoperasikan beberapa lokasi ritel, franchise, atau pasar regional dengan persyaratan operasional yang berbeda.

![Daftar Grup Toko](/static/core/admin/img/help/pos-store-groups/storegroup-list.webp)

## Apa Itu Grup Toko?

Grup toko adalah wadah organisasi untuk gudang dan terminal yang berbagi karakteristik umum:

**Strategi Pengelompokan Umum**:
- **Geografis**: Wilayah Utara, Wilayah Selatan, Pantai Barat, Pantai Timur
- **Franchise**: Toko Franchisee A, Toko Franchisee B, Toko Perusahaan
- **Format**: Lokasi Mal, Toko Mandiri, Toko Pop-Up
- **Pasar**: Toko Domestik, Toko Eropa, Toko Asia Pasifik

Grup tidak mengubah operasi fisik terminal—mereka menyediakan lapisan konfigurasi yang menyederhanakan manajemen pada skala.

## Kapan Menggunakan Grup Toko

**Satu Lokasi** - Tidak perlu grup. Konfigurasikan terminal secara langsung.

**2-3 Lokasi dengan Pengaturan Identik** - Grup opsional. Mungkin lebih mudah untuk mengonfigurasikan terminal secara langsung.

**4+ Lokasi** - Grup sangat disarankan. Konfigurasi terpusat menghemat waktu.

**Operasi Multi-Negara** - Grup esensial. Mata uang, bahasa, dan zona waktu yang berbeda memerlukan penimbalan pada tingkat grup.

**Operasi Franchise** - Grup kritis. Setiap franchisee membutuhkan pengaturan independen sambil mempertahankan konsistensi merek.

## Hierarki Pewarisan Pengaturan

Spwig POS menggunakan cascading pengaturan 4 tingkat (prioritas tertinggi ke terendah):

| Tingkat | Prioritas | Contoh | Kasus Penggunaan |
|---------|-----------|-------|------------------|
| **Terminal** | 1 (Tertinggi) | Terminal 5 menimpa lebar kertas menjadi 58mm | Satu terminal memiliki perangkat printer unik |
| **Toko** | 2 | Toko 2 menimpa mata uang menjadi GBP | Lokasi Inggris di antara toko-toko AS yang mayoritas |
| **Grup** | 3 | Grup Eropa mengatur zona waktu menjadi CET | Konsistensi regional di beberapa toko |
| **Situs** | 4 (Terendah) | Default global: USD, Inggris, UTC | Pengganti untuk semua pengaturan yang belum dikonfigurasikan |

**Bagaimana Cara Kerjanya**:
- Sistem memeriksa pengaturan Terminal terlebih dahulu
- Jika tidak diatur, memeriksa pengaturan Toko
- Jika tidak diatur, memeriksa pengaturan Grup
- Jika tidak diatur, menggunakan default Situs

**Contoh**:
- Default Situs: Mata Uang = USD, Bahasa = Inggris
- Grup "Toko Eropa": Mata Uang = EUR, Bahasa = tidak diatur
- Toko "Paris Flagship": Mata Uang = tidak diatur, Bahasa = Prancis
- Terminal "Paris Register 1": Mata Uang = tidak diatur, Bahasa = tidak diatur

**Hasil untuk Paris Register 1**:
- Mata Uang: EUR (diturunkan dari Grup)
- Bahasa: Prancis (diturunkan dari Toko)

Cascading ini memungkinkan default luas dengan penimbalan yang tepat di tempat yang diperlukan.

## Membuat Grup Toko

Navigasi ke **POS > Grup Toko** dan klik **+ Tambahkan Grup Toko**:

![Form Tambah Grup Toko](/static/core/admin/img/help/pos-store-groups/storegroup-add-form.webp)

### Konfigurasi Dasar

**Nama Grup** - Label deskriptif (contoh: "West Coast Stores", "European Franchises", "Mall Locations")

**Kode** - Identifikasi unik pendek (contoh: "WEST", "EUR", "MALL"):
- Digunakan secara internal untuk referensi
- Harus unik di seluruh grup
- 2-10 karakter, alphanumeric
- Disarankan menggunakan huruf besar untuk konsistensi

**Urutan Pengurutan** - Mengontrol urutan tampilan dalam daftar admin (angka lebih rendah muncul lebih dulu):
- Gunakan kelipatan 10: 10, 20, 30 (memungkinkan menyisipkan grup baru antara yang sudah ada)
- Membantu mengorganisasi grup secara logis (urutan geografis, urutan ukuran, dll.)

### Penimbalan Regional

**Penimbalan Mata Uang** - Atur mata uang tingkat grup berbeda dari default situs:
- Contoh: Grup Eropa menggunakan EUR, grup Asia Pasifik menggunakan JPY
- Semua terminal dalam grup ini secara default menggunakan mata uang ini
- Mempengaruhi tampilan harga, rekonsiliasi uang tunai, laporan

**Penimbalan Bahasa** - Atur bahasa tingkat grup berbeda dari default situs:
- Contoh: Toko Prancis menggunakan Prancis, toko Jerman menggunakan Jerman
- Mempengaruhi bahasa antarmuka POS, bahasa struk (jika template mendukung)
- Staf melihat antarmuka POS dalam bahasa ini saat masuk ke terminal grup

**Penimbalan Zona Waktu** - Atur zona waktu tingkat grup berbeda dari default situs:
- Contoh: Toko Pantai Barat menggunakan America/Los_Angeles, toko Eropa menggunakan Europe/Paris
- Mempengaruhi timestamp shift, penjadwalan laporan, penjadwalan slide promosi
- Memastikan laporan shift selaras dengan jam operasional lokal

**Kapan Menimbal**:
- **Mata Uang**: Selalu timbal untuk lokasi internasional (mata uang pembayaran berbeda)
- **Bahasa**: Timbal untuk pasar non-Inggris (konten menghadap ke pelanggan)
- **Zona Waktu**: Timbal untuk lokasi >2 jam dari default situs (timestamp lokal akurat)

## Menghubungkan Gudang dengan Grup

Setelah membuat grup, tetapkan gudang ke dalamnya:

1. Navigasi ke **Katalog > Gudang**
2. Edit gudang yang mewakili lokasi toko
3. Atur bidang **Grup Toko** ke grup yang telah dibuat
4. Simpan

Semua terminal yang ditetapkan ke gudang ini sekarang mewarisi pengaturan grup.

**Contoh Pengaturan**:
- Buat grup: "Toko Eropa" (Mata Uang: EUR, Bahasa: tidak diatur, Zona Waktu: CET)
- Buat gudang: "Toko Paris", "Toko Berlin", "Toko Roma"
- Tetapkan semua 3 gudang ke grup "Toko Eropa"
- Buat terminal: "Paris Register 1", "Berlin Register 1", "Roma Register 1"
- Setiap terminal mewarisi mata uang EUR dan zona waktu CET dari grup
- Timbal bahasa pada tingkat toko: Paris=Prancis, Berlin=Jerman, Roma=Italia

## Pengaturan yang dikontrol oleh Grup

Grup dapat menimbal pengaturan berikut:

**Pengaturan Operasional**:
- Mata Uang (mempengaruhi tampilan harga dan rekonsiliasi uang tunai)
- Bahasa (mempengaruhi bahasa antarmuka POS)
- Zona Waktu (mempengaruhi timestamp dan penjadwalan)

**Pengaturan Konten** (melalui model yang dibatasi):
- Template struk (membuat desain struk khusus grup)
- Slide promosi (menargetkan promosi ke grup tertentu)

**Tidak dikontrol oleh Grup**:
- Konfigurasi perangkat terminal (dikonfigurasikan per-terminal)
- Penugasan staf (dikonfigurasikan per-terminal)
- Tingkat stok gudang (dikonfigurasikan per-gudang)
- Akun penyedia pembayaran (dikonfigurasikan secara situs-wide atau per-penyedia)

## Contoh Dunia Nyata

### Contoh 1: Penyedia Pakaian Mode Internasional

**Pengaturan**:
- 50 toko di 5 negara
- Setiap negara memiliki mata uang, bahasa, dan persyaratan pajak yang berbeda

**Struktur Grup**:
- Grup: "Toko AS" (USD, Inggris, America/New_York)
  - 20 gudang (NY, LA, Chicago, dll.)
  - 60 terminal
- Grup: "Toko UK" (GBP, Inggris, Europe/London)
  - 10 gudang (London, Manchester, dll.)
  - 30 terminal
- Grup: "Toko Eropa" (EUR, tidak diatur, Europe/Paris)
  - 15 gudang (Paris, Berlin, Roma, dll.)
  - 45 terminal
  - Bahasa ditimbal pada tingkat toko (Paris=Prancis, Berlin=Jerman, Roma=Italia)
- Grup: "Toko Jepang" (JPY, Jepang, Asia/Tokyo)
  - 5 gudang (Tokyo, Osaka, dll.)
  - 15 terminal

**Manfaat**:
- Satu konfigurasi grup berlaku untuk semua toko di setiap pasar
- Template struk yang dibatasi ke grup (format pajak untuk Eropa, pajak penjualan untuk AS)
- Slide promosi yang ditargetkan berdasarkan wilayah (AS: Penjualan Hari Memorial, Eropa: Penjualan Liburan Musim Panas)

### Contoh 2: Rantai Kafe

**Pengaturan**:
- 30 lokasi, semua di negara yang sama, tetapi berbeda format

**Struktur Grup**:
- Grup: "Lokasi Mal" (tidak diatur, tidak diatur, tidak diatur)
  - 10 toko berbasis mal
  - Slide promosi jam operasional diperpanjang (buka hingga pukul 9 malam)
  - Template struk dengan kode QR validasi parkir mal
- Grup: "Toko Mandiri" (tidak diatur, tidak diatur, tidak diatur)
  - 15 toko depan jalan
  - Slide promosi jam operasional standar
  - Template struk standar
- Grup: "Lokasi Bandara" (tidak diatur, tidak diatur, tidak diatur)
  - 5 toko bandara
  - Slide promosi 24 jam
  - Template struk dengan integrasi kode QR informasi penerbangan

**Manfaat**:
- Konten promosi berbeda untuk format berbeda
- Kustomisasi struk berdasarkan lokasi
- Manajemen disederhanakan (perbarui satu grup daripada memperbarui 10 toko individu)

### Contoh 3: Operasi Franchise

**Pengaturan**:
- 100 toko, 20 franchisee berbeda

**Struktur Grup**:
- Grup: "Franchisee A" (tidak diatur, tidak diatur, tidak diatur)
  - 10 toko yang dioperasikan oleh Franchisee A
  - Informasi kontak Franchisee A pada struk (melalui template struk grup)
  - Konten promosi Franchisee A (acara lokal, khusus)
- Grup: "Franchisee B" (tidak diatur, tidak diatur, tidak diatur)
  - 8 toko yang dioperasikan oleh Franchisee B
  - Informasi kontak Franchisee B pada struk
  - Konten promosi Franchisee B
- (Ulangi untuk semua franchisee)
- Grup: "Toko Perusahaan" (tidak diatur, tidak diatur, tidak diatur)
  - 5 toko milik perusahaan
  - Branding perusahaan dan promosi

**Manfaat**:
- Setiap franchisee mengelola pengaturan grup mereka sendiri
- Konsistensi merek dipertahankan melalui default situs
- Kemandirian franchisee melalui penimbalan grup

## Mengelola Pengaturan Grup

**Mengubah Pengaturan Grup** memengaruhi semua terminal dalam grup tersebut:
- Perubahan mata uang: Semua terminal grup beralih ke mata uang baru pada sinkronisasi berikutnya
- Perubahan bahasa: Semua terminal grup beralih ke bahasa baru pada sinkronisasi berikutnya
- Perubahan zona waktu: Semua terminal grup menghitung ulang timestamp pada sinkronisasi berikutnya

**Pertimbangan Dampak**:
- Uji perubahan pada satu terminal sebelum menerapkannya ke seluruh grup
- Beri tahu staf tentang perubahan yang akan datang (misalnya, perubahan bahasa)
- Jadwalkan perubahan selama jam non-puncak untuk meminimalkan gangguan

**Menghapus Grup**:
- Tetapkan ulang semua gudang ke grup lain atau hapus penugasan grup
- Terminal kehilangan pengaturan tingkat grup dan kembali ke default situs
- Tidak dapat menghapus grup saat gudang masih ditugaskan

## Tips

- **Gunakan kode yang bermakna** - "WEST" lebih jelas daripada "GRP1" saat meninjau konfigurasi
- **Rencanakan hierarki sebelum membuat grup** - Pikirkan struktur organisasi Anda terlebih dahulu; restrukturisasi nanti adalah tugas yang melelahkan
- **Uji pengaturan grup dengan satu terminal** - Sebelum menetapkan 50 gudang ke grup, uji pengaturan grup dengan satu terminal
- **Timbal secara jarang pada tingkat toko** - Terlalu banyak penimbalan tingkat toko mengalahkan tujuan grup
- **Dokumentasikan tujuan grup** - Catat dalam nama grup apa yang membuat grup ini berbeda (geografi, format, franchisee)
- **Gunakan urutan pengurutan secara strategis** - Urutkan grup berdasarkan pentingnya (Toko Perusahaan terlebih dahulu) atau geografi (Barat ke Timur) untuk navigasi yang lebih mudah
- **Jaga jumlah grup tetap wajar** - 20+ grup menunjukkan segmentasi berlebihan; pertimbangkan konsolidasi
- **Penimbalan mata uang adalah permanen** - Beralih mata uang grup di tengah operasi mempersulit akuntansi; rencanakan dengan hati-hati

Ingat: Pertahankan semua format markdown, jalur gambar, blok kode, dan istilah teknis secara tepat seperti yang ditunjukkan dalam aturan pelestarian.