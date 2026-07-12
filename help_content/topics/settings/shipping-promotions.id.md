---
title: Promosi Pengiriman
---

Aturan pengiriman menerapkan penyesuaian biaya bersyarat pada metode pengiriman berdasarkan isi keranjang, atribut pelanggan, dan zona pengiriman—secara otomatis menawarkan pengiriman gratis untuk pembelian di atas $50, menambah biaya tambahan untuk area terpencil, atau memberikan diskon pengiriman untuk pelanggan VIP. Aturan menggunakan eksekusi berbasis prioritas (prioritas tinggi terlebih dahulu) dengan bendera berhenti opsional untuk mencegah pemrosesan lebih lanjut. Setiap aturan mengevaluasi beberapa kondisi (nilai keranjang, berat, zona, produk, kelompok pelanggan) dan mengeksekusi salah satu dari 6 jenis penyesuaian biaya ketika semua kondisi cocok.

Gunakan promosi pengiriman ketika Anda membutuhkan biaya pengiriman dinamis yang berubah berdasarkan konteks pesanan, bukan hanya tingkat statis dari metode pengiriman.

## Jenis Promosi Pengiriman

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

**Kasus Penggunaan**:
- Diskon pelanggan VIP (20% diskon untuk semua pengiriman)
- Promosi musiman (15% diskon pengiriman di bulan Desember)
- Diskon pesanan besar (10% diskon pengiriman untuk 5+ item)

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

**Kasus Penggunaan**:
- Bonus pelanggan baru ($5 diskon pengiriman untuk pesanan pertama)
- Hadiah pendaftaran newsletter ($3 diskon pengiriman)
- Manfaat program loyalitas ($10 diskon pengiriman per bulan)

---

### Biaya Pengganti

**Apa yang Dilakukan**: Mengganti biaya pengiriman ke jumlah tertentu.

**Rumus**: `new_cost = fixed_amount`

**Contoh**:
```
Biaya dasar: $25
Diatur ke: $9.99
Hasil: $9.99
```

**Kasus Penggunaan**:
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

**Kasus Penggunaan**:
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

**Kasus Penggunaan**:
- Biaya pengiriman area terpencil
- Biaya penanganan item besar
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

**Kasus Penggunaan**:
- Biaya tambahan musim puncak (20% selama liburan)
- Premium pengiriman ekspres (biaya tambahan 50%)
- Biaya tambahan bahan bakar (berubah berdasarkan tingkat saat ini)

---

## Kondisi Promosi

Promosi mengevaluasi **semua kondisi harus lulus** untuk aturan berlaku:

### Validitas Waktu

- **Tanggal Mulai**: Aturan hanya aktif setelah tanggal ini
- **Tanggal Berakhir**: Aturan hanya aktif sebelum tanggal ini
- **Kasus Penggunaan**: Promosi musiman, penawaran terbatas waktu

**Contoh**: Pengiriman gratis hanya akhir pekan Black Friday
```
Mulai: 2026-11-27 00:00
Berakhir: 2026-11-30 23:59
```

---

### Rentang Nilai Keranjang

- **Nilai Keranjang Minimum**: Subtotal keranjang harus ≥ jumlah
- **Nilai Keranjang Maksimum**: Subtotal keranjang harus ≤ jumlah
- **Kasus Penggunaan**: Ambang batas pengiriman gratis, diskon bertingkat

**Contoh**: Pengiriman gratis untuk pesanan $50-$200
```
Minimum: $50
Maksimum: $200
```

---

### Rentang Berat Keranjang

- **Berat Minimum**: Berat total keranjang harus ≥ jumlah
- **Berat Maksimum**: Berat total keranjang harus ≤ jumlah
- **Kasus Penggunaan**: Diskon pengiriman barang ringan, biaya tambahan untuk item berat

**Contoh**: Biaya tambahan $5 untuk pesanan di atas 20kg
```
Berat Minimum: 20kg
Berat Maksimum: null (tidak terbatas)
```

---

### Rentang Jumlah Item


- **Min Item Count**: Keranjang harus memiliki ≥ jumlah item
- **Max Item Count**: Keranjang harus memiliki ≤ jumlah item
- **Use Case**: Diskon pesanan besar, biaya item tunggal

**Contoh**: Pengiriman gratis untuk 5+ item
```
Min Items: 5
Max Items: null
```

---

### Zone Pengiriman

- **Zones**: Aturan hanya berlaku jika alamat pelanggan cocok dengan setidaknya satu zona yang dipilih
- **Empty selection**: Aturan berlaku untuk SEMUA zona
- **Use Case**: Biaya tambahan atau diskon berdasarkan zona

**Contoh**: Pengiriman gratis hanya untuk zona Domestik
```
Zones: ["Domestic USA"]
```

---

### Metode Pengiriman

- **Methods**: Aturan hanya berlaku untuk metode pengiriman tertentu
- **Empty selection**: Aturan berlaku untuk SEMUA metode
- **Use Case**: Promosi berdasarkan metode

**Contoh**: Diskon 25% untuk Pengiriman Ekspres
```
Methods: ["Express Delivery"]
```

---

### Persyaratan Produk

**Requires Products**: Keranjang harus berisi setidaknya satu dari produk ini

**Requires Categories**: Keranjang harus berisi setidaknya satu produk dari kategori-kategori ini

**Use Case**: Pengiriman gratis berdasarkan produk, bundel promosi

**Contoh**: Pengiriman gratis ketika keranjang berisi "Promotion Item A"
```
Requires Products: [Product ID 123]
```

---

### Eksklusi Produk

**Excludes Products**: Aturan tidak berlaku jika keranjang berisi salah satu dari produk ini

**Excludes Categories**: Aturan tidak berlaku jika keranjang berisi produk dari kategori-kategori ini

**Use Case**: Eksklusi produk berat/ukuran besar dari pengiriman gratis

**Contoh**: Pengiriman gratis kecuali untuk kategori furnitur
```
Excludes Categories: [Furniture]
```

---

### Kelompok Pelanggan

- **Customer Groups**: Aturan hanya berlaku untuk pelanggan dalam kelompok yang dipilih (VIP, Wholesales, dll.)
- **Empty selection**: Aturan berlaku untuk SEMUA kelompok pelanggan
- **Use Case**: Manfaat VIP, diskon grosir

**Contoh**: Diskon pengiriman 15% untuk anggota VIP
```
Customer Groups: ["VIP"]
```

---

### Pelanggan Baru

- **First Time Customer**: Toggle untuk membatasi aturan hanya berlaku untuk pelanggan tanpa pesanan sebelumnya
- **Use Case**: Penawaran selamat datang untuk pelanggan baru

**Contoh**: Diskon $5 untuk pengiriman pesanan pertama
```
First Time Customer: Yes
```

---

## Prioritas & Eksekusi Promosi

Promosi dieksekusi dalam **urutan prioritas** (angka lebih tinggi = eksekusi lebih awal):

### Mekanisme Prioritas

**Contoh Eksekusi**:
```
Promotion A (Priority 100): Free shipping if cart > $50
Promotion B (Priority 50): 10% discount on all shipping
Promotion C (Priority 1): $2 surcharge for remote zones

Cart: $60, Remote zone
Base shipping cost: $15

Step 1: Promotion A evaluates (Priority 100)
  Cart > $50? YES
  Apply: Set cost to $0
  Cost now: $0

Step 2: Promotion B evaluates (Priority 50)
  Apply 10% discount to $0
  Cost now: $0 (still free)

Step 3: Promotion C evaluates (Priority 1)
  Add $2 surcharge to $0
  Cost now: $2

Final cost: $2
```

**Stop Further Promotions Flag**:

Jika Promotion A memiliki `stop_further_promotions = True`:
```
Promotion A (Priority 100, stop_further_promotions=True): Free shipping if cart > $50
Promotion B (Priority 50): 10% discount
Promotion C (Priority 1): $2 surcharge

Cart: $60
Base: $15

Step 1: Promotion A applies, sets cost to $0
        stop_further_promotions = True → STOP

Final cost: $0 (Rules B and C never execute)
```

---

## Membuat Promosi Pengiriman

**Workflow Langkah Demi Langkah**:

1. **Navigate to Rules**
   - Settings > Shipping > Shipping Promotions
   - Click "Add Shipping Promotion"

2. **Basic Configuration**
   - **Name**: Identifier internal (misalnya, "Free Shipping Over $50")
   - **Description**: Catatan opsional (tidak ditampilkan kepada pelanggan)
   - **Active**: Toggle untuk mengaktifkan/menonaktifkan
   - **Priority**: Tetapkan urutan eksekusi (100 untuk prioritas tinggi, 1 untuk prioritas rendah)

3. **Choose Promotion Type**
   - Pilih jenis penyesuaian (diskon %, diskon tetap, set cost, gratis, biaya tambahan %, biaya tambahan tetap)
   - Masukkan jumlah atau persentase


Centang "Hentikan Promosi Lanjutan" jika aturan ini harus mencegah promosi dengan prioritas lebih rendah untuk dieksekusi

Gunakan untuk aturan akhir/absolut (misalnya, pengiriman gratis tidak boleh memiliki biaya tambahan yang ditambahkan setelahnya)

Validitas waktu: Tanggal mulai/akhir

Nilai keranjang: Min/maks

Berat keranjang: Min/maks

Jumlah item: Min/maks

Zona: Pilih zona yang berlaku

Metode: Pilih metode yang berlaku

Produk: Diperlukan atau dikecualikan

Pelanggan: Kelompok atau hanya pelanggan baru

Klik Simpan

Aturan menjadi aktif segera (jika tombol aktif diatur ke Ya)

## Skenario Umum Promosi Pengiriman

### Skenario 1: Pengiriman Gratis untuk Pembelian di Atas $50

**Tujuan**: Tawarkan pengiriman gratis ketika subtotal keranjang ≥ $50.

**Konfigurasi**

Nama: Pengiriman Gratis untuk Pembelian di Atas $50

Tipe: Pengiriman Gratis

Prioritas: 100

Kondisi:

  Nilai Minimum Keranjang: $50

Hentikan Promosi Lanjutan: Ya

### Skenario 2: Biaya Tambahan untuk Wilayah Terpencil

**Tujuan**: Tambahkan biaya tambahan $10 untuk pengiriman ke wilayah terpencil.

Nama: Biaya Tambahan Wilayah Terpencil

Tipe: Biaya Tambahan (Tetap)

Jumlah: $10

Prioritas: 50

  Zona: ["Wilayah Terpencil"]

Hentikan Promosi Lanjutan: Tidak

### Skenario 3: Diskon 20% untuk Pelanggan VIP

**Tujuan**: Pelanggan VIP mendapatkan diskon 20% untuk semua pengiriman.

Nama: Diskon Pengiriman VIP

Tipe: Diskon (Persentase)

Persentase: 20

Prioritas: 75

  Kelompok Pelanggan: ["VIP"]

### Skenario 4: Tarif Tetap untuk Liburan

**Tujuan**: Semua pengiriman dibatasi hingga $9.99 selama bulan Desember.

Nama: Promo Tarif Tetap Desember

Tipe: Tambah Biaya

Jumlah: $9.99

  Tanggal Mulai: 2026-12-01

  Tanggal Akhir: 2026-12-31

### Skenario 5: Biaya Tambahan untuk Item Berat

**Tujuan**: Tambahkan biaya $15 untuk pesanan di atas 25kg.

Nama: Biaya Tambahan Pesanan Berat

Jumlah: $15

  Berat Minimum: 25kg

### Skenario 6: Pengiriman Gratis untuk Pesanan Pertama

**Tujuan**: Pelanggan baru mendapatkan pengiriman gratis untuk pesanan pertama.

Nama: Pengiriman Gratis untuk Pesanan Pertama

  Pelanggan Baru: Ya

### Skenario 7: Pengiriman Gratis Berdasarkan Kategori

**Tujuan**: Pengiriman gratis untuk pesanan yang berisi item dari kategori promosi.

Nama: Pengiriman Gratis Kategori Promosi

Prioritas: 90

  Membutuhkan Kategori: ["Promosi"]

### Skenario 8: Eksklusi Perabot dari Pengiriman Gratis

**Tujuan**: Pengiriman gratis untuk pembelian di atas $50, kecuali jika keranjang berisi perabot.

**Solusi**: Dua aturan

**Promosi 1**

Nama: Pengiriman Gratis Umum

  Eksklusi Kategori: ["Perabot"]

**Promosi 2**

Nama: Diskon $5 untuk Pesanan Perabot

Tipe: Diskon (Tetap)

Jumlah: $5

Prioritas: 40

  Membutuhkan Kategori: ["Perabot"]

## Strategi Kombinasi Promosi

### Strategi 1: Tumpukan Diskon

**Izinkan beberapa diskon untuk ditumpuk**

Promosi A (Prioritas 100): Diskon 10% untuk VIP → stop_further_promotions=Tidak

Promosi B (Prioritas 50): Diskon 15% untuk pesanan >$100 → stop_further_promotions=Tidak

Pelanggan VIP dengan pesanan $120:

Dasar: $15

Setelah Promosi A: $13.50 (diskon 10%)

Setelah Promosi B: $11.48 (diskon 15% dari $13.50)

### Strategi 2: Aturan Eksklusif

**Hanya satu aturan yang berlaku** (prioritas tertinggi)

Promosi A (Prioritas 100): Pengiriman gratis >$50 → stop_further_promotions=Ya

Promosi B (Prioritas 50): Diskon 20% untuk semua pengiriman → stop_further_promotions=Ya

Keranjang > $50:

Promosi A berlaku → Pengiriman gratis → BERHENTI

Promosi B tidak pernah dieksekusi

**Diskon terlebih dahulu, biaya tambahan terakhir**:
```
Promotion A (Priority 100): Free shipping >$75
Promotion B (Priority 75): 15% VIP discount
Promotion C (Priority 50): 10% general discount
Promotion D (Priority 25): $5 remote area surcharge
Promotion E (Priority 1): 10% fuel surcharge

Order: $80, Remote zone, VIP customer
Base: $20
A: $80 > $75 → Free ($0)
B: VIP → 15% off $0 = $0
C: 10% off $0 = $0
D: Remote +$5 = $5
E: Fuel +10% of $5 = $5.50

Final: $5.50 (not free due to surcharges)
```

**Untuk mencegah ini, gunakan stop_further_promotions=Yes**:
```
Promotion A (Priority 100, stop=Yes): Free shipping >$75

Same order:
A: $80 > $75 → Free ($0) → STOP
Final: $0 (truly free)
```

---

## Testing Shipping Promotions

**Before going live**:

1. **Create Test Carts**
   - Cart A: $25 (below threshold)
   - Cart B: $55 (above threshold)
   - Cart C: $200 + Remote zone
   - Cart D: VIP customer

2. **Test Each Rule**
   - Proceed to checkout
   - Verify correct shipping cost displayed
   - Check rule execution order

3. **Test Priority Resolution**
   - Multiple matching rules
   - Verify highest priority executes first
   - Check stop_further_promotions behavior

4. **Test Edge Cases**
   - Cart value exactly at threshold
   - Multiple conditions matching
   - Conflicting rules

---

## Troubleshooting

**Issue 1: Promotion not applying**

**Causes**:
- Rule is inactive
- One or more conditions not met
- Higher priority rule set stop_further_promotions=Yes
- Time validity outside current date

**Solution**: Review all conditions, check priority, verify active status.

---

**Issue 2: Unexpected discount amount**

**Causes**:
- Multiple promotions stacking
- Percentage applied to already-discounted cost
- Rule priority incorrect

**Solution**: Check priority order, review stop_further_promotions flags, trace execution manually.

---

**Issue 3: Free shipping not working**

**Causes**:
- Lower priority surcharge rule adding cost after free shipping promotion
- Cart doesn't meet min value threshold
- Excluded products in cart

**Solution**: Use stop_further_promotions=Yes on free shipping promotion, verify conditions, check exclusions.

---

## Tips

- **Use high priority for free shipping** - Priority 100 ensures it executes before other adjustments
- **Set stop_further_promotions for absolute rules** - Free shipping should stop further processing
- **Test rule combinations** - Multiple promotions can interact unexpectedly
- **Use descriptive names** - "VIP 20% Discount (Priority 75)" better than "Promotion 3"
- **Document complex logic** - Add notes in description field
- **Start with simple promotions** - Add complexity gradually
- **Monitor rule performance** - Check if rules are being used or causing confusion
- **Avoid excessive promotions** - Too many promotions slow checkout, use 5-10 max
- **Use zones for geography** - Better than multiple similar rules per country
- **Combine with methods** - Rules + Methods work together for sophisticated pricing
- **Set clear time windows** - Always include end dates for promotions
- **Test edge cases** - Exactly $50, exactly 5 items, etc.