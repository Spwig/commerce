---
title: Zones Pengiriman
---

Zones pengiriman mendefinisikan wilayah geografis untuk tarif pengiriman yang ditargetkan—kelompokkan negara, negara bagian, atau kode pos ke dalam zona, lalu kaitkan metode pengiriman ke zona tertentu untuk pengendalian tarif yang tepat. Zona menggunakan pencocokan berbasis prioritas ketika alamat memenuhi beberapa zona (zona dengan prioritas tertinggi menang). Sistem ini memungkinkan strategi penentuan harga yang canggih: kenakan biaya lebih tinggi untuk wilayah terpencil, tawarkan pengiriman gratis secara domestik, atau berikan tarif diskon untuk wilayah tertentu.

Gunakan zona ketika Anda membutuhkan biaya pengiriman berbeda untuk wilayah geografis berbeda, dari pemisahan sederhana antara domestik vs internasional hingga harga bertingkat multi-wilayah yang kompleks.

## Memahami Zones Pengiriman

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
- **Pola Kode Pos**: Pola regex untuk cocokkan kode pos (opsional)
- **Prioritas**: Angka lebih tinggi = prioritas lebih tinggi ketika beberapa zona cocok

---

## Logika Cocok Zona

Zona menggunakan **penyempitan bertahap** untuk cocokkan alamat:

### Tingkat 1: Cocok Negara

**Daftar negara kosong** → Zona cocok dengan SEMUA negara

**Daftar negara disediakan** → Negara alamat harus ada dalam daftar

Contoh:
```
Zona: "Domestik"
Negara: ["US"]
→ Cocok: Alamat AS apa pun
→ Tidak cocok: Kanada, Inggris, dll.
```

### Tingkat 2: Cocok Negara Bagian/Provinsi

**Tidak ada negara bagian yang didefinisikan** → Zona cocok dengan SEMUA negara bagian dalam negara yang diizinkan

**Negara bagian didefinisikan untuk negara tertentu** → Negara bagian alamat harus cocok

Contoh:
```
Zona: "West Coast"
Negara: ["US"]
Negara Bagian: {"US": ["CA", "OR", "WA"]}
→ Cocok: Alamat California, Oregon, Washington
→ Tidak cocok: New York, Texas, dll.
```

### Tingkat 3: Cocok Kode Pos

**Tidak ada pola yang didefinisikan** → Zona cocok dengan SEMUA kode pos dalam negara yang diizinkan/negara bagian

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
- Angka lebih tinggi = prioritas lebih tinggi
- Jika alamat cocok dengan zona dengan prioritas 100 dan 50, prioritas 100 menang
- Hanya metode pengiriman dari zona pemenang yang tersedia

**Kasus Penggunaan**:

**Skenario 1: Zona Spesifik Mengatasi Zona Umum**
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

## Membuat Zones Pengiriman

**Alur Kerja Langkah Demi Langkah**:

1. **Navigasi ke Zona**
   - Pergi ke Pengaturan > Pengiriman > Zones Pengiriman
   - Klik "Tambahkan Zone Pengiriman"

2. **Konfigurasi Dasar**
   - **Nama**: Identifier deskriptif (contoh: "Uni Eropa", "West Coast", "Wilayah Terpencil")
   - **Prioritas**: Tetapkan tingkat penting relatif (100 untuk spesifik, 50 untuk umum, 1 untuk fallback)
   - **Aktif**: Toggle untuk mengaktifkan/menonaktifkan

3. **Definisikan Cakupan Geografis**

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
   - Klik "Validasi Pola" untuk memeriksa sintaksis

4. **Kaitkan ke Metode Pengiriman**
   - Metode dapat dikaitkan saat mengedit metode (tidak dalam konfigurasi zona)
   - Atau kaitkan zona ke metode yang ada: Edit Metode → Zones Pengiriman → Pilih zona

5. **Setel Prioritas Tampilan**
   - Zona dengan prioritas lebih tinggi mengatasi zona dengan prioritas lebih rendah ketika beberapa cocok
   - Direkomendasikan: Zona spesifik (100), Zona Regional (50), Zona Default (1)

6. **Aktifkan Zona**
   - Toggle "Aktif" = Ya
   - Simpan

---

## Konfigurasi Zona Umum

### Konfigurasi 1: Domestik vs Internasional

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

### Konfigurasi 2: Internasional Multi-Wilayah

**Tujuan**: Tarif berbeda untuk EU, Amerika Utara, Asia, Rest of World.

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

Zona 4: "Rest of World"
  Negara: [Biarkan kosong]
  Prioritas: 1
```

**Metode Pengiriman**:
- "Pengiriman EU" → Zona EU
- "Pengiriman Amerika Utara" → Zona Amerika Utara
- "Pengiriman Asia Pasifik" → Zona Asia Pasifik
- "Standar Internasional" → Zona Rest of World

---

### Konfigurasi 3: Biaya Tambahan Wilayah Terpencil

**Tujuan**: Tambahkan biaya tambahan untuk kode pos terpencil dalam zona domestik.

```
Zona 1: "Domestik Terpencil"
  Negara: [US]
  Pola Kode Pos: ["^99[0-9]{3}$", "^96[7-9][0-9]{2}$"]  # Alaska, Hawaii
  Prioritas: 100

Zona 2: "Domestik Standar"
  Negara: [US]
  Prioritas: 50
```

**Metode Pengiriman**:
- "Pengiriman Terpencil" → Zona Domestik Terpencil (biaya lebih tinggi)
- "Pengiriman Standar" → Zona Domestik Standar

---

### Konfigurasi 4: Zona Berdasarkan Negara Bagian

**Tujuan**: Tarif berbeda untuk setiap wilayah AS.

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

Zona 5: "Negara Bagian Lain di AS"
  Negara: [US]
  Prioritas: 50
```

---

## Contoh Pola Kode Pos

Kode pos menggunakan **regex** (ekspresi reguler) untuk cocokkan pola:

### Amerika Serikat (Kode ZIP)

**Format**: 5 digit (contoh: 90210)

```
California (90000-96199):  ^9[0-6][0-9]{3}$
New York (10000-14999):    ^1[0-4][0-9]{3}$
Texas (75000-79999, 88500-88599):  ^(7[5-9]|885)[0-9]{2}$
Alaska (99500-99999):      ^99[5-9][0-9]{2}$
```

### Kanada (Kode Pos)

**Format**: A1A 1A1 (huruf-angka-huruf spasi angka-huruf-angka)

```
Semua kode pos Kanada:  ^[A-Z][0-9][A-Z] [0-9][A-Z][0-9]$
Ontario (K, L, M, N, P):    ^[KLMNP][0-9][A-Z] [0-9][A-Z][0-9]$\nQuebec (G, H, J):           ^[GHJ][0-9][A-Z] [0-9][A-Z][0-9]$\n```

### Inggris Raya (Kode Pos)

**Format**: AA1A 1AA atau A1A 1AA

```
London (E, EC, N, NW, SE, SW, W, WC):  ^(E|EC|N|NW|SE|SW|W|WC)[0-9]{1,2}
Manchester (M):                        ^M[0-9]{1,2}
Birmingham (B):                        ^B[0-9]{1,2}
```

### Australia (Kode Pos)

**Format**: 4 digit (contoh: 2000)

```
New South Wales (1000-2999):  ^[12][0-9]{3}$
Victoria (3000-3999, 8000-8999):  ^[38][0-9]{3}$
Queensland (4000-4999, 9000-9999):  ^[49][0-9]{3}$
```

### Pengujian Pola

**Sebelum menyimpan pola**, uji dengan kode pos yang diketahui:

1. Masukkan pola: `^90[0-9]{3}$`
2. Masukkan uji: "90210" → Harus cocok
3. Masukkan uji: "10001" → Harus TIDAK cocok
4. Masukkan uji: "9021" → Harus TIDAK cocok (hanya 4 digit)

Gunakan pengujian regex online (regex101.com) untuk memvalidasi pola yang kompleks.

---

## Ringkasan Cakupan Zona

Zona menampilkan **ringkasan cakupan** dalam tampilan daftar admin yang menunjukkan apa yang termasuk:

**Contoh**:
- "Semua negara" → Tidak ada pembatasan negara
- "US, CA, MX" → 3 negara
- "US (CA, OR, WA)" → US dengan 3 negara bagian
- "US (90xxx-91xxx)" → US dengan pola kode pos

**Gunakan Ringkasan Untuk**:
- Memverifikasi cepat cakupan zona tanpa membuka
- Menemukan tumpang tindih atau celah dalam cakupan
- Memeriksa konfigurasi zona secara sekilas

---

## Mengaitkan Zona ke Metode Pengiriman

Zona dan metode memiliki **relasi banyak-ke-banyak**:

**Dari Sisi Metode** (Direkomendasikan):
1. Edit Metode Pengiriman
2. Gulir ke bagian "Zona Pengiriman"
3. Pilih zona yang berlaku (multi-pilih)
4. Simpan metode

**Dari Sisi Zona**:
- Zona tidak secara langsung terkait dengan metode
- Pengaitan selalu dilakukan dari konfigurasi metode

**Perilaku Metode-Zona**:

**Tidak ada zona yang terkait** → Metode tersedia untuk SEMUA alamat

**Zona terkait** → Metode hanya tersedia jika alamat pelanggan cocok dengan setidaknya satu zona yang terkait

**Contoh**:
```
Metode: "Standar Domestik"
Zona Terkait: ["USA Domestik"]
→ Hanya ditampilkan untuk alamat AS

Metode: "Ekspres Internasional"
Zona Terkait: ["EU", "Asia Pasifik", "Rest of World"]
→ Ditampilkan untuk semua alamat non-AS
```

---

## Pengujian Cocok Zona

Sebelum diluncurkan, uji konfigurasi zona:

1. **Buat Pesanan Uji**
   - Gunakan alamat di berbagai zona
   - Verifikasi cocok zona yang benar

2. **Periksa Resolusi Prioritas**
   - Gunakan alamat yang cocok dengan beberapa zona
   - Verifikasi zona dengan prioritas tertinggi menang
   - Konfirmasi metode pengiriman yang diharapkan muncul

3. **Uji Kasus Batas**
   - Kode pos batas (contoh: 90999 vs 91000)
   - Batas negara bagian
   - Alamat internasional dengan kode pos serupa

4. **Gunakan Alat Pratinjau Zona** (jika tersedia)
   - Masukkan alamat uji
   - Lihat zona mana yang cocok
   - Lihat resolusi prioritas

---

## Penyelesaian Masalah

**Masalah 1: Tidak ada metode pengiriman yang tersedia saat checkout**

**Penyebab**:
- Alamat pelanggan tidak cocok dengan zona apa pun
- Semua metode terkait dengan zona yang tidak cocok
- Tidak ada metode yang ada tanpa pembatasan zona

**Solusi**:
- Buat zona fallback (semua negara, prioritas 1)
- ATAU hapus pembatasan zona dari setidaknya satu metode
- Periksa pola negara/negara bagian/kode pos zona

---

**Masalah 2: Cocok zona yang salah**

**Penyebab**:
- Zona dengan prioritas lebih rendah dipilih meskipun zona dengan prioritas lebih tinggi cocok
- Kesalahan sintaksis pola kode pos (pola gagal secara diam-diam)
- Ketidakcocokan kode negara bagian (CA vs California)

**Solusi**:
- Periksa nilai prioritas (angka lebih tinggi = prioritas lebih tinggi)
- Uji pola kode pos dengan validasi regex
- Gunakan kode negara bagian 2 huruf (CA, bukan California)

---

**Masalah 3: Metode yang tidak diharapkan ditampilkan**

**Penyebab**:
- Metode tidak memiliki zona yang terkait (tersedia di semua alamat)
- Beberapa zona cocok, zona yang tidak diharapkan memiliki prioritas lebih tinggi
- Cakupan zona tumpang tindih secara tidak sengaja

**Solusi**:
- Periksa zona yang terkait dengan metode
- Periksa prioritas zona yang cocok
- Audit ringkasan cakupan zona untuk tumpang tindih

---

## Tips

- **Mulai dengan 2 zona** - Domestik dan Internasional, perluas saat diperlukan
- **Gunakan prioritas dengan bijak** - Zona spesifik 100, zona regional 50, zona fallback 1
- **Uji pola kode pos secara menyeluruh** - Kesalahan regex gagal secara diam-diam, menyebabkan zona tidak cocok
- **Dokumentasikan logika zona** - Tambahkan catatan ke deskripsi zona untuk menjelaskan niat cakupan
- **Hindari zona berlebihan** - Terlalu banyak zona mempersulit konfigurasi; gunakan aturan pengiriman untuk skenario kompleks
- **Gunakan kode negara bagian, bukan nama** - "CA" bukan "California", "NY" bukan "New York"
- **Buat zona fallback** - Semua negara, prioritas 1, memastikan setidaknya satu opsi pengiriman selalu tersedia
- **Pantau kinerja zona** - Jika banyak pelanggan melihat "tidak ada pengiriman yang tersedia", audit cakupan zona
- **Perbarui zona untuk wilayah baru** - Tambahkan negara ke zona EU ketika negara anggota baru bergabung
- **Gunakan nama deskriptif** - "EU (Tanpa UK)" lebih baik daripada "Zona 3"
- **Uji dengan alamat nyata** - Gunakan alamat pelanggan yang sebenarnya selama pengujian, bukan alamat yang dibuat-buat

Ingat: Pertahankan semua format markdown, jalur gambar, blok kode, dan istilah teknis secara tepat seperti yang ditunjukkan dalam aturan preservasi.