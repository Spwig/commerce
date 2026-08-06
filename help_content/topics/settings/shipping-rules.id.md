---
title: Aturan Pengiriman
---

Aturan pengiriman menerapkan penyesuaian biaya berdasarkan kondisi keranjang belanja, atribut pelanggan, dan zona pengiriman—menawarkan pengiriman gratis di atas $50, menambah biaya tambahan untuk area terpencil, atau mengurangi biaya pengiriman untuk pelanggan VIP. Aturan menggunakan eksekusi berbasis prioritas (prioritas tinggi terlebih dahulu) dengan bendera henti opsional untuk mencegah pemrosesan lebih lanjut. Setiap aturan mengevaluasi beberapa kondisi (nilai keranjang, berat, zona, produk, kelompok pelanggan) dan mengeksekusi salah satu dari 6 jenis penyesuaian ketika semua kondisi cocok.

Gunakan aturan pengiriman ketika Anda membutuhkan biaya pengiriman dinamis yang berubah berdasarkan konteks pesanan, bukan hanya tingkat tetap dari metode pengiriman.

## Jenis Aturan Pengiriman

Aturan pengiriman menerapkan 6 jenis penyesuaian biaya:

### Diskon Persentase

**Yang Dikerjakan**: Mengurangi biaya pengiriman dengan persentase (misalnya, diskon 25%).

**Rumus**: `new_cost = base_cost × (1 - percent/100)`

**Contoh**:
```
Biaya dasar: $20
Diskon: 25%
Hasil: $15
```

**Kasus Penggunaan**:
- Diskon pengguna VIP (diskon 20% untuk semua pengiriman)
- Promosi musiman (diskon 15% untuk pengiriman bulan Desember)
- Diskon pesanan besar (diskon 10% untuk pengiriman 5+ item)

---

### Diskon Tetap

**Yang Dikerjakan**: Mengurangi jumlah tetap dari biaya pengiriman.

**Rumus**: `new_cost = base_cost - amount` (minimum $0)

**Contoh**:
```
Biaya dasar: $15
Diskon: $5
Hasil: $10
```

**Kasus Penggunaan**:
- Bonus pelanggan pertama ($5 diskon pengiriman pesanan pertama)
- Hadiah pendaftaran newsletter ($3 diskon pengiriman)
- Manfaat program loyalitas ($10 diskon pengiriman per bulan)

---

### Biaya Tetap

**Yang Dikerjakan**: Mengganti biaya pengiriman menjadi jumlah tertentu.

**Rumus**: `new_cost = fixed_amount`

**Contoh**:
```
Biaya dasar: $25
Atur menjadi: $9.99
Hasil: $9.99
```

**Kasus Penggunaan**:
- Penjualan cepat (pengiriman flat $5 untuk semua pesanan hari ini)
- Pengiriman berdasarkan kategori (buku selalu $3.99 pengiriman)
- Promosi berdasarkan waktu (pengiriman dibatasi $9.99 minggu ini)

---

### Pengiriman Gratis

**Yang Dikerjakan**: Menetapkan biaya pengiriman menjadi $0.

**Rumus**: `new_cost = $0`

**Contoh**:
```
Biaya dasar: $18
Aturan berlaku
Hasil: $0
```

**Kasus Penggunaan**:
- Pengiriman gratis di atas $50
- Pengiriman gratis untuk produk tertentu (barang promosi)
- Pengiriman gratis untuk pelanggan VIP
- Pengiriman gratis untuk pesanan dengan 3+ item

---

### Biaya Tambahan (Tetap)

**Yang Dikerjakan**: Menambahkan jumlah tetap ke biaya pengiriman.

**Rumus**: `new_cost = base_cost + amount`

**Contoh**:
```
Biaya dasar: $12
Biaya tambahan: $5
Hasil: $17
```

**Kasus Penggunaan**:
- Biaya pengiriman ke daerah terpencil
- Pengelolaan barang besar
- Biaya pengiriman hari Sabtu
- Biaya kemasan barang rapuh

---

### Biaya Tambahan (Persentase)

**Yang Dikerjakan**: Meningkatkan biaya pengiriman dengan persentase.

**Rumus**: `new_cost = base_cost × (1 + percent/100)`

**Contoh**:
```
Biaya dasar: $20
Biaya tambahan: 15%
Hasil: $23
```

**Kasus Penggunaan**:
- Biaya tambahan musim puncak (20% selama liburan)
- Premi pengiriman ekspres (biaya tambahan 50%)
- Biaya bahan bakar (berfluktuasi berdasarkan tingkat saat ini)

---

## Kondisi Aturan

Aturan mengevaluasi **semua kondisi harus lulus** agar aturan berlaku:

### Keabsahan Waktu

- **Tanggal Mulai**: Aturan hanya aktif setelah tanggal ini
- **Tanggal Akhir**: Aturan hanya aktif sebelum tanggal ini
- **Kasus Penggunaan**: Promosi musiman, tawaran khusus waktu tertentu

**Contoh**: Pengiriman gratis akhir pekan Black Friday saja
```
Mulai: 2026-11-27 00:00
Selesai: 2026-11-30 23:59
```

---

### Rentang Nilai Keranjang

- **Nilai Keranjang Minimum**: Subtotal keranjang harus ≥ jumlah
- **Nilai Keranjang Maksimum**: Subtotal keranjang harus ≤ jumlah
- **Kasus Penggunaan**: Ambang batas pengiriman gratis, diskon berjenjang

**Contoh**: Pengiriman gratis untuk pesanan $50-$200
```
Min: $50
Max: $200
```

---

### Rentang Berat Keranjang

- **Berat Minimum**: Berat total keranjang harus ≥ jumlah
- **Berat Maksimum**: Berat total keranjang harus ≤ jumlah
- **Kasus Penggunaan**: Diskon pengiriman ringan, biaya tambahan untuk barang berat

**Contoh**: Biaya tambahan $5 untuk pesanan di atas 20kg
```
Berat Minimum: 20kg
Berat Maksimum: null (tak terbatas)
```

---

### Rentang Jumlah Item

- **Jumlah Item Minimum**: Keranjang harus memiliki ≥ jumlah item
- **Jumlah Item Maksimum**: Keranjang harus memiliki ≤ jumlah item
- **Contoh Kasus**: Diskon pesanan besar, biaya item tunggal

**Contoh**: Pengiriman gratis untuk 5+ item
```
Jumlah Item Minimum: 5
Jumlah Item Maksimum: null
```


### Wilayah Pengiriman

- **Wilayah**: Aturan hanya berlaku jika alamat pelanggan sesuai dengan salah satu wilayah yang dipilih
- **Pilihan kosong**: Aturan berlaku untuk SEMUA wilayah
- **Contoh Kasus**: Biaya tambah atau diskon khusus wilayah

**Contoh**: Pengiriman gratis hanya untuk wilayah Dalam Negeri
```
Wilayah: ["Dalam Negeri USA"]
```


### Metode Pengiriman

- **Metode**: Aturan hanya berlaku untuk metode pengiriman tertentu
- **Pilihan kosong**: Aturan berlaku untuk SEMUA metode
- **Contoh Kasus**: Promosi khusus metode

**Contoh**: Diskon 25% untuk Pengiriman Ekspres
```
Metode: ["Pengiriman Ekspres"]
```


### Persyaratan Produk

**Membutuhkan Produk**: Keranjang harus berisi setidaknya satu produk dari daftar ini

**Membutuhkan Kategori**: Keranjang harus berisi setidaknya satu produk dari kategori ini

**Contoh Kasus**: Pengiriman gratis khusus produk, paket promosi

**Contoh**: Pengiriman gratis ketika keranjang berisi "Produk Promosi A"
```
Membutuhkan Produk: [ID Produk 123]
```


### Eksklusi Produk

**Menghapus Produk**: Aturan tidak berlaku jika keranjang berisi salah satu produk ini

**Menghapus Kategori**: Aturan tidak berlaku jika keranjang berisi produk dari kategori ini

**Contoh Kasus**: Mengecualikan barang berat/ukuran besar dari pengiriman gratis

**Contoh**: Pengiriman gratis kecuali untuk kategori furniture
```
Menghapus Kategori: [Furniture]
```


### Kelompok Pelanggan

- **Kelompok Pelanggan**: Aturan hanya berlaku untuk pelanggan dalam kelompok yang dipilih (VIP, eceran, dll.)
- **Pilihan kosong**: Aturan berlaku untuk SEMUA kelompok pelanggan
- **Contoh Kasus**: Manfaat VIP, diskon eceran

**Contoh**: Diskon pengiriman 15% untuk anggota VIP
```
Kelompok Pelanggan: ["VIP"]
```


### Pelanggan Pertama Kalinya

- **Pelanggan Pertama Kalinya**: Nyalakan untuk membatasi aturan hanya pada pelanggan dengan pesanan sebelumnya
- **Contoh Kasus**: Penawaran selamat datang untuk pelanggan baru

**Contoh**: $5 diskon pengiriman untuk pesanan pertama
```
Pelanggan Pertama Kalinya: Ya
```


## Prioritas Aturan & Eksekusi

Aturan dieksekusi dalam **urutan prioritas** (angka yang lebih tinggi = eksekusi lebih dulu):

### Mekanisme Prioritas

**Contoh Eksekusi**:
```
Aturan A (Prioritas 100): Pengiriman gratis jika keranjang > $50
Aturan B (Prioritas 50): Diskon 10% pada semua pengiriman
Aturan C (Prioritas 1): Biaya tambah $2 untuk zona terpencil

Keranjang: $60, Zona Terpencil
Biaya pengiriman dasar: $15

Langkah 1: Aturan A mengevaluasi (Prioritas 100)
  Keranjang > $50? YA
  Terapkan: Atur biaya menjadi $0
  Biaya sekarang: $0

Langkah 2: Aturan B mengevaluasi (Prioritas 50)
  Terapkan diskon 10% pada $0
  Biaya sekarang: $0 (masih gratis)

Langkah 3: Aturan C mengevaluasi (Prioritas 1)
  Tambahkan biaya tambah $2 pada $0
  Biaya sekarang: $2

Biaya akhir: $2
```

**Bendera Hentikan Aturan Lain**:

Jika Aturan A memiliki `stop_further_rules = True`:
```
Aturan A (Prioritas 100, stop_further_rules=True): Pengiriman gratis jika keranjang > $50
Aturan B (Prioritas 50): Diskon 10% pada semua pengiriman
Aturan C (Prioritas 1): Biaya tambah $2 untuk zona terpencil

Keranjang: $60
Dasar: $15

Langkah 1: Aturan A berlaku, menetapkan biaya menjadi $0
        stop_further_rules = True → HENTIkan

Biaya akhir: $0 (Aturan B dan C tidak pernah dieksekusi)
```


## Membuat Aturan Pengiriman

**Workflow Langkah demi Langkah**:

1. **Navigasi ke Aturan**
   - Pengaturan > Pengiriman > Aturan Pengiriman
   - Klik "Tambahkan Aturan Pengiriman"

2. **Konfigurasi Dasar
   - **Nama**: Identifikasi internal (misalnya, "Pengiriman Gratis Lebih dari $50")
   - **Deskripsi**: Catatan opsional (tidak ditampilkan kepada pelanggan)
   - **Aktif**: Nyalakan untuk mengaktifkan/mematikan
   - **Prioritas**: Tetapkan urutan eksekusi (100 untuk prioritas tinggi, 1 untuk prioritas rendah)

3. **Pilih Jenis Aturan
   - Pilih jenis penyesuaian (diskon %, diskon tetap, atur biaya, gratis, biaya tambah %, biaya tambah tetap)
   - Masukkan jumlah atau persentase

4. **Atur Bendera Hentikan** (Opsional)
   - Centang "Hentikan Aturan Lain" jika aturan ini harus mencegah aturan dengan prioritas lebih rendah untuk dieksekusi
   - Gunakan untuk aturan terakhir/absolut (misalnya, pengiriman gratis tidak boleh memiliki biaya tambah setelahnya)

5. **Tentukan Kondisi** (Opsional - kosongkan untuk "terapkan selalu")
   - Validitas waktu: Tanggal mulai/tanggal akhir
   - Nilai keranjang: Minimum/maksimum
   - Berat keranjang: Minimum/maksimum
   - Jumlah item: Minimum/maksimum
   - Wilayah: Pilih wilayah yang sesuai
   - Metode: Pilih metode yang sesuai
   - Produk: Wajib atau dilarang
   - Pelanggan: Kelompok atau hanya pelanggan pertama kali

6. **Simpan Aturan**
   - Klik Simpan
   - Aturan langsung aktif (jika toggle aktif adalah Ya)


## Skenario Aturan Pengiriman Umum

### Skenario 1: Pengiriman Gratis Lebih dari $50

**Tujuan**: Berikan pengiriman gratis ketika subtotal keranjang ≥ $50.

**Konfigurasi**:
```
Nama: Pengiriman Gratis Lebih dari $50
Jenis: Pengiriman Gratis
Prioritas: 100
Kondisi:
  Nilai Minimum Keranjang: $50
Hentikan Aturan Lainnya: Ya
```


### Skenario 2: Biaya Tambahan Wilayah Terpencil

**Tujuan**: Tambahkan biaya tambahan sebesar $10 untuk pengiriman ke wilayah terpencil.

**Konfigurasi**:
```
Nama: Biaya Tambahan Wilayah Terpencil
Jenis: Biaya Tambahan (Jumlah Tetap)
Jumlah: $10
Prioritas: 50
Kondisi:
  Wilayah: ["Wilayah Terpencil"]
Hentikan Aturan Lainnya: Tidak
```


### Skenario 3: Diskon Pengiriman 20% untuk Pelanggan VIP

**Tujuan**: Pelanggan VIP mendapatkan diskon 20% untuk semua pengiriman.

**Konfigurasi**:
```
Nama: Diskon Pengiriman VIP
Jenis: Diskon (Persentase)
Persentase: 20
Prioritas: 75
Kondisi:
  Kelompok Pelanggan: ["VIP"]
Hentikan Aturan Lainnya: Tidak
```


### Skenario 4: Tarif Tetap Selama Liburan

**Tujuan**: Semua pengiriman dibatasi pada $9.99 selama bulan Desember.

**Konfigurasi**:
```
Nama: Promo Tarif Tetap Desember
Jenis: Harga Tetap
Jumlah: $9.99
Prioritas: 100
Kondisi:
  Tanggal Mulai: 2026-12-01
  Tanggal Akhir: 2026-12-31
Hentikan Aturan Lainnya: Ya
```


### Skenario 5: Biaya Tambahan untuk Barang Berat

**Tujuan**: Tambahkan biaya sebesar $15 untuk pesanan yang beratnya lebih dari 25kg.

**Konfigurasi**:
```
Nama: Biaya Tambahan Pesanan Berat
Jenis: Biaya Tambahan (Jumlah Tetap)
Jumlah: $15
Prioritas: 50
Kondisi:
  Berat Minimum: 25kg
Hentikan Aturan Lainnya: Tidak
```


### Skenario 6: Pengiriman Gratis untuk Pesanan Pertama

**Tujuan**: Pelanggan baru mendapatkan pengiriman gratis untuk pesanan pertama mereka.

**Konfigurasi**:
```
Nama: Pengiriman Gratis Pesanan Pertama
Jenis: Pengiriman Gratis
Prioritas: 100
Kondisi:
  Pelanggan Baru: Ya
Hentikan Aturan Lainnya: Ya
```


### Skenario 7: Pengiriman Gratis Berdasarkan Kategori

**Tujuan**: Pengiriman gratis untuk pesanan yang mencakup item kategori promosi.

**Konfigurasi**:
```
Nama: Pengiriman Gratis Kategori Promosi
Jenis: Pengiriman Gratis
Prioritas: 90
Kondisi:
  Membutuhkan Kategori: ["Promosi"]
Hentikan Aturan Lainnya: Ya
```


### Skenario 8: Eksklusi Furnitur dari Pengiriman Gratis

**Tujuan**: Pengiriman gratis lebih dari $50, kecuali jika keranjang berisi furnitur.

Solusi: Dua aturan

**Aturan 1**:
```
Nama: Pengiriman Gratis Umum
Jenis: Pengiriman Gratis
Prioritas: 50
Kondisi:
  Nilai Minimum Keranjang: $50
  Mengecualikan Kategori: ["Furnitur"]
Hentikan Aturan Lainnya: Tidak
```

**Aturan 2**:
```
Nama: Diskon $5 untuk Pesanan Furnitur
Jenis: Diskon (Jumlah Tetap)
Jumlah: $5
Prioritas: 40
Kondisi:
  Membutuhkan Kategori: ["Furnitur"]
  Nilai Minimum Keranjang: $50
Hentikan Aturan Lainnya: Tidak
```


## Strategi Kombinasi Aturan

### Strategi 1: Diskon yang Dapat Diakumulasikan

**izinkan beberapa diskon untuk diakumulasikan**:
```
Aturan A (Prioritas 100): 10% diskon untuk VIP → stop_further_rules=Tidak
Aturan B (Prioritas 50): 15% diskon untuk pesanan >$100 → stop_further_rules=Tidak

Pelanggan VIP dengan pesanan $120:
Harga dasar: $15
Setelah Aturan A: $13.50 (diskon 10%)
Setelah Aturan B: $11.48 (diskon 15% dari $13.50)
```


### Strategi 2: Aturan Eksklusif

**Hanya satu aturan yang berlaku** (prioritas tertinggi):
```
Aturan A (Prioritas 100): Pengiriman Gratis >$50 → stop_further_rules=Ya
Aturan B (Prioritas 50): Diskon 20% untuk semua pengiriman → stop_further_rules=Ya

Keranjang > $50:
Aturan A berlaku → Pengiriman Gratis → HENTIkan
Aturan B tidak pernah dijalankan
```


### Strategi 3: Biaya Tambahan yang Bergantung Kondisi

**Diskon terlebih dahulu, biaya tambahan terakhir**:
```
Aturan A (Prioritas 100): Pengiriman Gratis >$75
Aturan B (Prioritas 75): Diskon VIP 15%
Aturan C (Prioritas 50): Diskon umum 10%
Aturan D (Prioritas 25): Biaya tambahan wilayah terpencil sebesar $5
Aturan E (Prioritas 1): Biaya tambahan bahan bakar sebesar 10%

Pesanan: $80, wilayah terpencil, pelanggan VIP
Harga dasar: $20
A: $80 > $75 → Gratis ($0)
B: VIP → diskon 15% dari $0 = $0
C: diskon 10% dari $0 = $0
D: Wilayah terpencil +$5 = $5
E: Bahan bakar +10% dari $5 = $5.50
```


Preserve all markdown formatting, image paths, code blocks, and technical terms.

Akhir: $5.50 (tidak gratis karena biaya tambahan)

```

**Untuk mencegah ini, gunakan stop_further_rules=Ya**:
```
Aturan A (Prioritas 100, stop=Ya): Pengiriman gratis >$75

Pesanan yang sama:
A: $80 > $75 → Gratis ($0) → HENTI
Akhir: $0 (benar-benar gratis)
```

---

## Pengujian Aturan Pengiriman

**Sebelum diluncurkan**:

1. **Buat Keranjang Uji**
   - Keranjang A: $25 (di bawah ambang batas)
   - Keranjang B: $55 (di atas ambang batas)
   - Keranjang C: $200 + zona terpencil
   - Keranjang D: Pelanggan VIP

2. **Uji Setiap Aturan**
   - Lanjutkan ke checkout
   - Pastikan biaya pengiriman yang benar ditampilkan
   - Periksa urutan eksekusi aturan

3. **Uji Penyelesaian Prioritas**
   - Banyak aturan yang cocok
   - Pastikan prioritas tertinggi dieksekusi terlebih dahulu
   - Periksa perilaku stop_further_rules

4. **Uji Kasus-kasus Ekstrem**
   - Jumlah keranjang tepat pada ambang batas
   - Banyak kondisi yang cocok
   - Aturan yang bertentangan

---

## Masalah Umum

**Masalah 1: Aturan tidak berlaku**

**Penyebab**:
- Aturan tidak aktif
- Salah satu atau lebih kondisi tidak terpenuhi
- Aturan prioritas tinggi yang mengatur stop_further_rules=Ya
- Waktu validitas di luar tanggal saat ini

**Solusi**: Tinjau semua kondisi, periksa prioritas, pastikan status aktif.

---

**Masalah 2: Jumlah diskon yang tidak terduga**

**Penyebab**:
- Banyak aturan yang tumpang tindih
- Persentase diterapkan pada biaya yang sudah didiskon
- Prioritas aturan salah

**Solusi**: Periksa urutan prioritas, tinjau bendera stop_further_rules, lacak eksekusi secara manual.

---

**Masalah 3: Pengiriman gratis tidak berfungsi**

**Penyebab**:
- Aturan biaya tambahan prioritas rendah menambah biaya setelah aturan pengiriman gratis
- Keranjang tidak memenuhi ambang batas nilai minimum
- Produk yang dikecualikan ada di keranjang

**Solusi**: Gunakan stop_further_rules=Ya pada aturan pengiriman gratis, pastikan kondisi, periksa pengecualian.

---

## Tips

- **Gunakan prioritas tinggi untuk pengiriman gratis** - Prioritas 100 memastikan dieksekusi sebelum penyesuaian lainnya
- **Atur stop_further_rules untuk aturan mutlak** - Pengiriman gratis harus menghentikan pemrosesan lebih lanjut
- **Uji kombinasi aturan** - Banyak aturan bisa saling terkait secara tidak terduga
- **Gunakan nama yang deskriptif** - "Diskon VIP 20% (Prioritas 75)" lebih baik daripada "Aturan 3"
- **Dokumentasikan logika yang rumit** - Tambahkan catatan di bidang deskripsi
- **Mulai dengan aturan yang sederhana** - Tambahkan kompleksitas secara bertahap
- **Pantau kinerja aturan** - Periksa apakah aturan digunakan atau menyebabkan kebingungan
- **Hindari terlalu banyak aturan** - Terlalu banyak aturan memperlambat checkout, gunakan maksimal 5-10
- **Gunakan zona untuk geografi** - Lebih baik daripada banyak aturan serupa per negara
- **Gabungkan dengan metode** - Aturan + Metode bekerja sama untuk harga yang rumit
- **Atur jendela waktu yang jelas** - Selalu sertakan tanggal akhir untuk promosi
- **Uji kasus-kasus ekstrem** - Tepat $50, tepat 5 item, dll.