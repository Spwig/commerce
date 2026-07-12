---
title: Zona Pengiriman
---

Zona pengiriman mendefinisikan wilayah geografis untuk tarif pengiriman yang ditargetkan—kelompokkan negara, negara bagian, atau kode pos ke dalam zona, lalu kaitkan metode pengiriman ke zona tertentu untuk pengendalian tarif yang tepat. Zona menggunakan pencocokan berbasis prioritas ketika alamat memenuhi beberapa zona (prioritas tertinggi menang). Sistem ini memungkinkan strategi penentuan harga yang canggih: kenakan biaya lebih tinggi untuk area terpencil, tawarkan pengiriman gratis secara domestik, atau berikan tarif diskon untuk wilayah tertentu.

Gunakan zona ketika Anda memerlukan biaya pengiriman yang berbeda untuk wilayah geografis yang berbeda, dari pembagian sederhana antara domestik vs internasional hingga penentuan harga bertingkat multi-wilayah yang kompleks.

## Memahami Zona Pengiriman

**Apa Itu Zona**: Wilayah geografis yang diberi nama dan didefinisikan oleh pola kode negara, negara bagian/provinsi, dan kode pos.

**Bagaimana Zona Bekerja**:
1. Pelanggan memasukkan alamat pengiriman saat checkout
2. Sistem mengevaluasi semua zona aktif
3. Zona yang cocok dengan alamat pelanggan menjadi kandidat
4. Jika beberapa zona cocok, zona dengan prioritas tertinggi menang
5. Metode pengiriman yang terkait dengan zona pemenang ditampilkan
6. Metode yang tidak terkait dengan zona apa pun (atau terkait dengan zona yang cocok) ditampilkan

**Komponen Zona**:
- **Nama**: Identifier zona (contoh: "Domestik", "EU", "Wilayah Terpencil")
- **Negara**: Daftar kode negara yang termasuk (kosong = semua negara)
- **Negara Bagian/Provinsi**: Batasan negara bagian per negara (opsional)
- **Pola Kode Pos**: Pola regex untuk pencocokan kode pos (opsional)
- **Prioritas**: Angka yang lebih tinggi = prioritas yang lebih tinggi ketika beberapa zona cocok

---

## Logika Pemilihan Zona

Zona menggunakan **penyempitan bertahap** untuk cocok dengan alamat:

### Tingkat 1: Pencocokan Negara

**Daftar negara kosong** → Zona cocok dengan SEMUA negara

**Daftar negara disediakan** → Negara alamat harus berada dalam daftar

Contoh:
```
Zona: "Domestik"
Negara: ["US"]
→ Cocok: Setiap alamat AS
→ Tidak cocok: Kanada, Inggris, dll.
```

### Tingkat 2: Pencocokan Negara Bagian/Provinsi

**Tidak ada negara bagian yang didefinisikan** → Zona cocok dengan SEMUA negara bagian di negara yang diizinkan

**Negara bagian didefinisikan untuk negara tertentu** → Negara bagian alamat harus cocok

Contoh:
```
Zona: "West Coast"
Negara: ["US"]
Negara Bagian: {"US": ["CA", "OR", "WA"]}
→ Cocok: Alamat California, Oregon, Washington
→ Tidak cocok: New York, Texas, dll.
```

### Tingkat 3: Pencocokan Kode Pos

**Tidak ada pola yang didefinisikan** → Zona cocok dengan SEMUA kode pos di negara yang diizinkan/negara bagian

**Pola didefinisikan** → Kode pos alamat harus cocok dengan setidaknya satu pola

Contoh:
```
Zona: "Los Angeles Metro"
Negara: ["US"]
Negara Bagian: {"US": ["CA"]}
Pola Kode Pos: ["^90[0-9]{3}$", "^91[0-9]{3}$"]
→ Cocok: 90001, 91210, 90245
→ Tidak cocok: 94102 (San Francisco)
```

**Contoh Pola Regex**:
- `^90[0-9]{3}$` - Wilayah Los Angeles (90000-90999)
- `^[A-Z][0-9][A-Z] [0-9][A-Z][0-9]$` - Format kode pos Kanada (K1A 0B1)
- `^SW[0-9]{1,2}` - Kode pos Inggris yang dimulai dengan SW

---

## Pemilihan Zona Berbasis Prioritas

Ketika beberapa zona cocok dengan alamat, **prioritas** menentukan zona mana yang berlaku:

**Bagaimana Prioritas Bekerja**:
- Angka yang lebih tinggi = prioritas yang lebih tinggi
- Jika alamat cocok dengan zona dengan prioritas 100 dan 50, prioritas 100 menang
- Hanya metode pengiriman dari zona pemenang yang tersedia

**Kasus Penggunaan**:

**Skenario 1: Spesifik Mengatasi Umum**
```
Zona A: "Wilayah Terpencil Alaska"
  Negara: ["US"]
  Negara Bagian: {"US": ["AK"]}
  Prioritas: 100

Zona B: "USA Domestik"
  Negara: ["US"]
  Prioritas: 50

Alamat: Anchorage, AK
→ Cocok dengan kedua zona
→ Prioritas 100 menang
→ Zona "Wilayah Terpencil Alaska" berlaku (biaya pengiriman lebih tinggi)
```

**Skenario 2: Kode Pos Mengatasi Negara Bagian**
```
Zona A: "Manhattan Premium"
  Negara: ["US"]
  Negara Bagian: {"US": ["NY"]}
  Pola Kode Pos: ["^100[0-2][0-9]$"]
  Prioritas: 100

Zona B: "Negara Bagian New York"
  Negara: ["US"]
  Negara Bagian: {"US": ["NY"]}
  Prioritas: 50

Alamat: New York, NY 10001
→ Cocok dengan kedua zona
→ Prioritas 100 menang
→ "Manhattan Premium" berlaku (layanan pengiriman premium)
```

---

## Membuat Zona Pengiriman

**Alur Kerja Langkah Demi Langkah**:

1. **Navigasi ke Zona**
   - Pergi ke Pengaturan > Pengiriman > Zona Pengiriman
   - Klik "Tambah Zona Pengiriman"

2. **Konfigurasi Dasar**
   - **Nama**: Identifier deskriptif (misalnya, "Uni Eropa", "West Coast", "Wilayah Terpencil")
   - **Prioritas**: Tetapkan tingkat kepentingan relatif (100 untuk spesifik, 50 untuk umum, 1 untuk fallback)
   - **Aktif**: Toggle untuk mengaktifkan/menonaktifkan

3. **Tentukan Cakupan Geografis**

   **Opsi A: Semua Negara** (biarkan daftar negara kosong)
   - Zona cocok dengan setiap alamat secara global
   - Gunakan untuk zona default/fallback

   **Opsi B: Negara Tertentu**
   - Klik "Tambahkan Negara"
   - Pilih negara dari dropdown (US, CA, UK, dll.)
   - Ulangi untuk semua negara yang termasuk

   **Opsi C: Negara Bagian/Provinsi Tertentu**
   - Setelah menambahkan negara, klik "Tambahkan Negara Bagian" untuk setiap negara
   - Pilih negara bagian dari dropdown
   - Contoh: US → CA, OR, WA untuk West Coast

   **Opsi D: Pola Kode Pos** (lanjutan)
   - Masukkan pola regex (satu per baris)
   - Uji pola dengan kode pos contoh
   - Klik "Validasi Pola" untuk memeriksa sintaks

4. **Kaitkan dengan Metode Pengiriman**
   - Metode dapat dikaitkan saat mengedit metode (bukan dalam konfigurasi zona)
   - Atau kaitkan zona ke metode yang sudah ada: Edit Metode → Zona Pengiriman → Pilih zona

5. **Tetapkan Prioritas Tampilan**
   - Zona dengan prioritas lebih tinggi akan menggantikan zona dengan prioritas lebih rendah ketika beberapa zona cocok
   - Direkomendasikan: Zona spesifik (100), Zona regional (50), Zona default (1)

6. **Aktifkan Zona**
   - Toggle "Aktif" = Ya
   - Simpan

---

## Konfigurasi Zona Umum

### Pengaturan 1: Domestik vs Internasional

**Tujuan**: Tarif berbeda untuk domestik vs semua negara lain.

```
Zona 1: "Domestik"
  Negara: [Kode Negara Anda]
  Prioritas: 50

Zona 2: "Internasional"
  Negara: [Biarkan kosong atau pilih semua negara lain]
  Prioritas: 1
```

**Metode Pengiriman**:
- "Standar Domestik" → Terkait dengan zona Domestik
- "Pengiriman Internasional" → Terkait dengan zona Internasional

---

### Pengaturan 2: Internasional Multi-Region

**Tujuan**: Tarif berbeda untuk EU, Amerika Utara, Asia, dan Wilayah Lainnya.

```
Zona 1: "Uni Eropa"
  Negara: [AT, BE, BG, CY, CZ, DE, DK, EE, ES, FI, FR, GR, HR, HU, IE, IT, LT, LU, LV, MT, NL, PL, PT, RO, SE, SI, SK]
  Prioritas: 100

Zona 2: "Amerika Utara"
  Negara: [US, CA, MX]
  Prioritas: 100

Zona 3: "Asia Pasifik"
  Negara: [AU, CN, HK, IN, JP, KR, NZ, SG, TH, TW]
  Prioritas: 100

Zona 4: "Wilayah Lainnya"
  Negara: [Biarkan kosong]
  Prioritas: 1
```

**Metode Pengiriman**:
- "Pengiriman Eropa" → Zona Eropa
- "Pengiriman Amerika Utara" → Zona Amerika Utara
- "Pengiriman Asia Pasifik" → Zona Asia Pasifik
- "Standar Internasional" → Zona Wilayah Lainnya

---

### Pengaturan 3: Tambahan Wilayah Terpencil

**Tujuan**: Tambahkan tambahan untuk kode pos terpencil dalam zona domestik.

```
Zona 1: "Domestik Terpencil"
  Negara: [US]
  Pola Pos: ["^99[0-9]{3}$", "^96[7-9][0-9]{2}$"]  # Alaska, Hawaii
  Prioritas: 100

Zona 2: "Domestik Standar"
  Negara: [US]
  Prioritas: 50
```

**Metode Pengiriman**:
- "Pengiriman Terpencil" → Zona Domestik Terpencil (biaya lebih tinggi)
- "Pengiriman Standar" → Zona Domestik Standar

---

### Pengaturan 4: Zona Berdasarkan Negara Bagian

**Tujuan**: Tarif berbeda untuk setiap wilayah di AS.

```
Zona 1: "West Coast"
  Negara: [US]
  Negara Bagian: {"US": ["CA", "OR", "WA"]}
  Prioritas: 100

Zona 2: "East Coast"
  Negara: [US]
  Negara Bagian: {"US": ["NY", "NJ", "CT", "MA", "PA"]}
  Prioritas: 100

Zona 3: "Midwest"
  Negara: [US]
  Negara Bagian: {"US": ["IL", "IN", "OH", "MI", "WI"]}
  Prioritas: 100

Zona 4: "South"
  Negara: [US]
  Negara Bagian: {"US": ["TX", "FL", "GA", "NC", "SC"]}
  Prioritas: 100

Zona 5: "Negara Bagian Lainnya di AS"
  Negara: [US]
  Prioritas: 50
```

---

## Contoh Pola Kode Pos

Kode pos menggunakan **regex** (ekspresi reguler) untuk pencocokan pola:

### Amerika Serikat (Kode ZIP)

**Format**: 5 digit (misalnya, 90210)

```
California (90000-96199):  ^9[0-6][0-9]{3}$
New York (10000-14999):    ^1[0-4][0-9]{3}$
Texas (75000-79999, 88500-88599):  ^(7[5-9]|885)[0-9]{2}$
Alaska (99500-99999):      ^99[5-9][0-9]{2}$
```

### Kanada (Kode Pos)

**Format**: A1A 1A1 (huruf-angka-huruf spasi angka-huruf-angka)


Semua kode pos Kanada:  ^[A-Z][0-9][A-Z] [0-9][A-Z][0-9]$

- **Mulai dengan 2 zona** - Domestik dan Internasional, perluas saat diperlukan
- **Gunakan prioritas dengan bijak** - Zona spesifik 100, regional 50, fallback 1
- **Uji pola pos dengan menyeluruh** - Kesalahan regex gagal secara diam-diam, menyebabkan zona tidak cocok
- **Dokumentasikan logika zona** - Tambahkan catatan ke deskripsi zona untuk menjelaskan niat cakupan
- **Hindari zona berlebihan** - Terlalu banyak zona mempersulit konfigurasi; gunakan promosi pengiriman untuk skenario kompleks
- **Gunakan kode negara, bukan nama** - "CA" bukan "California", "NY" bukan "New York"
- **Buat zona fallback** - Semua negara, prioritas 1, memastikan setidaknya satu opsi pengiriman selalu tersedia
- **Pantau kinerja zona** - Jika banyak pelanggan melihat "tidak ada pengiriman yang tersedia", audit cakupan zona
- **Perbarui zona untuk wilayah baru** - Tambahkan negara ke zona EU saat anggota baru bergabung
- **Gunakan nama yang deskriptif** - "EU (Excluding UK)" lebih baik daripada "Zone 3"
- **Uji dengan alamat nyata** - Gunakan alamat pelanggan yang sebenarnya saat pengujian, bukan alamat yang dibuat-buat