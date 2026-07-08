---
title: Gradient Creator
---

Gradient Creator memungkinkan Anda membuat transisi warna yang halus untuk latar belakang elemen. Ia diakses melalui tab Gradient di Background Editor dan muncul sebagai panel mengapung dengan bar gradient visual, kontrol titik warna, dan opsi preset.

![Gradient Creator](/static/core/admin/img/help/gradient-creator/gradient-creator.webp)

## Mengakses Gradient Creator

1. Pilih elemen di Page Builder atau Header/Footer Builder
2. Buka tab **Style** di panel properti
3. Klik bagian **Background** untuk membuka Background Editor
4. Beralih ke tab **Gradient**
5. Panel Gradient Creator terbuka dengan pratinjau langsung dan kontrol pengeditan

## Pratinjau Langsung

Bagian atas panel menampilkan perbandingan sampingan:

| Box | Purpose |
|-----|---------|
| **Current** | Gradient yang ada (atau transparan jika tidak ada yang diatur) |
| **New** | Perubahan yang terjadi secara real-time saat Anda membuat perubahan |

Panah antara dua kotak menunjukkan arah perubahan.

## Jenis Gradient

Tiga jenis gradient tersedia, yang dapat dipilih melalui tab di bagian atas editor:

| Type | Description | Controls |
|------|-------------|----------|
| **Linear** | Transisi warna sepanjang garis lurus | Slider sudut (0-360 derajat) dengan tombol arah preset (ke atas, diagonal, ke kanan, ke bawah, dll.) |
| **Radial** | Transisi warna yang menyebar dari titik pusat | Pemilih bentuk (lingkaran atau elips) dan pemilih posisi (pusat, atas, bawah, sudut-sudut) |
| **Conic** | Transisi warna yang berputar di sekitar titik pusat | Slider sudut awal (0-360 derajat) dan pemilih posisi |

### Kontrol Arah Linear

Untuk gradient linear, Anda dapat mengatur sudut dengan tiga cara:
- **Slider sudut** — drag dari 0 hingga 360 derajat
- **Input sudut** — ketik nilai derajat yang tepat
- **Tombol preset** — klik ikon panah untuk arah umum (ke atas, ke kanan atas, ke kanan, ke kanan bawah, ke bawah, ke kiri bawah, ke kiri, ke kiri atas)

## Titik Warna

Bar gradient menampilkan titik warna saat ini Anda sebagai penanda yang dapat digeser. Setiap titik mendefinisikan warna pada posisi tertentu sepanjang gradient.

**Menambahkan titik** — Klik tombol **+** di bagian Color Stops untuk menambahkan titik baru. Tidak ada batas keras pada jumlah titik.

**Mengedit titik** — Setiap titik dalam daftar menampilkan:
- Swatch warna yang membuka Color Picker saat diklik
- Nilai posisi (0% hingga 100%) yang dapat diketik atau diatur
- Kontrol opasitas (0 hingga 1)
- Tombol hapus untuk menghapus titik

**Mengurutkan ulang** — Drag titik sepanjang bar gradient untuk mengatur ulang secara visual.

## Preset Gradient

Enam preset bawaan tersedia sebagai titik awal cepat. Klik preset apa pun untuk menerapkannya secara instan:

| Preset | Colors | Angle |
|--------|--------|-------|
| **Ocean** | Biru muda ke biru | 120 derajat |
| **Sunset** | Oranye hangat ke merah muda koral (3 titik) | 45 derajat |
| **Forest** | Indigo ke hijau emerald | 135 derajat |
| **Berry** | Merah muda ke biru ungu | 90 derajat |
| **Flame** | Merah ke kuning emas | 45 derajat |
| **Night** | Batu gelap ke biru laut | 180 derajat |

Preset adalah titik awal. Setelah menerapkan satu, Anda dapat memodifikasi warna, menambah atau menghapus titik, dan mengubah sudut untuk membuat variasi Anda sendiri.

## Aksi Footer

| Tombol | Aksi |
|--------|--------|
| **Clear** | Menghapus gradient secara keseluruhan, mengembalikan ke transparan |
| **Apply** | Menyimpan gradient dan menutup editor |

Menutup editor tanpa mengklik Apply akan mengabaikan perubahan Anda.

## Di Mana Ia Muncul

Gradient Creator digunakan di:

- **Page Builder** — melalui tab Gradient di Background Editor pada elemen apa pun
- **Header/Footer Builder** — untuk latar belakang gradient pada bagian header, bar navigasi, dan area footer

Ia bekerja bersama dengan Background Editor, yang juga menawarkan opsi latar belakang berwarna solid, gambar, dan video.

## Tips

- **Mulai dengan preset** — terapkan preset yang dekat dengan apa yang Anda inginkan, lalu sesuaikan warna dan sudut daripada membangun dari awal.
- **Gunakan dua atau tiga titik** — gradient sederhana dengan dua titik terlihat bersih dan profesional. Lebih banyak titik berguna untuk efek kompleks tetapi dapat dengan cepat menjadi membingungkan.
- **Sesuaikan dengan warna merek Anda** — gunakan Color Picker untuk memasukkan nilai heksa eksak dari palet warna merek Anda untuk gradient yang konsisten dan sesuai dengan merek.
- **Uji dengan konten** — gradient yang terlihat menarik sendirian mungkin mengurangi keterbacaan teks. Selalu periksa bahwa teks di atas latar belakang gradient memiliki kontras yang cukup.
- **Coba radial untuk efek sorotan** — gradient radial bekerja baik untuk menarik perhatian ke area pusat, seperti titik fokus bagian hero.