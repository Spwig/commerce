---
title: Pengaturan Template Struk
---

Template struk mengontrol penampilan dan konten struk termal yang dicetak di terminal POS Anda. Kustomisasi teks header dan footer, tambahkan logo Anda, konfigurasikan bidang kepatuhan (nomor ID pajak, nomor pendaftaran bisnis), dan sertakan kode QR promosi. Template mendukung penargetan cakupan—buat template default untuk semua toko, template khusus grup untuk wilayah, atau template khusus toko untuk lokasi individu. Sistem menggunakan aturan prioritas cakupan untuk menentukan template mana yang berlaku saat mencetak struk.

Gunakan template struk untuk menjaga konsistensi merek, memenuhi persyaratan kepatuhan regional, dan meningkatkan keterlibatan pelanggan melalui elemen promosi.

![Daftar Template Struk](/static/core/admin/img/help/receipt-template-customization/receipt-list.webp)

## Dasar-Dasar Template Struk

Template struk mendefinisikan struktur dan konten struk yang dicetak dari printer termal ESC/POS. Setiap template menentukan:

**Konfigurasi Fisik**:
- Lebar kertas (58mm atau 80mm)
- Gambar logo (monochrome untuk pencetakan termal)
- Ukuran font dan jarak

**Bagian Konten**:
- Teks header (nama toko, alamat, informasi kontak)
- Data transaksi dinamis (item, harga, total, metode pembayaran)
- Teks footer (kebijakan pengembalian, pesan terima kasih, media sosial)
- Bidang kepatuhan (nomor ID pajak, nomor pendaftaran bisnis)
- Kode QR promosi dengan label

**Penargetan Cakupan**:
- Template default (berlaku untuk semua toko kecuali ditimpa)
- Template grup (berlaku untuk semua toko dalam grup)
- Template toko (berlaku untuk toko tertentu/gudang)

## Aturan Prioritas Cakupan

Ketika terminal mencetak struk, sistem memilih template menggunakan hierarki ini (prioritas tertinggi ke terendah):

| Prioritas | Cakupan | Contoh | Kasus Penggunaan |
|-----------|--------|-------|------------------|
| **1** | Khusus toko | Template Toko Paris | Persyaratan kepatuhan pajak unik Prancis |
| **2** | Khusus grup | Template Toko Eropa | Tampilan PPN untuk semua lokasi Eropa |
| **3** | Default | Template Global | Fallback untuk semua toko yang belum dikonfigurasi |

**Bagaimana Cara Kerjanya**:
1. Periksa apakah toko memiliki template khusus (gudang spesifik)
2. Jika tidak, periksa apakah grup toko memiliki template grup
3. Jika tidak, gunakan template default

**Contoh**:
- Template default: "Standard Receipt" (tidak ada penugasan cakupan)
- Template grup: "EU Receipt" (ditugaskan ke grup Toko Eropa) - termasuk pendaftaran PPN
- Template toko: "Paris Receipt" (ditugaskan ke gudang Paris) - termasuk nomor SIRET Prancis

**Hasil**:
- Terminal Toko Paris: Menggunakan "Paris Receipt" (paling spesifik)
- Terminal Toko Berlin (dalam grup Toko Eropa, tanpa template toko): Menggunakan "EU Receipt" (tingkat grup)
- Terminal Toko New York (tanpa grup, tanpa template toko): Menggunakan "Standard Receipt" (fallback default)

## Konfigurasi Lebar Kertas

Printer termal struk menggunakan kertas berlebar 58mm atau 80mm. Pilih berdasarkan perangkat printer Anda:

| Lebar Kertas | Karakter Per Baris | Terbaik Untuk | Penggunaan Umum |
|--------------|-------------------|--------------|------------------|
| **58mm** | ~32 karakter | Ruang kecil, portabel | Truk makanan, POS mobile, kios |
| **80mm** | ~48 karakter | Penjualan ritel standar | Kebanyakan toko ritel, restoran |

**Tidak bisa mencampur lebar kertas**: Semua terminal yang menggunakan template yang sama harus memiliki printer dengan lebar kertas yang sama. Jika Anda memiliki jenis printer yang berbeda, buat template terpisah untuk setiap lebar kertas.

**Batas Ukuran Logo**:
- **58mm**: Lebar maksimal 384 piksel (direkomendasikan: 350px)
- **80mm**: Lebar maksimal 576 piksel (direkomendasikan: 550px)

Logo yang melebihi lebar maksimal akan secara otomatis diukur kecil, yang dapat mengurangi kualitas.

## Konfigurasi Logo

Logo struk harus **monochrome** (hanya hitam dan putih) untuk kompatibilitas dengan printer termal:

**Persyaratan Logo**:
- Format file: PNG, JPG, atau WebP
- Mode warna: Monochrome (piksel hitam di latar belakang putih)
- Dimensi direkomendasikan:
  - Kertas 58mm: 350px lebar × 100-150px tinggi
  - Kertas 80mm: 550px lebar × 150-200px tinggi
- Ukuran file: <100KB (printer termal memiliki memori terbatas)

**Membuat Logo Monochrome**:
1. Mulai dengan logo biasa Anda (warna atau abu-abu)
2. Gunakan editor gambar untuk mengubah menjadi hitam dan putih murni (tanpa abu-abu)
3. Tingkatkan kontras untuk memastikan elemen hitam padat
4. Ekspor sebagai PNG dengan latar belakang transparan atau putih

**Posisi Logo**:
- Selalu di tengah secara horizontal
- Cetak di bagian atas struk (di atas teks header)
- Diikuti oleh ruang kosong otomatis (mencegah kepadatan dengan konten)

**Memilih Logo**:
- Klik **Browse Media Library** di formulir template
- Pilih aset logo monochrome
- Tampilan pratinjau menunjukkan bagaimana logo akan muncul di struk

**Tidak Ada Logo**: Biarkan bidang logo kosong jika Anda lebih suka branding hanya teks (teks header dapat mencakup nama toko).

## Teks Header

Teks header muncul segera setelah logo (atau di bagian atas jika tidak ada logo). Konten umum:

**Nama Toko dan Alamat**:
```
Your Store Name
123 Main Street
City, State 12345
Phone: (555) 123-4567
```

**Jam Operasional**:
```
Senin-Jumat: 9 pagi-9 malam
Sabtu-Minggu: 10 pagi-6 malam
```

**Tagline atau Slogan**:
```
Produk Berkualitas, Layanan Luar Biasa
```

**Format**:
- Gunakan pemisah baris untuk memisahkan informasi
- Otomatis rata tengah
- Pertahankan baris di bawah batas karakter untuk lebar kertas (32 karakter untuk 58mm, 48 untuk 80mm)

**Variabel yang Tersedia** (opsional):
- `{store_name}` - Diganti dengan nama gudang
- `{order_date}` - Diganti dengan tanggal transaksi
- `{order_number}` - Diganti dengan ID pesanan

Sebagian besar pedagang menggunakan teks statis alih-alih variabel untuk konsistensi header.

## Teks Footer

Teks footer muncul setelah detail transaksi (item, total, pembayaran). Konten umum:

**Kebijakan Pengembalian**:
```
Kembalikan dalam 30 hari dengan struk
Hanya kredit toko atau pertukaran
```

**Pesan Terima Kasih**:
```
Terima kasih telah berbelanja dengan kami!
Ikuti kami @yourstore
```

**Layanan Pelanggan**:
```
Pertanyaan? Hubungi (555) 123-4567
atau email support@yourstore.com
```

**Tips Format**:
- Pertahankan informasi terpenting di bagian depan (kebijakan pengembalian, kontak)
- Gunakan pemisah baris untuk keterbacaan
- Pertimbangkan menambahkan garis pemisah (`---`) antar bagian

## Bidang Kepatuhan

Banyak yurisdiksi memerlukan informasi tertentu di struk:

**Label ID Pajak** - Label kustom untuk nomor identifikasi pajak:
- AS: "Tax ID" atau "EIN"
- EU: "VAT Number" atau "VAT Reg No"
- Kanada: "GST/HST Number"
- Australia: "ABN"

**Nilai ID Pajak** - Nomor identifikasi yang sebenarnya:
- Diisi sekali di template, muncul di semua struk
- Contoh: "VAT Number: GB123456789"

**Label Pendaftaran Bisnis** - Label kustom untuk pendaftaran bisnis:
- Prancis: "SIRET"
- Jerman: "Handelsregister"
- UK: "Company Registration Number"

**Nilai Pendaftaran Bisnis** - Nomor pendaftaran yang sebenarnya:
- Contoh: "SIRET: 123 456 789 00010"

**Tampilkan Powered By Spwig** - Toggle untuk menampilkan atau menyembunyikan branding "Powered by Spwig";
- Secara default diaktifkan (mendukung pengembangan platform)
- Nonaktifkan untuk operasi white-label

**Contoh Kepatuhan Berdasarkan Wilayah**:

**Uni Eropa**:
- Label ID Pajak: "VAT Number"
- Nilai ID Pajak: "GB123456789"
- Tampilkan nomor pendaftaran perusahaan jika diperlukan oleh negara

**Amerika Serikat**:
- Secara umum tidak ada persyaratan ID pajak di struk (berbeda-beda berdasarkan negara bagian)
- Mungkin termasuk EIN untuk transaksi B2B

**Prancis (Spesifik)**:
- SIRET wajib di semua struk
- Label Pendaftaran Bisnis: "SIRET"
- Nilai Pendaftaran Bisnis: "123 456 789 00010"

**Australia**:
- ABN (Australian Business Number) disarankan untuk bisnis yang terdaftar GST
- Label ID Pajak: "ABN"

Periksa persyaratan struk yurisdiksi lokal Anda sebelum diluncurkan.

## Promosi Kode QR

Sertakan kode QR di bagian bawah struk untuk meningkatkan keterlibatan pelanggan:

**URL Kode QR** - Tujuan saat di-scan:
- Ulasan: `https://yourstore.com/reviews/leave-review`
- Program loyalitas: `https://yourstore.com/loyalty/join`
- Diskon pembelian berikutnya: `https://yourstore.com/discount/THANKYOU`
- Media sosial: `https://instagram.com/yourstore`
- Halaman utama situs: `https://yourstore.com`

**Label Kode QR** - Teks yang ditampilkan di atas kode QR:
- "Scan untuk meninggalkan ulasan dan mendapatkan diskon 10% untuk pembelian berikutnya"
- "Bergabung dengan program loyalitas kami - Scan di sini"
- "Ikuti kami di Instagram - Scan untuk terhubung"
- "Nilai pengalaman Anda"

**Praktik Terbaik Kode QR**:
- Gunakan URL pendek (URL panjang menciptakan kode yang padat, sulit untuk di-scan)
- Uji kode QR dengan berbagai kamera ponsel sebelum diterapkan
- Sertakan penawaran nilai jelas dalam label (apa yang pelanggan dapatkan dengan memindainya)
- Lacak pemindaian kode QR untuk mengukur efektivitasnya (gunakan URL dengan parameter pelacakan)

**Kode QR Dinamis** (Lanjutan):
- Gunakan layanan redirect QR (bit.ly, tinyurl) untuk membuat URL pendek
- Arahkan redirect ke tujuan berbeda secara musiman tanpa mencetak ulang struk
- Contoh: `https://bit.ly/yourstoreqr` → mengarahkan ke promosi saat ini

## Membuat Template untuk Cakupan Berbeda

**Template Default** (rekomendasi titik awal):
1. Navigasi ke **POS > Receipt Templates**
2. Klik **+ Tambah Template Struk**
3. Biarkan bidang **Warehouse** dan **Store Group** kosong (ini membuatnya menjadi default)
4. Konfigurasikan lebar kertas sesuai dengan jenis printer yang paling umum
5. Tambahkan logo, header, footer
6. Konfigurasikan bidang kepatuhan untuk pasar utama Anda
7. Simpan

Template ini berlaku untuk semua toko kecuali ditimpa.

**Template Grup** (untuk variasi regional):
1. Buat template baru
2. Pilih **Store Group** (misalnya, "European Stores")
3. Biarkan **Warehouse** kosong
4. Sesuaikan bidang kepatuhan untuk wilayah (misalnya, format PPN)
5. Sesuaikan teks header (misalnya, alamat regional)
6. Simpan

Template ini berlaku untuk semua toko dalam grup.

**Template Toko** (untuk kebutuhan lokasi spesifik):
1. Buat template baru
2. Pilih **Warehouse** (misalnya, "Paris Store")
3. Sesuaikan semua bidang untuk lokasi ini
4. Simpan

Template ini hanya berlaku untuk satu toko ini.

**Menguji Template**:
- Proses transaksi uji di terminal
- Cetak struk
- Verifikasi kejelasan logo, penjajaran teks, bidang kepatuhan, dan kemampuan pemindaian kode QR
- Sesuaikan template dan uji ulang jika diperlukan

## Tata Letak Struk Umum

**Struk Minimal** (truk makanan, pop-up):
- Tidak ada logo (penghematan ruang)
- Header: Nama toko dan nomor telepon saja
- Footer: Pesan terima kasih
- Tidak ada kode QR

**Struk Penjualan Ritel Standar**:
- Logo (logo merek monochrome)
- Header: Nama toko lengkap, alamat, jam operasional
- Kepatuhan: ID pajak
- Footer: Kebijakan pengembalian, pesan terima kasih
- Kode QR: Permintaan ulasan

**Struk Penjualan Ritel Premium**:
- Logo (logo kata merek lengkap)
- Header: Tagline, alamat, kontak
- Kepatuhan: ID pajak, pendaftaran bisnis
- Footer: Kebijakan pengembalian, layanan pelanggan, media sosial
- Kode QR: Pendaftaran program loyalitas

**Rantai Multi-Lokasi**:
- Template default: Branding perusahaan, kebijakan standar
- Template grup: Kepatuhan regional (PPN untuk Eropa, GST untuk Kanada)
- Template toko: Alamat dan telepon spesifik lokasi

## Mengelola Banyak Template

**Konvensi Penamaan Template**:
- Gunakan cakupan dalam nama: "Default Receipt", "EU Group Receipt", "Paris Store Receipt"
- Membantu mengidentifikasi template mana yang berlaku di mana saat meninjau daftar

**Perubahan Template**:
- Perubahan berlaku langsung untuk struk masa depan
- Struk masa lalu (yang sudah dicetak) tidak terpengaruh
- Uji perubahan di terminal dengan lalu lintas rendah sebelum diterapkan ke semua toko

**Duplikasi Template**:
- Saat membuat template baru yang mirip dengan yang ada, duplikasikan template yang ada dan ubah
- Mencegah mulai dari awal

**Menghapus Template**:
- Tidak bisa menghapus template default saat terminal ada (harus memiliki satu fallback)
- Bisa menghapus template grup/toko (terminal kembali ke tingkat berikutnya dalam hierarki)
- Konfirmasi bahwa tidak ada terminal yang secara aktif menggunakan template sebelum menghapus

## Tips

- **Mulai dengan 80mm jika ragu** - Lebar kertas standar cocok untuk kebanyakan ritel; 58mm adalah spesialisasi
- **Uji logo di printer sebenarnya** - Yang terlihat bagus di layar mungkin mencetak buruk; uji sejak awal
- **Perbarui bidang kepatuhan secara teratur** - Pendaftaran pajak yang kedaluwarsa di struk menciptakan masalah hukum
- **Kode QR dengan nilai properti scan lebih baik** - "Scan untuk 10% diskon" mengungguli "Scan di sini" sebanyak 10x
- **Periksa batas karakter** - Penyelarasan teks merusak format; hitung karakter per baris sebelum diterapkan
- **Satu template per lebar kertas** - Jangan tugaskan template 80mm ke terminal dengan printer 58mm (logo tidak akan muat)
- **Cetak struk uji bulanan** - Printer menurun seiring waktu; verifikasi kualitas tetap dapat diterima
- **Gunakan variabel secara terbatas** - Teks statis lebih andal daripada variabel dinamis (lebih sedikit titik kegagalan)
- **Cadangkan konfigurasi template** - Ambil screenshot atau ekspor pengaturan template sebelum perubahan besar (mudah rollback)
- **Kepatuhan regional bervariasi** - Riset persyaratan struk lokal sebelum diterapkan; denda untuk ketidakpatuhan bisa parah

Ingat: Pertahankan semua format markdown, jalur gambar, blok kode, dan istilah teknis secara tepat seperti yang ditunjukkan dalam aturan pelestarian.