---
title: Metode Pengiriman
---

Metode pengiriman adalah opsi pengiriman yang ditampilkan kepada pelanggan saat checkout—setiap metode menghitung biaya pengiriman menggunakan strategi harga yang berbeda. Spwig mendukung 7 jenis metode pengiriman, mulai dari tarif flat sederhana hingga harga real-time yang dihitung oleh penyedia pengiriman yang kompleks. Metode dapat dibatasi berdasarkan nilai pesanan minimum/maksimum, berat, dan zona geografis. Pelanggan memilih metode yang mereka prefer saat checkout, dan biaya yang dihitung ditambahkan ke total pesanan mereka.

Gunakan panduan ini untuk mengonfigurasi metode pengiriman yang sesuai dengan model bisnis Anda, mulai dari pengiriman flat-rate dasar hingga harga berbasis zona yang kompleks.

## Jenis-Jenis Metode Pengiriman

Spwig menyediakan 7 jenis metode pengiriman, masing-masing dengan logika perhitungan biaya yang berbeda:

### Pengiriman Tarif Flat

**Apa Itu**: Biaya tetap tanpa memandang isi keranjang, tujuan, atau berat.

**Kapan Digunakan**:
- Toko sederhana dengan biaya pengiriman yang dapat diprediksi
- Jenis produk tunggal (ukuran/berat yang mirip)
- Pengiriman domestik dengan tarif standar penyedia pengiriman
- Promosi pengiriman gratis (gunakan dengan aturan pengiriman)

**Konfigurasi**:
- Setel **Jenis Metode** = Pengiriman Tarif Flat
- Masukkan **Biaya Tetap** (misalnya, $9.99)
- Opsional: Setel batasan nilai pesanan minimum/maksimum

**Contoh**: "Pengiriman Standar - $9.99" untuk semua pesanan domestik.

---

### Pengiriman Gratis

**Apa Itu**: Opsi pengiriman dengan biaya nol (tidak ada biaya untuk pelanggan).

**Kapan Digunakan**:
- Promosi pengiriman gratis
- Pesanan bernilai tinggi (gabungkan dengan nilai pesanan minimum)
- Alternatif pengambilan lokal
- Keuntungan program loyalitas

**Konfigurasi**:
- Setel **Jenis Metode** = Pengiriman Gratis
- Opsional: Setel **Nilai Pesanan Minimum** (misalnya, gratis untuk pesanan di atas $50)
- Bekerja dengan baik bersama aturan pengiriman untuk pengiriman gratis kondisional

**Contoh**: "Pengiriman Gratis untuk Pesanan di Atas $50" dengan min_order_value = $50.

---

### Pengiriman Berbasis Berat

**Apa Itu**: Biaya dihitung dari tabel tarif bertingkat berdasarkan berat total keranjang.

**Kapan Digunakan**:
- Produk dengan berat variabel (buku, peralatan, makanan)
- Model harga penyedia pengiriman berbasis berat
- Rasio berat ke biaya yang dapat diprediksi

**Konfigurasi**:
1. Setel **Jenis Metode** = Berbasis Berat
2. Buat **Tabel Tarif Pengiriman** dengan basis_type = "weight"
3. Tambahkan **Tingkat Tarif Pengiriman** (misalnya, 0-5kg = $10, 5-10kg = $15, 10-20kg = $25)
4. Opsional: Batasi ke zona tertentu

**Contoh**:
```
0-2kg: $8
2-5kg: $12
5-10kg: $18
10kg+: $25
```

**Cara Kerjanya**: Keranjang menghitung total berat → menemukan tingkat yang cocok → mengembalikan tarif tingkat tersebut.

---

### Pengiriman Berbasis Harga

**Apa Itu**: Biaya dihitung dari tabel tarif bertingkat berdasarkan subtotal keranjang.

**Kapan Digunakan**:
- Biaya pengiriman berkorelasi dengan nilai pesanan
- Dorong nilai keranjang yang lebih tinggi (tarif per dolar lebih rendah di tingkat yang lebih tinggi)
- Alternatif sederhana untuk berbasis berat untuk item dengan harga serupa

**Konfigurasi**:
1. Setel **Jenis Metode** = Berbasis Harga
2. Buat **Tabel Tarif Pengiriman** dengan basis_type = "price"
3. Tambahkan **Tingkat Tarif Pengiriman** (misalnya, $0-$50 = $9.99, $50-$100 = $14.99, $100+ = $19.99)

**Contoh**:
```
$0-$25: $6.99
$25-$75: $9.99
$75-$150: $12.99
$150+: Gratis
```

**Cara Kerjanya**: Keranjang menghitung subtotal → menemukan tingkat yang cocok → mengembalikan tarif tingkat tersebut.

---

### Tarif Pengiriman Real-Time

**Apa Itu**: Tarif langsung yang diambil dari API penyedia pengiriman (FedEx, UPS, DHL) saat checkout.

**Kapan Digunakan**:
- Biaya pengiriman bervariasi berdasarkan tujuan
- Opsi penyedia pengiriman yang berbeda untuk pelanggan
- Harga penyedia yang akurat tanpa tabel tarif manual
- Pengiriman internasional dengan harga yang kompleks

**Konfigurasi**:
1. Setel **Jenis Metode** = Real-Time
2. Buat **Akun Penyedia** (Pengaturan > Pengiriman > Akun Penyedia)
3. Masukkan kredensial API penyedia pengiriman (nomor akun, kunci API, rahasia)
4. Hubungkan akun penyedia ke metode pengiriman
5. Opsional: Tambahkan persentase markup atau markup tetap

**Persyaratan**:
- Akun penyedia aktif (FedEx, UPS, DHL, dll.)
- Kredensial API dari penyedia pengiriman
- Paket pengiriman yang didefinisikan (untuk perhitungan berat dimensi)

**Contoh**: Metode "FedEx Ground" mengambil tarif langsung FedEx berdasarkan berat keranjang, dimensi, dan tujuan saat checkout.

**Cara Kerjanya**:
1. Pelanggan memasukkan alamat saat checkout
2. Sistem memanggil API penyedia dengan asal, tujuan, dimensi paket, berat
3. Penyedia mengembalikan kutipan tarif
4. Markup opsional diterapkan
5. Tarif ditampilkan kepada pelanggan

---

### Pengambilan Lokal

**Apa Itu**: Pelanggan mengambil pesanan di lokasi fisik (tidak ada biaya pengiriman).

**Kapan Digunakan**:
- Toko ritel yang menawarkan pengambilan
- Opsi pengambilan gudang
- Acara atau tenda pasar
- Menghilangkan biaya pengiriman untuk pelanggan lokal

**Konfigurasi**:
1. Setel **Jenis Metode** = Pengambilan Lokal
2. Buat **Lokasi** (Pengaturan > Pengiriman > Lokasi)
   - Setel alamat, jam operasional, kapasitas pengambilan
3. Hubungkan lokasi (lokasi) ke metode
4. Opsional: Setel waktu persiapan pengambilan (misalnya, "Siap dalam 2 jam")

**Pengalaman Pelanggan**:
- Memilih "Pengambilan Lokal" saat checkout
- Memilih lokasi pengambilan (jika ada beberapa)
- Memilih tanggal/waktu pengambilan berdasarkan ketersediaan
- Menerima notifikasi saat pesanan siap

**Contoh**: "Ambil di Toko - Gratis" dengan 3 lokasi ritel, siap dalam 24 jam.

---

### Pengiriman Berdasarkan Tabel

**Apa Itu**: Harga bertingkat fleksibel berdasarkan berat, harga, atau kuantitas dengan penargetan zona yang canggih.

**Kapan Digunakan**:
- Harga kompleks (tarif berbeda berdasarkan zona DAN berat)
- Membutuhkan kontrol lebih dari berbasis berat atau berbasis harga saja
- Faktor harga yang berbeda (misalnya, berat + tujuan + kuantitas)

**Konfigurasi**:
1. Setel **Jenis Metode** = Berdasarkan Tabel
2. Buat **Tabel Tarif Pengiriman**
3. Definisikan **basis_type**: berat, harga, atau kuantitas
4. Tambahkan **Tingkat Tarif Pengiriman** dengan nilai minimum/maksimum
5. Opsional: Batasi tingkat ke zona atau negara tertentu

**Perbedaan dari Berbasis Berat/Harga**: Tabel tarif mendukung pembatasan geografis per tingkat, memungkinkan tarif berbeda untuk berat/harga yang sama di zona berbeda.

**Contoh**:
```
Zona A (Domestik):
  0-5kg: $10
  5-10kg: $15

Zona B (Terpencil):
  0-5kg: $18
  5-10kg: $25
```

**Cara Kerjanya**: Keranjang menghitung nilai basis (berat/harga/kuantitas) → menemukan tingkat yang cocok untuk zona pelanggan → mengembalikan tarif tingkat tersebut.

---

## Konfigurasi Metode Pengiriman

Semua metode pengiriman memiliki pengaturan umum berikut:

### Pengaturan Dasar

- **Nama**: Identifikasi internal (tidak ditampilkan kepada pelanggan)
- **Nama Tampilan**: Nama yang ditujukan kepada pelanggan saat checkout (misalnya, "Pengiriman Standar", "Pengiriman Ekspres")
- **Deskripsi**: Teks bantuan opsional yang ditampilkan saat checkout (misalnya, "Pengiriman dalam 3-5 hari kerja")
- **Jenis Metode**: Satu dari 7 jenis di atas
- **Aktif**: Toggle untuk mengaktifkan/menonaktifkan metode tanpa menghapusnya

### Pengaturan Biaya

- **Biaya Tetap**: Hanya untuk metode flat-rate
- **Tabel Tarif**: Untuk metode berbasis berat, berbasis harga, dan berbasis tabel
- **Akun Penyedia**: Untuk metode real-time
- **Kelas Pajak**: Terapkan pajak ke biaya pengiriman (jika berlaku)

### Pembatasan

**Pembatasan Nilai Pesanan**:
- **Nilai Pesanan Minimum**: Metode hanya tersedia jika subtotal keranjang ≥ jumlah (misalnya, pengiriman gratis untuk pesanan di atas $50)
- **Nilai Pesanan Maksimum**: Metode disembunyikan jika subtotal keranjang > jumlah (misalnya, flat rate hanya untuk pesanan di bawah $100)

**Pembatasan Berat**:
- **Berat Minimum**: Metode hanya tersedia jika berat keranjang ≥ jumlah
- **Berat Maksimum**: Metode disembunyikan jika berat keranjang > jumlah (umum untuk opsi pengiriman berat ringan)

**Pembatasan Geografis**:
- **Zona Pengiriman**: Hubungkan metode ke zona tertentu (domestik, internasional, regional)
- Zona kosong = tersedia untuk semua alamat
- Banyak zona = tersedia untuk zona yang cocok

### Pengaturan Lanjutan

- **Prioritas**: Urutan tampil di checkout (angka lebih rendah = lebih tinggi dalam daftar)
- **Biaya Penanganan**: Biaya tambahan tetap yang ditambahkan ke biaya yang dihitung
- **Ambang Batas Pengiriman Gratis**: Setel biaya ke $0 jika subtotal keranjang ≥ ambang batas (alternatif dari min_order_value)

---

## Membuat Metode Pengiriman

**Alur Kerja Langkah Demi Langkah**:

1. **Navigasi ke Metode Pengiriman**
   - Pergi ke Pengaturan > Keranjang > Metode Pengiriman
   - Klik "Tambah Metode Pengiriman"

2. **Pilih Jenis Metode**
   - Pilih jenis yang sesuai berdasarkan strategi harga Anda
   - Jenis menentukan bidang konfigurasi biaya yang tersedia

3. **Konfigurasi Informasi Dasar**
   - Nama: Referensi internal (misalnya, "domestic_ground")
   - Nama Tampilan: Untuk pelanggan (misalnya, "Pengiriman Ground")
   - Deskripsi: Waktu pengiriman (misalnya, "5-7 hari kerja")

4. **Setel Perhitungan Biaya**
   - **Flat Rate**: Masukkan biaya tetap
   - **Berat/Harga/Tabel Tarif**: Buat tabel tarif (lihat di bawah)
   - **Real-Time**: Hubungkan akun penyedia
   - **Gratis/Pengambilan**: Tidak perlu konfigurasi biaya

5. **Tambahkan Pembatasan (Opsional)**
   - Nilai pesanan minimum/maksimum
   - Berat minimum/maksimum
   - Zona pengiriman

6. **Setel Prioritas**
   - Angka lebih rendah muncul lebih dulu di checkout
   - Rekomendasi urutan: Gratis (1), Pengambilan Lokal (2), Standar (3), Ekspres (4)

7. **Aktifkan Metode**
   - Toggle "Aktif" = Ya
   - Simpan

---

## Membuat Tabel Tarif

Untuk metode berbasis berat, berbasis harga, dan berbasis tabel:

**Langkah 1: Membuat Tabel Tarif**
- Pergi ke Pengaturan > Pengiriman > Tabel Tarif
- Klik "Tambah Tabel Tarif"
- Setel **Nama** (misalnya, "Tingkat Berat Domestik")
- Setel **Jenis Basis**: berat, harga, atau kuantitas

**Langkah 2: Menambahkan Tingkat**
- Klik "Tambah Tingkat"
- Setel **Nilai Minimum** dan **Nilai Maksimum** (rentang untuk cocok)
- Setel **Tarif** (biaya untuk tingkat ini)
- Opsional: Batasi ke zona atau negara tertentu
- Simpan tingkat

**Langkah 3: Ulangi untuk Semua Tingkat**
- Tutup rentang penuh (0 hingga nilai maksimum yang diperkirakan)
- Pastikan tidak ada celah (misalnya, 0-5, 5-10, 10-20, 20+)
- Gunakan `null` untuk nilai maksimum di tingkat terakhir (tidak terbatas)

**Langkah 4: Hubungkan ke Metode Pengiriman**
- Edit metode pengiriman
- Pilih tabel tarif dari dropdown
- Simpan

**Contoh Tabel Berbasis Berat**:
```
Nama: Tingkat Berat Domestik
Basis: Berat

Tingkat:
1. Min: 0g, Max: 2000g, Tarif: $8
2. Min: 2000g, Max: 5000g, Tarif: $12
3. Min: 5000g, Max: 10000g, Tarif: $18
4. Min: 10000g, Max: null, Tarif: $25
```

---

## Skenario Pengiriman Umum

### Skenario 1: Pengiriman Domestik Dasar

**Tujuan**: Tarif flat $9.99 sederhana untuk semua pesanan domestik.

**Solusi**:
- Jenis Metode: Tarif Flat
- Biaya Tetap: $9.99
- Zona Pengiriman: "Domestik" (hanya negara Anda)

---

### Skenario 2: Pengiriman Gratis untuk Pesanan di Atas $50

**Tujuan**: Dorong nilai keranjang yang lebih tinggi dengan ambang batas pengiriman gratis.

**Solusi Opsi A** (Direkomendasikan):
- Jenis Metode: Pengiriman Gratis
- Nilai Pesanan Minimum: $50
- Nama Tampilan: "Pengiriman Gratis (Pesanan $50+)")

**Solusi Opsi B** (Menggunakan Aturan):
- Jenis Metode: Tarif Flat
- Biaya Tetap: $9.99
- Membuat Aturan Pengiriman:
  - Kondisi: Nilai keranjang ≥ $50
  - Tindakan: Setel biaya ke $0

---

### Skenario 3: Pengiriman Berbasis Berat Domestik + Internasional

**Tujuan**: Tarif berbeda untuk domestik vs internasional berdasarkan berat.

**Solusi**:
1. Membuat 2 zona: "Domestik", "Internasional"
2. Membuat 2 tabel tarif: "Berat Domestik", "Berat Internasional"
3. Membuat 2 metode:
   - "Pengiriman Domestik" → menghubungkan zona Domestik + tabel tarif Berat Domestik
   - "Pengiriman Internasional" → menghubungkan zona Internasional + tabel tarif Berat Internasional

---

### Skenario 4: Opsi Penyedia Pengiriman Beragam

**Tujuan**: Izinkan pelanggan memilih antara FedEx Ground, FedEx Express, UPS Ground.

**Solusi**:
1. Membuat Akun Penyedia untuk API FedEx
2. Membuat Akun Penyedia untuk API UPS
3. Membuat 3 metode real-time:
   - "FedEx Ground" → penyedia FedEx, kode layanan = "FEDEX_GROUND"
   - "FedEx Express" → penyedia FedEx, kode layanan = "FEDEX_EXPRESS"
   - "UPS Ground" → penyedia UPS, kode layanan = "UPS_GROUND"
4. Semua 3 metode memanggil API penyedia saat checkout dan menampilkan tarif langsung

---

### Skenario 5: Pengambilan Lokal + Pengiriman

**Tujuan**: Toko ritel menawarkan opsi pengambilan dan pengiriman.

**Solusi**:
1. Membuat Lokasi: "Toko Utama" dengan alamat, jam, waktu persiapan
2. Membuat 2 metode:
   - "Pengambilan Lokal" → jenis Pengambilan Lokal, menghubungkan lokasi Toko Utama
   - "Pengiriman Standar" → Tarif Flat $9.99
3. Pelanggan melihat kedua opsi saat checkout

---

## Pengujian Metode Pengiriman

Sebelum diluncurkan, uji semua metode:

1. **Buat Keranjang Uji**
   - Tambahkan produk dengan berbagai berat/harga
   - Lanjutkan ke checkout

2. **Uji Setiap Metode**
   - Masukkan alamat di zona berbeda
   - Verifikasi metode yang benar muncul
   - Periksa biaya yang dihitung sesuai ekspektasi

3. **Uji Pembatasan**
   - Tambahkan item hingga nilai pesanan minimum tercapai → verifikasi pengiriman gratis muncul
   - Tambahkan item berat → verifikasi tingkat berat berfungsi
   - Uji pembatasan zona → verifikasi metode disembunyikan untuk zona yang dikecualikan

4. **Uji Metode Real-Time** (jika berlaku)
   - Gunakan kredensial uji penyedia
   - Verifikasi tarif dikembalikan dengan sukses
   - Periksa akurasi tarif terhadap situs penyedia

---

## Penyelesaian Masalah

**Masalah 1: Metode tidak muncul saat checkout**

**Penyebab**:
- Metode tidak aktif
- Keranjang tidak memenuhi nilai pesanan minimum/maksimum
- Keranjang tidak memenuhi berat minimum/maksimum
- Alamat pelanggan tidak cocok dengan zona yang terhubung
- Tidak ada tingkat tabel tarif yang menutupi berat/harga keranjang

**Solusi**: Periksa pembatasan, verifikasi status aktif, pastikan zona/tingkat menutupi skenario pelanggan.

---

**Masalah 2: Tarif real-time gagal**

**Penyebab**:
- Kredensial API tidak valid
- Akun penyedia tidak aktif
- Tidak ada paket pengiriman yang didefinisikan (penyedia membutuhkan dimensi)
- Alamat asal tidak disetel
- API penyedia sedang down

**Solusi**: Uji koneksi penyedia, verifikasi kredensial, pastikan paket dikonfigurasi, periksa alamat asal di pengaturan.

---

**Masalah 3: Biaya yang dihitung salah**

**Penyebab**:
- Tingkat tabel tarif memiliki celah atau tumpang tindih
- Nilai minimum/maksimum tingkat dalam satuan yang salah (gram vs kg)
- Biaya penanganan ditambahkan secara tidak diinginkan
- Aturan pengiriman memodifikasi biaya

**Solusi**: Periksa tingkat tabel tarif, verifikasi satuan, periksa prioritas aturan pengiriman.

---

## Tips

- **Mulai sederhana** - Gunakan tarif flat untuk metode pertama, tambahkan kompleksitas jika diperlukan
- **Uji secara menyeluruh** - Verifikasi semua metode bekerja di lingkungan staging sebelum mengaktifkan di produksi
- **Gunakan nama deskriptif** - "Pengiriman Standar (5-7 hari)" lebih baik daripada "Metode 1"
- **Setel waktu pengiriman yang realistis** - Under-promise, over-deliver untuk kepuasan pelanggan
- **Tawarkan pengambilan jika memungkinkan** - Mengurangi biaya pengiriman, meningkatkan kenyamanan pelanggan
- **Pantau keandalan API penyedia** - Siapkan fallback tarif flat jika tarif real-time gagal
- **Gunakan zona untuk pengiriman internasional** - Tarif berbeda berdasarkan wilayah mencegah kerugian di destinasi yang mahal
- **Gabungkan dengan aturan pengiriman** - Aturan menambahkan logika kondisional (promosi pengiriman gratis, biaya tambahan untuk area terpencil)
- **Batasi metode** - 2-4 opsi di checkout mencegah kebingungan pengambilan keputusan
- **Perbarui tabel tarif secara musiman** - Tarif penyedia berubah, tinjau setiap tahun
- **Gunakan prioritas dengan bijak** - Letakkan opsi gratis/cheaper di depan, opsi mahal di akhir
