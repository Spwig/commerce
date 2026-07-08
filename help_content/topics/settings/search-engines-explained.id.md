---
title: Penjelasan Mesin Pencari
---

Mesin pencari di Spwig bukan layanan eksternal seperti Elasticsearch atau Algolia - mereka adalah konteks konfigurasi dalam sistem pencarian bawaan toko Anda. Setiap mesin mendefinisikan jenis konten apa yang dicari, apa yang harus dikecualikan, dan bagaimana hasilnya harus dirangking. Panduan ini menjelaskan apa itu mesin pencari, kapan membuat beberapa mesin, dan cara mengonfigurasinya.

Sebagian besar pedagang menggunakan satu mesin default "shop". Buat beberapa mesin hanya jika Anda membutuhkan campuran konten atau pengecualian yang berbeda untuk berbagai kasus penggunaan.

![Daftar Mesin Pencari](/static/core/admin/img/help/search-engines-explained/search-engines-list.webp)

## Apa Itu Mesin Pencari?

Mesin pencari di Spwig adalah konfigurasi bernama yang menentukan:

- **Jenis konten apa yang dicari** (produk, kategori, merek, posting blog)
- **Apa yang harus dikecualikan** (kategori atau merek tertentu yang ingin disembunyikan dari pencarian)
- **Bobot relevansi khusus** (opsional, penimbalan bobot per mesin)
- **Status aktif** (mesin dapat dinonaktifkan sementara)

Setiap mesin memiliki slug unik yang digunakan dalam panggilan API dan kode frontend untuk menentukan mesin mana yang harus menangani permintaan pencarian.

## Kapan Membuat Beberapa Mesin

Sebagian besar toko hanya membutuhkan satu mesin. Buat mesin tambahan untuk skenario berikut:

| Kasus Penggunaan | Contoh |
|------------------|--------|
| **Campuran konten berbeda** | Mesin toko hanya mencari produk; mesin blog hanya mencari posting blog |
| **Pengecualian selektif** | Mesin toko utama menyembunyikan kategori diskon; mesin diskon hanya menampilkan item diskon |
| **Pencarian khusus departemen** | Mesin elektronik mengecualikan kategori pakaian; mesin pakaian mengecualikan elektronik |
| **Pemisahan B2B vs B2C** | Mesin grosir hanya menampilkan produk dalam jumlah besar; mesin ritel menampilkan produk konsumen |

Jika Anda tidak yakin apakah membutuhkan beberapa mesin, tetap gunakan satu. Menambahkan mesin menciptakan kompleksitas tanpa manfaat kecuali Anda memiliki kasus penggunaan spesifik.

## Wizard 4 Langkah

![Langkah Wizard 1 - Informasi Dasar](/static/core/admin/img/help/search-engines-explained/wizard-step1-basic.webp)

Navigasikan ke **Search > Setup Wizard** untuk membuat mesin baru melalui proses 4 langkah terbimbing:

### Langkah 1: Informasi Dasar

**Nama Mesin** - Nama tampilan ramah (misalnya, "Pencarian Toko", "Pencarian Blog"). Hanya digunakan di antarmuka admin.

**Slug** - Identifikasi yang aman untuk URL (misalnya, "shop-search", "blog-search"). Digunakan dalam panggilan API dan kode frontend. Dihasilkan secara otomatis dari nama jika dibiarkan kosong.

**Aktif** - Apakah mesin ini tersedia untuk pencarian. Mesin tidak aktif tidak mengembalikan hasil.

### Langkah 2: Jenis Konten

Pilih jenis konten apa yang akan dicari oleh mesin ini:

- Produk (termasuk semua jenis produk: fisik, digital, langganan)
- Kategori
- Merek
- Posting Blog

**Tips**: Pilih hanya jenis konten yang relevan dengan tujuan mesin ini. Mesin yang fokus pada blog tidak perlu mengaktifkan produk.

### Langkah 3: Bobot (Opsional)

![Langkah Wizard 3 - Bobot](/static/core/admin/img/help/search-engines-explained/wizard-step3-weights.webp)

Opsional, atur ulang bobot relevansi untuk mesin ini secara spesifik. Jika dilewati, mesin akan mewarisi bobot global dari SearchSettings.

Sebagian besar mesin sebaiknya melewati langkah ini dan menggunakan bobot default global. Hanya atur ulang bobot jika mesin ini memiliki kebutuhan peringkat yang unik (misalnya, mesin blog mungkin meningkatkan weight_blog_posts menjadi 1.2).

### Langkah 4: Periksa dan Buat

Periksa konfigurasi Anda dan klik **Buat Mesin** untuk menyimpan.

## Bidang Konfigurasi Mesin

Jika Anda mengedit mesin secara langsung (melewati wizard), Anda akan melihat bidang berikut:

**Nama dan Slug** - Nama tampilan dan identifikasi URL

**Status Aktif** - Tombol untuk mengaktifkan/menonaktifkan

**Jenis Konten** - Array JSON seperti `[