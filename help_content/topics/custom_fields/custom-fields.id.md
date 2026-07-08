---
title: Bidang Kustom
---

Bidang kustom memungkinkan Anda menambahkan data tambahan ke Produk, Kategori, Pesanan, dan Profil Pelanggan tanpa memodifikasi kode apa pun. Gunakan mereka untuk menyimpan informasi khusus bisnis seperti ID API eksternal, lokasi gudang, data kepatuhan, atau atribut apa pun yang diperlukan toko Anda.

## Mengakses Bidang Kustom

Navigasikan ke **Pengaturan > Bidang Kustom** di bilah sisi admin.

![Halaman Bidang Kustom](/static/core/admin/img/help/custom-fields/custom-fields-page.webp)

## Konsep Penting

### Kelompok Bidang

Bidang diorganisir ke dalam **kelompok** — kumpulan logis yang muncul bersama sebagai bagian. Misalnya, kelompok "Informasi Pengiriman" mungkin berisi bidang untuk lokasi gudang, dimensi paket, dan klasifikasi bahan berbahaya.

### Definisi Bidang

Setiap definisi bidang mengontrol:
- **Nama**: Label yang ditampilkan di formulir
- **Slug**: Kunci yang dapat dibaca mesin yang digunakan dalam penyimpanan JSON dan respons API
- **Jenis Bidang**: Jenis input yang ditampilkan (teks, angka, dropdown, dll.)
- **Validasi**: Aturan seperti min/max, panjang maksimum, regex, atau pilihan yang diizinkan
- **Visibilitas**: Apakah bidang muncul di toko online

### Jenis Bidang yang Didukung

| Jenis | Deskripsi | Penggunaan Contoh |
|------|-------------|-------------|
| **Teks** | Masukan teks satu baris | ID API eksternal, kode merek |
| **Textarea** | Teks multi-baris | Catatan penanganan khusus |
| **Angka** | Nilai bilangan bulat | Jumlah pesanan minimum |
| **Desimal** | Nilai desimal | Override berat, dimensi kustom |
| **Ya/Tidak** | Toggle checkbox | Apakah rapuh, memerlukan tanda tangan |
| **Tanggal** | Pemilih tanggal | Tanggal rilis, tanggal kedaluwarsa |
| **Tanggal & Waktu** | Pemilih tanggal dan waktu | Ketersediaan yang dijadwalkan |
| **URL** | Alamat web | Tautan pemasok, URL lembar spesifikasi |
| **Email** | Alamat email | Kontak pabrikan |
| **Dropdown** | Daftar pilihan tunggal | Jenis bahan, negara asal |
| **Multi-select** | Daftar pilihan ganda | Sertifikasi, tag |
| **Warna** | Pemilih warna | Warna merek, warna label |

## Mengelola Bidang Kustom

### Membuat Kelompok Bidang

1. Buka **Pengaturan > Bidang Kustom**
2. Pilih tab model (Produk, Kategori, Pesanan, atau Profil Pelanggan)
3. Klik **Tambahkan Kelompok**
4. Masukkan **Nama Kelompok** (misalnya, "Integrasi Eksternal")
5. Secara opsional, aktifkan **Tampilkan di toko online** jika pelanggan harus melihat bidang ini
6. Klik **Simpan Kelompok**

### Menambahkan Bidang ke Kelompok

1. Di kartu kelompok, klik **Tambahkan Bidang**
2. Masukkan **Nama Bidang** — slug dihasilkan secara otomatis
3. Pilih **Jenis Bidang**
4. Secara opsional, atur **Teks Bantuan** dan **Nilai Default**
5. Konfigurasikan opsi validasi (berbeda tergantung jenis bidang):
   - Teks: panjang maksimum, pola regex
   - Angka/Desimal: nilai minimum dan maksimum
   - Dropdown: tentukan daftar pilihan
6. Atur opsi bidang:
   - **Wajib**: Pedagang harus mengisi bidang ini saat menyimpan
   - **Tampilkan di toko online**: Tampilkan nilai pada halaman yang menghadap ke pelanggan
   - **Terjemahkan**: Izinkan nilai untuk diterjemahkan (hanya teks/textarea)
7. Klik **Simpan Bidang**

### Mengedit dan Mengurutkan Ulang

- Klik ikon **pensil** pada kelompok atau bidang apa pun untuk mengeditnya
- Tarik **pegangan grip** untuk mengurutkan ulang kelompok atau bidang dalam kelompok
- Perubahan berlaku segera di semua formulir yang relevan

### Menghapus Kelompok dan Bidang

- Klik ikon **sampah** pada kelompok atau bidang untuk menghapusnya
- Penghapusan adalah **penghapusan lunak** — data tetap disimpan di database tetapi disembunyikan dari formulir
- Ini melindungi data yang sudah ada dari kehilangan tidak sengaja

## Menggunakan Bidang Kustom di Formulir

Setelah Anda mendefinisikan bidang kustom untuk model, **Bidang Kustom** secara otomatis muncul di tab formulir edit yang sesuai.

### Produk dan Kategori

1. Buka produk atau kategori apa pun untuk diedit
2. Klik tab **Bidang Kustom**
3. Isi bidang sesuai kebutuhan
4. Klik **Simpan** — nilai disimpan bersama dengan catatan

### Pesanan

Nilai bidang kustom untuk pesanan ditampilkan sebagai **bagian hanya baca** di halaman detail pesanan. Bidang kustom pesanan biasanya ditetapkan melalui API atau saat checkout.

### Profil Pelanggan

1. Buka profil pelanggan
2. Klik tab **Bidang Kustom**
3. Isi bidang dan simpan

## Akses API

### Menampilkan Definisi Bidang

Dapatkan semua definisi bidang kustom untuk model:

```
GET /api/custom-fields/definitions/?model=product&app=catalog
```

**Respons: **
```json
[
  {
    "id": 1,
    "name": "External API ID",
    "slug": "external_api_id",
    "field_type": "text",
    "is_required": false,
    "group": { "name": "External Integrations" }
  }
]
```

### Membaca Nilai Bidang Kustom

Nilai bidang kustom termasuk dalam objek JSON `custom_fields` pada respons API model:

```json
{
  "id": 42,
  "name": "Blue Widget",
  "custom_fields": {
    "external_api_id": "API-12345",
    "is_fragile": true
  }
}
```

### Menulis Nilai Bidang Kustom

Sertakan `custom_fields` saat menciptakan atau memperbarui catatan melalui API:

```json
{
  "custom_fields": {
    "external_api_id": "API-67890",
    "warehouse_location": "WH-A3"
  }
}
```

Nilai akan divalidasi terhadap definisi bidang. Nilai yang tidak valid mengembalikan kesalahan `400` dengan detailnya.

### Mencari dengan Bidang Kustom

Bidang kustom diindeks untuk query database yang cepat. Saring catatan menggunakan filter query database:

```
GET /api/products/?custom_fields__warehouse_location=WH-A3
```

## Tampilan di Toko Online

### Untuk Pengembang Tema

Gunakan tag templat `render_custom_fields` untuk menampilkan bidang kustom di toko online:

```python
{% load custom_fields_tags %}

{# Render semua bidang yang terlihat di toko online #}
{% render_custom_fields product %}

{# Dapatkan nilai bidang tertentu #}
{% get_custom_field product "warehouse_location" as location %}
<p>Kirim dari: {{ location }}</p>
```

Hanya bidang yang memiliki **Tampilkan di toko online** diaktifkan di tingkat kelompok dan bidang yang akan ditampilkan.

## Praktik Terbaik

- **Gunakan nama yang deskriptif** — nama bidang muncul di formulir dan di toko online
- **Atur teks bantuan** — pandu pedagang untuk memasukkan apa yang harus dimasukkan di setiap bidang
- **Kelompokkan bidang terkait** — menjaga formulir tetap terorganisir dan intuitif
- **Gunakan nilai default** — atur nilai yang masuk akal untuk mengurangi masukan data
- **Pilih secara selektif visibilitas toko online** — hanya tampilkan bidang yang bermakna bagi pelanggan
- **Gunakan slug dalam integrasi** — slug adalah identifikasi stabil; nama bidang dapat berubah

## Penyelesaian Masalah

**Tab Bidang Kustom tidak muncul: **
- Periksa apakah setidaknya satu kelompok bidang aktif ada untuk model tersebut
- Pastikan kelas admin mencakup `CustomFieldsAdminMixin`
- Bersihkan cache dan segarkan halaman

**Nilai bidang tidak disimpan: **
- Pastikan bidang yang diperlukan diisi
- Periksa aturan validasi (min/max, pola regex, pilihan yang diizinkan)
- Pastikan bidang aktif dan tidak dihapus lunak

**API mengembalikan custom_fields kosong: **
- Konfirmasi model memiliki `CustomFieldsMixin`
- Periksa apakah definisi bidang ada untuk jenis konten yang benar
- Pastikan serialisator mencakup `CustomFieldsSerializerMixin`

## Topik Terkait

- [Menambahkan Produk](#)
- [Pengaturan Toko](#)