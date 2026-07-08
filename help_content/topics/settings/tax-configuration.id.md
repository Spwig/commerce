---
title: Konfigurasi Pajak
---

Tarif pajak mendefinisikan pajak penjualan, PPN, dan pajak konsumsi lainnya yang diterapkan saat checkout berdasarkan lokasi pelanggan dan jenis produk—konfigurasikan tarif tingkat negara/propinsi/kota dengan pengecualian kategori produk opsional. Spwig mendukung pajak majemuk (pajak atas pajak), pemilihan tarif berbasis prioritas, dan kelompok pengaturan pajak prasetel untuk pengaturan cepat sistem pajak regional (PPN UE, Pajak Penjualan AS). Tarif dapat mengecualikan jenis produk tertentu (makanan, buku, barang digital) atau kategori untuk mematuhi hukum pajak lokal.

Gunakan konfigurasi pajak untuk memastikan kepatuhan hukum terhadap persyaratan pengumpulan pajak di yurisdiksi penjualan Anda.

## Konfigurasi Tarif Pajak

Setiap tarif pajak mendefinisikan:

**Cakupan Geografis**:
- Negara (wajib)
- Propinsi/Provinsi (opsional)
- Kota (opsional)
- Pola Kode Pos (opsional, regex)

**Detail Tarif**:
- **Tarif Pajak**: Persentase (contoh, 8,5%)
- **Nama**: Nama tampilan (contoh, "California Sales Tax")
- **Prioritas**: Prioritas yang lebih tinggi menang saat beberapa tarif cocok
- **Aktif**: Toggle tanpa penghapusan

**Pengecualian**:
- **Jenis Produk yang Dikecualikan**: Barang digital, barang fisik, jasa
- **Kategori yang Dikecualikan**: Kategori produk tertentu (Makanan, Buku, Medis)

**Pajak Majemuk**:
- **Apakah Pajak Majemuk**: Terapkan tarif ini di atas pajak sebelumnya (pajak atas pajak)
- Contoh: Pajak PST Quebec majemuk atas GST

---

## Skenario Pajak Umum

### Pajak Penjualan AS (Tingkat Propinsi)

```
Nama: California Sales Tax
Negara: US
Propinsi: CA
Tarif: 7,25%
Prioritas: 50
```

### PPN UE (Tingkat Negara)

```
Nama: UK VAT
Negara: GB
Tarif: 20%
Prioritas: 50

Nama: Germany VAT
Negara: DE
Tarif: 19%
Prioritas: 50
```

### GST/PST Kanada (Majemuk)

```
Tarif 1: GST Federal
Negara: CA
Tarif: 5%
Prioritas: 100
Apakah Pajak Majemuk: Tidak

Tarif 2: PST Quebec
Negara: CA
Propinsi: QC
Tarif: 9,975%
Prioritas: 50
Apakah Pajak Majemuk: Ya  (diterapkan pada subtotal + GST)
```

### Pajak Tingkat Kota

```
Nama: Seattle Sales Tax
Negara: US
Propinsi: WA
Kota: Seattle
Tarif: 10,1%
Prioritas: 100
```

---

## Pengecualian Pajak

### Pengecualian Jenis Produk

Pengecualian jenis produk secara keseluruhan:

- **Barang Digital**: Perangkat lunak, e-book, musik
- **Barang Fisik**: Produk nyata
- **Jasa**: Konsultasi, pemasangan

Contoh: PPN UE tidak berlaku untuk barang digital untuk konsumen (dalam beberapa kasus)

### Pengecualian Kategori

Pengecualian kategori produk tertentu:

- Makanan & Groceries (sering dikecualikan atau dengan tarif yang lebih rendah)
- Buku & Bahan Pendidikan
- Alat Kesehatan & Obat-obatan
- Pakaian (beberapa yurisdiksi)

Konfigurasi:
```
Nama: California Sales Tax
Tarif: 7,25%
Kategori yang Dikecualikan: ["Makanan & Minuman", "Obat-obatan Resep"]
```

---

## Kelompok Pajak Prasetel

Muat cepat konfigurasi pajak umum:

**Prasetel Pajak Penjualan AS**:
- Semua 50 negara bagian + DC
- Tarif tingkat negara bagian
- Otomatis diperbarui saat tarif berubah

**Prasetel PPN UE**:
- Semua 27 negara anggota UE
- Tarif PPN standar
- Logika pengembalian untuk B2B

**Untuk Menggunakan Prasetel**:
1. Pengaturan > Keranjang > Prasetel Pajak
2. Pilih kelompok prasetel (contoh, "US Sales Tax 2026")
3. Klik "Muat Prasetel"
4. Tarif diimpor secara otomatis
5. Sesuaikan jika diperlukan

---

## Resolusi Prioritas

Ketika beberapa tarif cocok, prioritas tertinggi menang:

Contoh:
```
Pelanggan di Seattle, WA:

Tarif A: Federal AS (Prioritas 1) - 0%
Tarif B: Negara Bagian Washington (Prioritas 50) - 6,5%
Tarif C: Kota Seattle (Prioritas 100) - 3,6%

Hasil: Tarif Seattle (total 10,1%) berlaku
```

---

## Opsi Tampilan Pajak

Konfigurasikan di Pengaturan > Keranjang > Pengaturan Pajak:

- **Harga Termasuk Pajak**: Tampilkan harga dengan pajak termasuk (gaya UE)
- **Tampilkan Pajak Terpisah**: Tunjukkan pajak sebagai item terpisah (gaya AS)
- **Bulatkan Pajak**: Per item atau per pesanan
- **Label Pajak**: Sesuaikan label ("PPN", "Pajak Penjualan", "GST")

---

## Pengujian Konfigurasi Pajak

Sebelum diluncurkan:

1. Buat pesanan uji dari berbagai yurisdiksi
2. Verifikasi tarif pajak yang benar diterapkan
3. Periksa apakah pengecualian bekerja untuk kategori yang dikecualikan
4. Uji perhitungan pajak majemuk
5. Tinjau item pajak pada faktur

---

## Catatan Kepatuhan

- **AS**: Aturan Nexus memerlukan pengumpulan pajak di negara bagian di mana Anda memiliki kehadiran fisik atau nexus ekonomi
- **UE**: Perusahaan yang terdaftar PPN harus mengumpulkan PPN dari pelanggan UE
- **Kanada**: GST/HST/PST bervariasi berdasarkan provinsi
- **Konsultasikan dengan profesional pajak**: Hukum pajak sering berubah, verifikasi persyaratan saat ini

---

## Tips

- **Gunakan prasetel pajak** - Lebih cepat daripada input manual, diperbarui otomatis
- **Pantau ambang batas nexus** - Lacak penjualan berdasarkan negara bagian untuk nexus ekonomi AS
- **Atur prioritas dengan benar** - Kota > Propinsi > Negara
- **Uji pajak majemuk** - Verifikasi perhitungan sesuai dengan jumlah yang diharapkan
- **Perbarui setiap tahun** - Tarif pajak berubah, tinjau setiap Januari
- **Dokumentasikan pengecualian** - Simpan catatan mengapa kategori dikecualikan
- **Gunakan nama deskriptif** - "California Sales Tax 2026" lebih baik daripada "Tax 1"
- **Aktifkan pajak secara default** - Lebih aman daripada lupa menerapkan pajak

Remember: Preserve all markdown formatting, image paths, code blocks, and technical terms exactly as shown in the preservation rules.