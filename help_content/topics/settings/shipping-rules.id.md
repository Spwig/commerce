---
title: Aturan Pengiriman
---

Aturan pengiriman menerapkan penyesuaian biaya bersyarat pada metode pengiriman berdasarkan isi keranjang, atribut pelanggan, dan zona pengiriman—secara otomatis menawarkan pengiriman gratis untuk pembelian di atas $50, menambahkan biaya tambahan untuk area terpencil, atau memberikan diskon pengiriman untuk pelanggan VIP. Aturan menggunakan eksekusi berbasis prioritas (prioritas tinggi terlebih dahulu) dengan bendera berhenti opsional untuk mencegah pemrosesan lebih lanjut. Setiap aturan mengevaluasi beberapa kondisi (nilai keranjang, berat, zona, produk, kelompok pelanggan) dan mengeksekusi salah satu dari 6 jenis penyesuaian biaya ketika semua kondisi cocok.

Gunakan aturan pengiriman ketika Anda membutuhkan biaya pengiriman dinamis yang berubah berdasarkan konteks pesanan, bukan hanya tingkat statis dari metode pengiriman.

## Jenis Aturan Pengiriman

Aturan pengiriman menerapkan 6 jenis penyesuaian biaya:

### Diskon Persentase

**Apa yang Dilakukan**: Mengurangi biaya pengiriman dengan persentase (misalnya, 25% diskon).

**Rumus**: `new_cost = base_cost × (1 - percent/100)`

**Contoh**:
```
Biaya dasar: $20
Diskon: 25%
Hasil: $15
```

**Penggunaan**:
- Diskon pelanggan VIP (20% diskon untuk semua pengiriman)
- Promosi musiman (15% diskon pengiriman di bulan Desember)
- Diskon pengiriman untuk pesanan besar (10% diskon pengiriman untuk 5+ item)

---

### Diskon Tetap

**Apa yang Dilakukan**: Mengurangi jumlah tetap dari biaya pengiriman.

**Rumus**: `new_cost = base_cost - amount` (minimum $0)

**Contoh**:
```
Biaya dasar: $15
Diskon: $5
Hasil: $10
```

**Penggunaan**:
- Bonus pelanggan baru ($5 diskon pengiriman untuk pesanan pertama)
- Hadiah pendaftaran newsletter ($3 diskon pengiriman)
- Manfaat program loyalitas ($10 diskon pengiriman per bulan)

---

### Tetapkan Biaya

**Apa yang Dilakukan**: Mengganti biaya pengiriman ke jumlah tertentu.

**Rumus**: `new_cost = fixed_amount`

**Contoh**:
```
Biaya dasar: $25
Tetapkan ke: $9.99
Hasil: $9.99
```

**Penggunaan**:
- Penjualan flash (biaya pengiriman flat $5 untuk semua pesanan hari ini)
- Pengiriman khusus kategori (buku selalu $3.99 pengiriman)
- Promosi berbasis waktu (biaya pengiriman dibatasi $9.99 minggu ini)

---

### Pengiriman Gratis

**Apa yang Dilakukan**: Menetapkan biaya pengiriman ke $0.

**Rumus**: `new_cost = $0`

**Contoh**:
```
Biaya dasar: $18
Aturan berlaku
Hasil: $0
```

**Penggunaan**:
- Pengiriman gratis untuk pembelian di atas $50
- Pengiriman gratis untuk produk tertentu (item promosi)
- Pengiriman gratis untuk pelanggan VIP
- Pengiriman gratis untuk pesanan dengan 3+ item

---

### Biaya Tambahan (Tetap)

**Apa yang Dilakukan**: Menambahkan jumlah tetap ke biaya pengiriman.

**Rumus**: `new_cost = base_cost + amount`

**Contoh**:
```
Biaya dasar: $12
Biaya tambahan: $5
Hasil: $17
```

**Penggunaan**:
- Biaya pengiriman area terpencil
- Pengelolaan item besar
- Biaya tambahan pengiriman Sabtu
- Biaya kemasan item rapuh

---

### Biaya Tambahan (Persentase)

**Apa yang Dilakukan**: Meningkatkan biaya pengiriman dengan persentase.

**Rumus**: `new_cost = base_cost × (1 + percent/100)`

**Contoh**:
```
Biaya dasar: $20
Biaya tambahan: 15%
Hasil: $23
```

**Penggunaan**:
- Biaya tambahan musim puncak (20% selama liburan)
- Premium pengiriman cepat (biaya tambahan 50%)
- Biaya bahan bakar (berubah berdasarkan tingkat saat ini)

---

## Kondisi Aturan

Aturan mengevaluasi **semua kondisi harus lulus** untuk aturan berlaku:

### Validitas Waktu

- **Tanggal Mulai**: Aturan hanya aktif setelah tanggal ini
- **Tanggal Berakhir**: Aturan hanya aktif sebelum tanggal ini
- **Penggunaan**: Promosi musiman, penawaran terbatas waktu

**Contoh**: Pengiriman gratis hanya akhir pekan Black Friday
```
Mulai: 2026-11-27 00:00
Berakhir: 2026-11-30 23:59
```

---

### Rentang Nilai Keranjang

- **Nilai Keranjang Minimum**: Subtotal keranjang harus ≥ jumlah
- **Nilai Keranjang Maksimum**: Subtotal keranjang harus ≤ jumlah
- **Penggunaan**: Ambang batas pengiriman gratis, diskon bertingkat

**Contoh**: Pengiriman gratis untuk pesanan $50-$200
```
Min: $50
Max: $200
```

---

### Rentang Berat Keranjang

- **Berat Minimum**: Berat total keranjang harus ≥ jumlah
- **Berat Maksimum**: Berat total keranjang harus ≤ jumlah
- **Penggunaan**: Diskon pengiriman berat ringan, biaya tambahan item berat

**Contoh**: Biaya tambahan $5 untuk pesanan di atas 20kg
```
Min Berat: 20kg
Max Berat: null (tidak terbatas)
```

---

### Rentang Jumlah Item

- **Jumlah Item Minimum**: Keranjang harus memiliki ≥ jumlah item
- **Jumlah Item Maksimum**: Keranjang harus memiliki ≤ jumlah item
- **Penggunaan**: Diskon pesanan besar, biaya item tunggal

**Contoh**: Pengiriman gratis untuk 5+ item
```
Min Item: 5
Max Item: null
```

---

### Zona Pengiriman

- **Zona**: Aturan hanya berlaku jika alamat pelanggan cocok dengan setidaknya satu zona yang dipilih
- **Pemilihan kosong**: Aturan berlaku untuk SEMUA zona
- **Penggunaan**: Biaya tambahan atau diskon khusus zona

**Contoh**: Pengiriman gratis hanya untuk zona Domestik
```
Zona: ["Domestic USA"]
```

---

### Metode Pengiriman

- **Metode**: Aturan hanya berlaku untuk metode pengiriman tertentu
- **Pemilihan kosong**: Aturan berlaku untuk SEMUA metode
- **Penggunaan**: Promosi khusus metode

**Contoh**: Diskon 25% untuk Pengiriman Ekspres
```
Metode: ["Express Delivery"]
```

---

### Persyaratan Produk

**Memerlukan Produk**: Keranjang harus berisi setidaknya satu dari produk ini

**Memerlukan Kategori**: Keranjang harus berisi setidaknya satu produk dari kategori ini

**Penggunaan**: Pengiriman gratis khusus produk, bundel promosi

**Contoh**: Pengiriman gratis ketika keranjang berisi "Item Promosi A"
```
Memerlukan Produk: [ID Produk 123]
```

---

### Eksklusi Produk

**Mengecualikan Produk**: Aturan tidak berlaku jika keranjang berisi salah satu produk ini

**Mengecualikan Kategori**: Aturan tidak berlaku jika keranjang berisi produk dari kategori ini

**Penggunaan**: Eksklusi item berat/berukuran besar dari pengiriman gratis

**Contoh**: Pengiriman gratis kecuali untuk kategori furnitur
```
Mengecualikan Kategori: [Furnitur]
```

---

### Kelompok Pelanggan

- **Kelompok Pelanggan**: Aturan hanya berlaku untuk pelanggan dalam kelompok yang dipilih (VIP, Grosir, dll.)
- **Pemilihan kosong**: Aturan berlaku untuk SEMUA kelompok pelanggan
- **Penggunaan**: Manfaat VIP, diskon grosir

**Contoh**: Diskon pengiriman 15% untuk anggota VIP
```
Kelompok Pelanggan: ["VIP"]
```

---

### Pelanggan Baru

- **Pelanggan Baru**: Toggle untuk membatasi aturan hanya untuk pelanggan tanpa pesanan sebelumnya
- **Penggunaan**: Penawaran selamat datang untuk pelanggan baru

**Contoh**: Diskon $5 pengiriman untuk pesanan pertama
```
Pelanggan Baru: Ya
```

---

## Prioritas dan Eksekusi Aturan

Aturan dieksekusi dalam **urutan prioritas** (angka lebih tinggi = eksekusi lebih awal):

### Mekanisme Prioritas

**Contoh Eksekusi**:
```
Aturan A (Prioritas 100): Pengiriman gratis jika keranjang > $50
Aturan B (Prioritas 50): Diskon 10% untuk semua pengiriman
Aturan C (Prioritas 1): Biaya tambahan $2 untuk zona terpencil

Keranjang: $60, Zona terpencil
Biaya pengiriman dasar: $15

Langkah 1: Aturan A dievaluasi (Prioritas 100)
  Keranjang > $50? YA
  Terapkan: Tetapkan biaya ke $0
  Biaya sekarang: $0

Langkah 2: Aturan B dievaluasi (Prioritas 50)
  Terapkan diskon 10% ke $0
  Biaya sekarang: $0 (masih gratis)

Langkah 3: Aturan C dievaluasi (Prioritas 1)
  Tambahkan $2 biaya tambahan ke $0
  Biaya sekarang: $2

Biaya akhir: $2
```

**Bendera Berhenti Eksekusi Aturan Lebih Lanjut**:

Jika Aturan A memiliki `stop_further_rules = True`:
```
Aturan A (Prioritas 100, stop_further_rules=True): Pengiriman gratis jika keranjang > $50
Aturan B (Prioritas 50): Diskon 10%
Aturan C (Prioritas 1): Biaya tambahan $2 untuk zona terpencil

Keranjang: $60
Biaya dasar: $15

Langkah 1: Aturan A berlaku, menetapkan biaya ke $0
        stop_further_rules = True → BERHENTI

Biaya akhir: $0 (Aturan B dan C tidak pernah dieksekusi)
```

---

## Membuat Aturan Pengiriman

**Alur Kerja Langkah Demi Langkah**:

1. **Navigasi ke Aturan**
   - Pengaturan > Pengiriman > Aturan Pengiriman
   - Klik "Tambah Aturan Pengiriman"

2. **Konfigurasi Dasar**
   - **Nama**: Identifikasi internal (misalnya, "Pengiriman Gratis untuk Pembelian di Atas $50")
   - **Deskripsi**: Catatan opsional (tidak ditampilkan kepada pelanggan)
   - **Aktif**: Toggle untuk mengaktifkan/menonaktifkan
   - **Prioritas**: Tetapkan urutan eksekusi (100 untuk prioritas tinggi, 1 untuk prioritas rendah)

3. **Pilih Jenis Aturan**
   - Pilih jenis penyesuaian (diskon %, diskon tetap, tetapkan biaya, gratis, biaya tambahan %, biaya tambahan tetap)
   - Masukkan jumlah atau persentase

4. **Setel Bendera Berhenti** (Opsional)
   - Centang "Berhenti Eksekusi Aturan Lebih Lanjut" jika aturan ini harus mencegah aturan dengan prioritas lebih rendah dari dieksekusi
   - Gunakan untuk aturan akhir/absolut (misalnya, pengiriman gratis tidak boleh memiliki biaya tambahan yang ditambahkan setelahnya)

5. **Definisikan Kondisi** (Opsional - biarkan kosong untuk "selalu berlaku")
   - Validitas waktu: Tanggal mulai/berakhir
   - Nilai keranjang: Min/max
   - Berat keranjang: Min/max
   - Jumlah item: Min/max
   - Zona: Pilih zona yang berlaku
   - Metode: Pilih metode yang berlaku
   - Produk: Diperlukan atau dikecualikan
   - Pelanggan: Kelompok atau hanya untuk pelanggan baru

6. **Simpan Aturan**
   - Klik Simpan
   - Aturan menjadi aktif segera (jika toggle aktif adalah Ya)

---

## Skenario Aturan Pengiriman Umum

### Skenario 1: Pengiriman Gratis untuk Pembelian di Atas $50

**Tujuan**: Menawarkan pengiriman gratis ketika subtotal keranjang ≥ $50.

**Konfigurasi**:
```
Nama: Pengiriman Gratis untuk Pembelian di Atas $50
Tipe: Pengiriman Gratis
Prioritas: 100
Kondisi:
  Nilai Keranjang Minimum: $50
Berhenti Eksekusi Aturan Lebih Lanjut: Ya
```

---

### Skenario 2: Biaya Tambahan Area Terpencil

**Tujuan**: Menambahkan biaya tambahan $10 untuk pengiriman ke area terpencil.

**Konfigurasi**:
```
Nama: Biaya Tambahan Area Terpencil
Tipe: Biaya Tambahan (Tetap)
Jumlah: $10
Prioritas: 50
Kondisi:
  Zona: ["Area Terpencil"]
Berhenti Eksekusi Aturan Lebih Lanjut: Tidak
```

---

### Skenario 3: Diskon 20% untuk Pelanggan VIP

**Tujuan**: Pelanggan VIP mendapatkan diskon 20% untuk semua pengiriman.

**Konfigurasi**:
```
Nama: Diskon Pengiriman VIP
Tipe: Diskon (Persentase)
Persentase: 20
Prioritas: 75
Kondisi:
  Kelompok Pelanggan: ["VIP"]
Berhenti Eksekusi Aturan Lebih Lanjut: Tidak
```

---

### Skenario 4: Tarif Tetap Liburan

**Tujuan**: Semua pengiriman dibatasi $9.99 selama bulan Desember.

**Konfigurasi**:
```
Nama: Promo Tarif Tetap Desember
Tipe: Tetapkan Biaya
Jumlah: $9.99
Prioritas: 100
Kondisi:
  Tanggal Mulai: 2026-12-01
  Tanggal Berakhir: 2026-12-31
Berhenti Eksekusi Aturan Lebih Lanjut: Ya
```

---

### Skenario 5: Biaya Tambahan Item Berat

**Tujuan**: Tambahkan biaya $15 untuk pesanan di atas 25kg.

**Konfigurasi**:
```
Nama: Biaya Tambahan Pesanan Berat
Tipe: Biaya Tambahan (Tetap)
Jumlah: $15
Prioritas: 50
Kondisi:
  Berat Minimum: 25kg
Berhenti Eksekusi Aturan Lebih Lanjut: Tidak
```

---

### Skenario 6: Pengiriman Gratis untuk Pesanan Pertama

**Tujuan**: Pelanggan baru mendapatkan pengiriman gratis untuk pesanan pertama.

**Konfigurasi**:
```
Nama: Pengiriman Gratis untuk Pesanan Pertama
Tipe: Pengiriman Gratis
Prioritas: 100
Kondisi:
  Pelanggan Baru: Ya
Berhenti Eksekusi Aturan Lebih Lanjut: Ya
```

---

### Skenario 7: Pengiriman Gratis untuk Kategori Promosi

**Tujuan**: Pengiriman gratis untuk pesanan yang berisi item kategori promosi.

**Konfigurasi**:
```
Nama: Pengiriman Gratis untuk Kategori Promosi
Tipe: Pengiriman Gratis
Prioritas: 90
Kondisi:
  Memerlukan Kategori: ["Promosi"]
Berhenti Eksekusi Aturan Lebih Lanjut: Ya
```

---

### Skenario 8: Eksklusi Furnitur dari Pengiriman Gratis

**Tujuan**: Pengiriman gratis untuk pembelian di atas $50, kecuali jika keranjang berisi furnitur.

**Solusi**: Dua aturan

**Aturan 1**:
```
Nama: Pengiriman Gratis Umum
Tipe: Pengiriman Gratis
Prioritas: 50
Kondisi:
  Nilai Keranjang Minimum: $50
  Mengecualikan Kategori: ["Furnitur"]
Berhenti Eksekusi Aturan Lebih Lanjut: Tidak
```

**Aturan 2**:
```
Nama: Pesanan Furnitur Diskon $5
Tipe: Diskon (Tetap)
Jumlah: $5
Prioritas: 40
Kondisi:
  Memerlukan Kategori: ["Furnitur"]
  Nilai Keranjang Minimum: $50
Berhenti Eksekusi Aturan Lebih Lanjut: Tidak
```

---

## Strategi Kombinasi Aturan

### Strategi 1: Menumpuk Diskon

**Izinkan beberapa diskon untuk menumpuk**:
```
Aturan A (Prioritas 100): Diskon 10% untuk VIP → stop_further_rules=No
Aturan B (Prioritas 50): Diskon 15% untuk pesanan >$100 → stop_further_rules=No

Pelanggan VIP dengan pesanan $120:
Biaya dasar: $15
Setelah Aturan A: $13.50 (diskon 10%)
Setelah Aturan B: $11.48 (diskon 15% dari $13.50)
```

### Strategi 2: Aturan Eksklusif

**Hanya satu aturan yang berlaku** (prioritas tertinggi):
```
Aturan A (Prioritas 100): Pengiriman gratis >$50 → stop_further_rules=Yes
Aturan B (Prioritas 50): Diskon 20% untuk semua pengiriman → stop_further_rules=Yes

Keranjang > $50:
Aturan A berlaku → Pengiriman gratis → BERHENTI
Aturan B tidak pernah dieksekusi
```

### Strategi 3: Biaya Tambahan Kondisional

**Diskon terlebih dahulu, biaya tambahan terakhir**:
```
Aturan A (Prioritas 100): Pengiriman gratis >$75
Aturan B (Prioritas 75): Diskon 15% untuk VIP
Aturan C (Prioritas 50): Diskon 10% umum
Aturan D (Prioritas 25): Biaya tambahan $5 untuk zona terpencil
Aturan E (Prioritas 1): Biaya bahan bakar 10%

Pesanan: $80, Zona terpencil, Pelanggan VIP
Biaya dasar: $20
A: $80 > $75 → Gratis ($0)
B: VIP → diskon 15% dari $0 = $0
C: diskon 10% dari $0 = $0
D: Zona terpencil +$5 = $5
E: Bahan bakar +10% dari $5 = $5.50

Akhir: $5.50 (tidak gratis karena biaya tambahan)
```

**Untuk mencegah ini, gunakan stop_further_rules=Yes**:
```
Aturan A (Prioritas 100, stop=Yes): Pengiriman gratis >$75

Pesanan yang sama:
A: $80 > $75 → Gratis ($0) → BERHENTI
Akhir: $0 (benar-benar gratis)
```

---

## Pengujian Aturan Pengiriman

**Sebelum diluncurkan**:

1. **Buat Keranjang Uji**
   - Keranjang A: $25 (di bawah ambang batas)
   - Keranjang B: $55 (di atas ambang batas)
   - Keranjang C: $200 + Zona terpencil
   - Keranjang D: Pelanggan VIP

2. **Uji Setiap Aturan**
   - Lanjutkan ke checkout
   - Verifikasi biaya pengiriman yang ditampilkan benar
   - Periksa urutan eksekusi aturan

3. **Uji Resolusi Prioritas**
   - Banyak aturan yang cocok
   - Verifikasi aturan dengan prioritas tertinggi dieksekusi terlebih dahulu
   - Periksa perilaku stop_further_rules

4. **Uji Kasus Batas**
   - Nilai keranjang tepat di ambang batas
   - Banyak kondisi cocok
   - Aturan yang bertentangan

---

## Penyelesaian Masalah

**Masalah 1: Aturan tidak berlaku**

**Penyebab**:
- Aturan tidak aktif
- Satu atau lebih kondisi tidak terpenuhi
- Aturan dengan prioritas lebih tinggi menetapkan stop_further_rules=Yes
- Validitas waktu di luar tanggal saat ini

**Solusi**: Periksa semua kondisi, periksa prioritas, verifikasi status aktif.

---

**Masalah 2: Jumlah diskon tidak terduga**

**Penyebab**:
- Banyak aturan menumpuk
- Persentase diterapkan pada biaya yang sudah didiskon
- Prioritas aturan tidak benar

**Solusi**: Periksa urutan prioritas, periksa bendera stop_further_rules, lacak eksekusi secara manual.

---

**Masalah 3: Pengiriman gratis tidak berfungsi**

**Penyebab**:
- Aturan biaya tambahan dengan prioritas lebih rendah menambahkan biaya setelah aturan pengiriman gratis
- Nilai keranjang tidak memenuhi ambang batas minimum
- Produk yang dikecualikan ada di keranjang

**Solusi**: Gunakan stop_further_rules=Yes pada aturan pengiriman gratis, verifikasi kondisi, periksa eksklusi.

---

## Tips

- **Gunakan prioritas tinggi untuk pengiriman gratis** - Prioritas 100 memastikan dieksekusi sebelum penyesuaian lain
- **Setel stop_further_rules untuk aturan absolut** - Pengiriman gratis harus menghentikan pemrosesan lebih lanjut
- **Uji kombinasi aturan** - Banyak aturan dapat berinteraksi secara tidak terduga
- **Gunakan nama deskriptif** - "Diskon VIP 20% (Prioritas 75)" lebih baik daripada "Aturan 3"
- **Dokumentasikan logika kompleks** - Tambahkan catatan di bidang deskripsi
- **Mulai dengan aturan sederhana** - Tambahkan kompleksitas secara bertahap
- **Pantau kinerja aturan** - Periksa apakah aturan digunakan atau menyebabkan kebingungan
- **Hindari aturan berlebihan** - Terlalu banyak aturan memperlambat checkout, gunakan 5-10 maksimal
- **Gunakan zona untuk geografi** - Lebih baik daripada banyak aturan serupa per negara
- **Gabungkan dengan metode** - Aturan + Metode bekerja bersama untuk harga yang canggih
- **Setel jendela waktu yang jelas** - Selalu sertakan tanggal berakhir untuk promosi
- **Uji kasus batas** - Tepat $50, tepat 5 item, dll.