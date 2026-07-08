---
title: Contoh Promosi
---

Panduan ini menunjukkan contoh konkret cara mengonfigurasi berbagai jenis promosi. Setiap contoh mencakup nilai bidang yang tepat untuk dimasukkan dalam wizard promosi sehingga Anda dapat mengikuti atau menyesuaikannya untuk toko Anda.

![Promotion Card](/static/core/admin/img/help/promotion-examples/promotion-card.webp)

## Contoh: Potongan Persentase pada Kategori

**Skenario:** Potongan 30% untuk semua sepatu dalam penjualan musim dingin.

Navigasikan ke **Marketing > Sales & Promotions** dan klik **+ Create Promotion**. Masukkan nilai berikut pada setiap langkah wizard:

| Langkah | Bidang | Nilai |
|---------|-------|-------|
| Basics | Nama | Winter Clearance — 30% Off Shoes |
| Basics | Deskripsi | Penjualan akhir musim untuk semua produk sepatu |
| Basics | Aktif | Dicentang |
| Diskon | Jenis | Percentage Off |
| Diskon | Nilai | 30 |
| Jadwal | Tanggal Mulai | Jan 15, 2026 |
| Jadwal | Tanggal Berakhir | Feb 28, 2026 |
| Produk | Diterapkan ke | Kategori |
| Produk | Terpilih | Sepatu, Boot, Sandal |

Ini menciptakan penjualan terbatas waktu yang secara otomatis memberikan diskon setiap produk dalam kategori yang dipilih. Sepatu boot seharga $120 menjadi $84, dan pasangan sandal seharga $60 menjadi $42.

## Contoh: Potongan Tetap pada Koleksi

**Skenario:** Potongan $15 untuk item dalam koleksi Summer Essentials.

| Langkah | Bidang | Nilai |
|---------|-------|-------|
| Basics | Nama | Summer Essentials — $15 Off |
| Basics | Aktif | Dicentang |
| Diskon | Jenis | Amount Off |
| Diskon | Nilai | 15.00 |
| Jadwal | Tanggal Mulai | Jun 1, 2026 |
| Jadwal | Tanggal Berakhir | (kosong — tidak ada tanggal kedaluwarsa) |
| Produk | Diterapkan ke | Koleksi |
| Produk | Terpilih | Summer Essentials |

> **Catatan:** Potongan $15 berlaku untuk setiap produk yang memenuhi syarat secara individual. Produk seharga $50 menjadi $35, produk seharga $30 menjadi $15. Meninggalkan Tanggal Berakhir kosong berarti promosi berjalan tanpa batas waktu hingga Anda menonaktifkannya secara manual.

## Contoh: Harga Jual Tetap untuk Penjualan Akhir

**Skenario:** Tetapkan semua item penjualan akhir menjadi $9.99.

| Langkah | Bidang | Nilai |
|---------|-------|-------|
| Basics | Nama | Final Clearance — Everything $9.99 |
| Basics | Aktif | Dicentang |
| Diskon | Jenis | Fixed Sale Price |
| Diskon | Nilai | 9.99 |
| Jadwal | Tanggal Mulai | (hari ini) |
| Produk | Diterapkan ke | Koleksi |
| Produk | Terpilih | Final Clearance |

> **Catatan:** Harga Jual Tetap menetapkan harga jual yang tepat, terlepas dari harga asli. Item seharga $75 dan item seharga $25 keduanya menjadi $9.99. Gunakan ini untuk rak penjualan akhir atau harga seragam di mana Anda ingin semua item pada titik harga yang sama.

![Category Promotion](/static/core/admin/img/help/promotion-examples/category-promotion.webp)

## Memilih Jenis Diskon yang Tepat

| Jenis | Cara Kerjanya | Terbaik Untuk | Contoh |
|-------|--------------|--------------|--------|
| **Potongan Persentase** | Mengurangi harga dengan persentase | Penjualan luas di mana produk memiliki harga yang bervariasi | Potongan 20% — $100 menjadi $80, $50 menjadi $40 |
| **Potongan Tetap** | Mengurangi jumlah dolar tetap | Promosi dengan pesan penghematan dolar tertentu | $15 potongan — $100 menjadi $85, $50 menjadi $35 |
| **Harga Jual Tetap** | Menetapkan harga jual yang tepat | Penjualan akhir, harga seragam, "semua barang di $X" | $9.99 — semua barang menjadi $9.99 tanpa memandang harga asli |

## Memilih Target yang Tepat

| Target | Cara Kerjanya | Terbaik Untuk |
|--------|--------------|--------------|
| **Semua Produk** | Berlaku untuk semua produk di toko Anda | Penjualan sitewide, acara toko-wide |
| **Kategori** | Berlaku untuk semua produk dalam kategori yang dipilih | Penjualan departemen, penjualan musiman berdasarkan jenis |
| **Merek** | Berlaku untuk semua produk dari merek yang dipilih | Kemitraan merek, acara khusus merek |
| **Koleksi** | Berlaku untuk semua produk dalam koleksi yang dipilih | Promosi yang disusun, penjualan berdasarkan tema |
| **Produk** | Berlaku untuk produk yang dipilih secara individual | Penawaran yang dipilih secara manual, pemilihan terbatas |

## Pola Jadwal

Tiga pola umum untuk mengatur jadwal promosi:

| Pola | Tanggal Mulai | Tanggal Berakhir | Kasus Penggunaan |
|------|---------------|------------------|------------------|
| **Segera, terus-menerus** | Hari ini | (kosong) | Pengurangan harga permanen, penjualan jangka panjang |
| **Rentang tanggal** | Tanggal masa depan | Tanggal masa depan | Acara musiman, penjualan hari raya |
| **Mulai masa depan, tanpa akhir** | Tanggal masa depan | (kosong) | Harga permanen baru yang dimulai pada tanggal tertentu |

Menetapkan Tanggal Mulai di masa depan menciptakan promosi yang dijadwalkan. Ini akan muncul di tab **Scheduled** pada dashboard promosi dan secara otomatis diaktifkan ketika tanggal tiba. Meninggalkan Tanggal Berakhir kosong berarti promosi tetap aktif hingga Anda menonaktifkannya secara manual.

## Tips

- **Gunakan nama yang deskriptif** — Sertakan nilai diskon dan target dalam nama (misalnya, "Summer 20% Off Shoes") sehingga Anda dapat dengan cepat mengidentifikasi promosi di dashboard.
- **Periksa jumlah produk yang terdampak** — Langkah Tinjau menunjukkan berapa banyak produk yang akan didiskon. Jika jumlahnya tampak salah, kembali dan periksa target Anda.
- **Mulai dengan kecil** — Jika Anda ragu tentang diskon, mulailah dengan persentase yang lebih kecil dan tingkatkan jika diperlukan.
- **Gunakan Potongan Tetap untuk pemasaran** — "$15 off" adalah penghematan konkret yang mudah dikomunikasikan dalam iklan dan kampanye email.
- **Gunakan Potongan Persentase untuk keadilan** — Diskon persentase berubah sesuai harga, memberikan penghematan proporsional di berbagai titik harga.

Remember: Preserve all markdown formatting, image paths, code blocks, and technical terms exactly as shown in the preservation rules.