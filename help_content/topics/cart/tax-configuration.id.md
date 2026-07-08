---
title: Konfigurasi Pajak
---

Konfigurasikan aturan pajak untuk toko Anda sehingga pajak yang benar diterapkan secara otomatis pada pesanan berdasarkan lokasi pelanggan. Anda dapat memuat preset regional dengan satu klik atau membuat aturan khusus untuk negara, provinsi, kota, atau kode pos mana pun.

![Dasbor Pajak](/static/core/admin/img/help/tax-configuration/tax-dashboard.webp)

## Dasbor Pajak

Navigasikan ke **Pesanan > Pengiriman > Tingkat Pajak** untuk membuka dasbor pajak. Halaman menampilkan:

- **Panel Statistik** — empat kartu yang menampilkan Total Aturan, Aturan Aktif, Negara yang Dicakup, dan Jenis Pajak yang Digunakan
- **Filter** — cari berdasarkan nama, negara, atau provinsi, dan saring berdasarkan negara, jenis pajak (Pajak Penjualan, PPN, PPN, Pajak Khusus), atau status (Aktif/Tidak Aktif)
- **Kartu Aturan Pajak** — setiap kartu menampilkan bendera negara, nama aturan, lokasi, persentase tingkat, badge jenis pajak, badge status, prioritas, dan jumlah pengecualian

## Memuat Preset Pajak

Klik **Muat Preset** untuk membuka modal preset. Preset adalah kumpulan tingkat pajak standar untuk suatu wilayah, siap dimuat ke toko Anda dengan satu klik.

![Muat Preset](/static/core/admin/img/help/tax-configuration/tax-presets-modal.webp)

Preset diorganisir berdasarkan wilayah dunia:

| Wilayah | Kelompok Preset |
|--------|--------------|
| **Afrika** | PPN Afrika (25 tingkat) |
| **Asia Pasifik** | PPN/PPN Asia-Pasifik (24 tingkat), PPN Asia Tengah (6 tingkat) |
| **Eropa** | Tingkat PPN UE, PPN Inggris, PPN Eropa Lainnya |
| **Amerika Latin** | PPN Amerika Latin |
| **Timur Tengah** | PPN Timur Tengah |
| **Amerika Utara** | Pajak Penjualan Negara Bagian AS, PPN/HST Kanada |
| **Oceania** | PPN/PPN Oceania |

### Cara Kerja Preset

1. Klik **Muat** pada kelompok preset yang ingin Anda pilih
2. Sistem membuat aturan pajak untuk setiap negara atau provinsi dalam kelompok tersebut
3. Aturan yang sudah ada dengan negara, provinsi, dan jenis pajak yang sama secara otomatis diabaikan untuk mencegah duplikasi
4. Setelah dimuat, setiap aturan dapat diedit sepenuhnya — sesuaikan tingkat, tambahkan pengecualian, atau nonaktifkan aturan yang tidak Anda butuhkan

Anda dapat memuat beberapa kelompok preset. Misalnya, muat baik Tingkat PPN UE dan PPN Inggris jika Anda menjual kepada pelanggan di seluruh Eropa.

## Membuat Aturan Pajak Secara Manual

Klik **Tambahkan Tingkat Pajak** untuk membuat aturan khusus. Formulir memiliki empat bagian:

![Formulir Tingkat Pajak](/static/core/admin/img/help/tax-configuration/tax-rate-form.webp)

### Informasi Dasar

| Bidang | Deskripsi |
|-------|-------------|
| **Nama** | Nama tampilan untuk aturan (misalnya, "Pajak Penjualan California") |
| **Aktif** | Toggle untuk mengaktifkan atau menonaktifkan aturan |
| **Jenis Pajak** | Pajak Penjualan, PPN, PPN, atau Pajak Khusus |
| **Tingkat (%)** | Tingkat pajak sebagai persentase (misalnya, masukkan 8,25 untuk 8,25%) |
| **Prioritas** | Angka yang lebih tinggi mengambil alih ketika beberapa aturan cocok dengan lokasi yang sama |

### Cakupan Geografis

| Bidang | Deskripsi |
|-------|-------------|
| **Negara** | Kode ISO 3166-1 alpha-2 (misalnya, US, GB, DE) |
| **Provinsi** | Provinsi atau wilayah (biarkan kosong untuk menerapkan ke seluruh negara) |
| **Kota** | Nama kota (opsional, untuk aturan pajak tingkat kota) |
| **Kode Pos** | Daftar kode pos spesifik (opsional, untuk aturan pajak tingkat kode pos) |

Aturan cocok dari yang paling spesifik ke yang paling umum. Aturan untuk kode pos spesifik mengambil alih aturan untuk provinsi yang sama, yang mengambil alih aturan untuk seluruh negara.

### Aturan Penerapan

| Bidang | Deskripsi |
|-------|-------------|
| **Berlaku untuk Pengiriman** | Ketika dicentang, pajak ini juga berlaku untuk biaya pengiriman |
| **Pajak Gabungan** | Ketika dicentang, pajak ini dihitung di atas pajak lainnya (jumlah dasar ditambah pajak yang sudah diterapkan sebelumnya) |

### Pengecualian Produk

| Bidang | Deskripsi |
|-------|-------------|
| **Jenis Produk yang Dikecualikan** | Jenis produk yang dikecualikan dari pajak ini (misalnya, digital, layanan) |
| **Kategori yang Dikecualikan** | Kategori produk spesifik yang dikecualikan dari pajak ini |

## Jenis Pajak

| Jenis | Digunakan Untuk | Contoh |
|------|----------|---------|
| **Pajak Penjualan** | AS, Kanada | Pajak penjualan tingkat provinsi dan negara bagian |
| **PPN** | Eropa, Inggris, sebagian besar Asia dan Afrika | Pajak Nilai Tambah |
| **PPN** | Australia, Selandia Baru, India, Singapura | Pajak Barang dan Jasa |
| **Pajak Khusus** | Kasus khusus | Pajak tambahan lokal, pajak lingkungan, pajak mewah |

## Cara Kerja Perhitungan Pajak

Ketika pelanggan mencapai checkout, sistem secara otomatis menghitung pajak berdasarkan alamat pengiriman mereka:

1. **Pencocokan Geografis** — menemukan semua aturan aktif yang cocok dengan negara pelanggan, kemudian menyempitkan berdasarkan provinsi, kota, dan kode pos
2. **Penilaian Spesifik** — aturan yang lebih spesifik (kode pos > kota > provinsi > negara) memiliki peringkat yang lebih tinggi
3. **Urutan Prioritas** — dalam tingkat spesifikasi yang sama, aturan dengan prioritas yang lebih tinggi mengambil alih
4. **Pengecualian Produk** — produk yang dikecualikan dikecualikan dari setiap aturan yang berlaku
5. **Pajak Non-Gabungan** — dihitung terlebih dahulu pada harga dasar setiap item
6. **Pajak Gabungan** — dihitung pada harga dasar ditambah semua pajak non-gabungan yang sudah diterapkan
7. **Pajak Pengiriman** — jika aturan memiliki "Berlaku untuk Pengiriman" dicentang, biaya pengiriman dimasukkan ke dalam jumlah yang dikenai pajak

Pembreakdownan pajak disimpan dengan pesanan sehingga Anda dapat melihat secara tepat aturan mana yang diterapkan dan berapa kontribusi masing-masing.

## Pengaturan Umum

### Toko Eropa

1. Klik **Muat Preset** dan muat kelompok **Tingkat PPN UE**
2. Ini membuat aturan PPN untuk semua negara anggota UE dengan tingkat standar saat ini mereka
3. Secara opsional muat **PPN Inggris** jika Anda juga menjual ke Inggris

### Toko AS

1. Klik **Muat Preset** dan muat kelompok **Pajak Penjualan Negara Bagian AS**
2. Ini membuat aturan pajak penjualan untuk semua negara bagian AS yang mengumpulkan pajak penjualan
3. Untuk pajak tingkat kota, tambahkan aturan secara manual dengan bidang kota diisi dan prioritas yang lebih tinggi

### Toko Multi-Wilayah

1. Muat beberapa kelompok preset untuk setiap pasar yang Anda jual
2. Sistem menerapkan pajak yang benar berdasarkan lokasi pelanggan masing-masing
3. Sesuaikan aturan individu sesuai kebutuhan bisnis spesifik Anda

## Tips

- **Mulai dengan preset** — muat kelompok preset untuk pasar target Anda, lalu sesuaikan tingkat individu daripada membuat setiap aturan dari awal.
- **Gunakan prioritas dengan bijak** — atur nilai prioritas yang lebih tinggi untuk aturan lokal yang lebih spesifik sehingga mereka benar menggantikan aturan regional yang lebih luas.
- **Periksa pajak gabungan dengan hati-hati** — pajak gabungan jarang digunakan. Sebagian besar yurisdiksi menggunakan pajak sederhana (non-gabungan). Hanya aktifkan pajak gabungan ketika peraturan lokal secara khusus memerlukan perhitungan pajak atas pajak.
- **Jaga aturan aktif/tidak aktif** — daripada menghapus aturan pajak untuk perubahan musiman atau sementara, nonaktifkan dan aktifkan kembali ketika diperlukan.
- **Uji sebelum diluncurkan** — setelah mengatur aturan pajak Anda, buat pesanan uji dari alamat berbeda untuk memverifikasi pajak yang benar diterapkan.