---
title: Atribut Produk
---

Atribut produk mendefinisikan dimensi di mana produk dapat bervariasi — contohnya, Ukuran, Warna, atau Bahan. Setelah Anda membuat atribut dan nilai-nilai yang mungkin, Anda dapat menetapkannya ke produk variabel apa pun dan Spwig akan menghasilkan pemilih variasi yang digunakan pelanggan saat checkout.

Navigasikan ke **Katalog > Atribut Produk** untuk mengelola atribut dan nilainya.

## Bagaimana atribut bekerja

Atribut dapat digunakan ulang di seluruh katalog Anda. Anda membuatnya sekali dan menetapkannya ke sebanyak produk yang diperlukan. Setiap atribut memiliki:

- **Nama** yang mengidentifikasikannya (misalnya, "Ukuran")
- **Tipe tampilan** yang mengontrol cara pemilih muncul di halaman produk
- Satu atau lebih **nilai** yang merepresentasikan opsi yang tersedia (misalnya, "Kecil", "Sedang", "Besar")

Ketika Anda menetapkan atribut ke produk, Anda juga menentukan nilai-nilai mana yang tersedia untuk produk tersebut. Ini berarti atribut "Ukuran" mungkin memiliki nilai dari S hingga 3XL, tetapi kemeja tertentu mungkin hanya menawarkan S, M, dan L.

## Jenis tampilan atribut

Bidang **Tipe** pada atribut mengontrol cara widget pemilihan muncul di halaman produk toko Anda:

| Tipe | Tampilan | Terbaik untuk |
|---|---|---|
| **Dropdown Select** | Menu dropdown yang dibuka oleh pelanggan untuk memilih nilai | Atribut dengan banyak nilai (misalnya, rentang ukuran dengan 10+ ukuran) |
| **Color Swatch** | Lingkaran atau persegi berwarna yang diklik oleh pelanggan | Atribut warna di mana identifikasi visual membantu |
| **Button Group** | Tombol berbentuk pil yang ditampilkan secara inline | Atribut dengan jumlah nilai kecil (misalnya, S, M, L, XL) |
| **Radio Buttons** | Daftar tombol radio tradisional | Atribut apa pun di mana Anda ingin tata letak daftar yang jelas dan dapat diakses |

Pilih jenis tampilan yang sesuai dengan cara pelanggan memikirkan atribut tersebut. Untuk warna, swatch hampir selalu lebih baik daripada dropdown. Untuk ukuran, grup tombol bekerja dengan baik ketika ada kurang dari 8 opsi.

## Membuat atribut

1. Navigasikan ke **Katalog > Atribut Produk**
2. Klik **+ Tambah Atribut Produk**
3. Masukkan **Nama** (misalnya, `Ukuran`, `Warna`, `Bahan`)
4. **Slug** diisi secara otomatis — Anda dapat membiarkannya seperti itu
5. Pilih **Tipe** (Dropdown, Color Swatch, Button Group, atau Radio Buttons)
6. Centang **Wajib Diisi** jika pelanggan harus memilih atribut ini sebelum mereka dapat menambahkan produk ke keranjang mereka — ini cocok untuk sebagian besar atribut ukuran dan warna
7. Tetapkan **Urutan Penyortiran** — atribut dengan angka lebih rendah muncul pertama di pemilih variasi di halaman produk
8. Tambahkan nilai atribut secara langsung di bagian **Nilai** (lihat di bawah)
9. Klik **Simpan**

## Menambahkan nilai atribut

Nilai atribut adalah opsi individu dalam atribut. Anda dapat menambahkannya secara langsung saat membuat atau mengedit atribut, menggunakan formulir nilai inline di bagian bawah halaman detail atribut.

Untuk setiap nilai:

- **Nilai** — label tampilan (misalnya, `Kecil`, `Merah`, `Katun`)
- **Slug** — diisi secara otomatis dari nilai; digunakan dalam URL dan identifikasi variasi
- **Hex Warna** — hanya relevan untuk atribut tipe **Color Swatch**. Masukkan kode warna hex (misalnya, `#FF0000` untuk merah) sehingga swatch menampilkan warna yang benar.
- **Urutan Penyortiran** — mengontrol urutan nilai muncul di pemilih. Tetapkan angka yang lebih rendah untuk nilai yang ingin muncul lebih awal.

### Mengurutkan nilai secara logis

Untuk atribut ukuran, atur urutan penyortiran sehingga ukuran berjalan dari kecil ke besar:

| Nilai | Urutan Penyortiran |
|---|---|
| XS | 1 |
| S | 2 |
| M | 3 |
| L | 4 |
| XL | 5 |
| 2XL | 6 |

Untuk atribut warna, Anda mungkin mengurutkan secara alfabetis atau mengelompokkan warna yang mirip — apa pun yang paling masuk akal untuk pelanggan Anda.

## Mengelola nilai atribut secara terpisah

Anda juga dapat mengelola nilai atribut secara terpisah di **Katalog > Nilai Atribut**. Daftar ini berguna ketika Anda perlu menemukan atau memperbarui nilai tertentu di seluruh katalog tanpa membuka setiap atribut secara individual. Daftar ini dapat difilter berdasarkan nama atribut.

## Menetapkan atribut ke produk

Atribut ditetapkan pada tingkat produk, bukan secara global.

Untuk menambahkan atribut ke produk:

1. Navigasikan ke **Katalog > Produk** dan buka produk variabel
2. Di tab **Variasi**, temukan bagian **Atribut**
3. Pilih atribut yang ingin Anda tambahkan
4. Pilih nilai atribut mana yang tersedia untuk produk ini
5. Simpan produk — Spwig akan menghasilkan kombinasi variasi yang sesuai

Untuk panduan terperinci tentang pengaturan variasi produk, lihat topik bantuan **Product Variants**.

## Contoh Praktis

### Contoh: Atribut ukuran pakaian

| Field | Value |
|---|---|
| Name | Size |
| Type | Button Group |
| Is Required | Yes |
| Sort Order | 1 |
| Values | XS (1), S (2), M (3), L (4), XL (5), 2XL (6) |

### Contoh: Atribut swatch warna

| Field | Value |
|---|---|
| Name | Colour |
| Type | Color Swatch |
| Is Required | Yes |
| Sort Order | 2 |
| Values | Black (#000000), White (#FFFFFF), Navy (#001F5B), Red (#CC0000) |

### Contoh: Atribut bahan

| Field | Value |
|---|---|
| Name | Material |
| Type | Dropdown Select |
| Is Required | No |
| Sort Order | 3 |
| Values | 100% Cotton, Cotton/Polyester Blend, Merino Wool, Linen |

## Tips

- Buat atribut yang mewakili keputusan pembelian nyata yang dibuat pelanggan — jika pelanggan tidak perlu memilihnya, mungkin tidak perlu menjadi atribut
- Gunakan penamaan yang konsisten di seluruh katalog Anda: jika beberapa produk menggunakan "Colour" dan yang lain menggunakan "Color", pelanggan dan tim Anda akan merasa bingung dengan ketidaksesuaian tersebut
- Urutan pengurutan pada atribut dan nilai penting — letakkan atribut yang paling penting di depan (biasanya Size atau Colour) dan urutkan nilai dalam urutan logis
- Jenis Color Swatch memerlukan kode heksa yang akurat; uji warna tersebut di picker warna browser sebelum menyimpan untuk memastikan swatch sesuai dengan warna produk yang sebenarnya
- Jika Anda perlu mengganti nama atribut (misalnya, dari "Color" ke "Colour"), perbarui bidang **Name** daripada membuat atribut baru — mengganti nama tidak memengaruhi penugasan produk yang sudah ada