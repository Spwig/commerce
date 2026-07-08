---
title: Keterbatasan Voucher
---

Keterbatasan voucher mengontrol siapa yang dapat menggunakan voucher, kapan, dan seberapa sering. Konfigurasikan pengaturan ini saat membuat atau mengedit voucher di **Pemasaran > Voucher**.

![Aturan Keterbatasan](/static/core/admin/img/help/voucher-restrictions/restriction-rules.webp)

## Batas Penggunaan

Tetapkan batas global dan per-pelanggan di bagian **Batas Penggunaan** dari formulir voucher.

- **Maksimal penggunaan total** — Jumlah maksimal kali voucher ini dapat digunakan oleh semua pelanggan. Biarkan kosong untuk tidak terbatas.
- **Maksimal penggunaan per pelanggan** — Berapa kali seorang pelanggan tunggal dapat menggunakan voucher ini. Tetapkan ke 1 untuk sebagian besar kampanye.

| Pola | Maksimal Total | Per Pelanggan | Kasus Penggunaan |
|------|----------------|----------------|------------------|
| Kampanye terbatas | 100 | 1 | "100 pelanggan pertama" kekurangan |
| Kode yang tidak terbatas dapat dibagikan | (kosong) | 1 | Kode pemasaran berkelanjutan |
| Kode yang dapat digunakan beberapa kali | (kosong) | (kosong) | Diskon internal/staf |
| Kode unik yang hanya bisa digunakan sekali | 1 | 1 | Kode kampanye yang dihasilkan dalam jumlah besar |

## Nilai Pesanan Minimum

Bidang **Nilai Pesanan Minimum** melindungi margin Anda dengan memerlukan total keranjang sebelum voucher berlaku. Contoh: "Potongan $10 untuk pesanan di atas $50" memastikan Anda tidak pernah mendiskon pesanan kecil hingga tidak menguntungkan.

| Diskon | Nilai Minimum yang Disarankan | Rasio |
|--------|-----------------------------|-------|
| $5 potongan | $30+ | ~6:1 |
| $10 potongan | $50+ | ~5:1 |
| $20 potongan | $100+ | ~5:1 |
| 15% potongan | $40+ | Bergantung pada katalog |

## Batas Diskon (Jumlah Diskon Maksimal)

Bidang **Jumlah Diskon Maksimal** di **Konfigurasi Diskon** membatasi seberapa besar voucher persentase dapat mengurangi. Ini hanya berlaku untuk voucher tipe persentase dan mencegah diskon yang berlebihan pada keranjang bernilai tinggi.

Contoh: "Potongan 20%, maksimal $50 diskon"
- Keranjang $200 = potongan $40 (20%)
- Keranjang $300 = potongan $50 (dibatasi)
- Keranjang $1.000 = potongan $50 (dibatasi)

Tambahkan batas diskon pada setiap voucher persentase yang Anda bagikan secara publik.

## Aturan Kombinasi

Bidang **Keterbatasan & Aturan** (klik untuk memperluas) berisi kotak centang yang mengontrol cara voucher berinteraksi dengan diskon lainnya.

| Pengaturan | Apa yang Dilakukan | Kapan Harus Diaktifkan |
|-----------|--------------------|--------------------------|
| **Eksklusif produk diskon** | Voucher melewatkan produk yang sudah ada diskon | Sebagian besar kampanye — melindungi margin diskon |
| **Tidak dapat dikombinasikan dengan voucher lain** | Hanya satu voucher per pesanan | Default untuk sebagian besar voucher |
| **Tidak dapat dikombinasikan dengan produk diskon** | Memblokir voucher jika keranjang memiliki SEMUA produk diskon | Kampanye ketat di mana voucher menggantikan harga diskon |
| **Hanya untuk pelanggan baru** | Hanya pelanggan dengan pesanan sebelumnya nol | Kampanye selamat datang/akuisisi |

## Keterbatasan Pelanggan

Untuk penargetan sederhana, centang **Hanya untuk pelanggan baru** di bidang **Keterbatasan & Aturan**.

Untuk penargetan lanjutan, gunakan tabel **Keterbatasan Voucher** di bagian bawah formulir. Klik **+ Tambahkan keterbatasan voucher lain** untuk menambahkan baris. Setiap keterbatasan memiliki tiga bidang:

- **Jenis** — Kategori keterbatasan (dropdown)
- **Nilai** — Nilai yang cocok (dipisahkan dengan koma atau JSON)
- **Inklusif** — Centang = pelanggan harus cocok; tidak dicentang = pelanggan harus TIDAK cocok

| Jenis | Nilai | Inklusif | Efek |
|------|-------|-----------|--------|
| user_email_domain | @company.com | Ya | Hanya karyawan perusahaan yang dapat menggunakan |
| shipping_country | US,CA | Ya | Hanya pelanggan AS dan Kanada |
| shipping_country | RU | Tidak | Semua orang KECUALI Rusia |
| day_of_week | monday,tuesday | Ya | Hanya valid pada Senin dan Selasa |
| payment_method | stripe | Ya | Hanya untuk pembayaran Stripe |

Gabungkan beberapa baris untuk keterbatasan bertingkat. Semua keterbatasan inklusif harus cocok, dan tidak ada keterbatasan eksklusif yang cocok, agar voucher berlaku.

## Strategi Kadaluarsa

Kontrol kapan voucher kadaluarsa menggunakan bidang tanggal dan validitas.

- **Tanggal akhir** — Tanggal batas keras (misalnya, 31 Desember 2026).

Voucher berhenti berfungsi pada tengah malam.
- **Hari valid** — Validitas yang berjalan dari tanggal pembuatan atau penggunaan pertama voucher.

Mengatasi tanggal akhir saat diatur.


Berguna untuk kode selamat datang: "valid selama 30 hari setelah Anda menerimanya."