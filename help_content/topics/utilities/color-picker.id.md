---
title: Pemilih Warna
---

Pemilih warna lanjutan memungkinkan Anda memilih warna menggunakan beberapa metode input dan preset yang sadar terhadap tema. Pemilih ini muncul di mana saja properti warna digunakan di seluruh platform — dalam pembuat halaman, pembuat header/footer, pembuat menu, dan admin katalog. Klik swatch warna atau bidang input warna untuk membuka pemilih.

![Pemilih Warna](/static/core/admin/img/help/color-picker/color-picker.webp)

## Metode Input Warna

Pemilih mendukung beberapa cara untuk mendefinisikan warna:

| Metode | Deskripsi | Contoh |
|--------|-------------|---------|
| **Hex** | Masukkan kode heksadesimal 6 digit secara langsung | `#FF5733` |
| **RGB** | Atur slider Merah, Hijau, dan Biru (masing-masing 0-255) | `rgb(255, 87, 51)` |
| **HSL** | Tetapkan Hue (0-360), Saturation (0-100%), dan Lightness (0-100%) | `hsl(14, 100%, 60%)` |
| **RGBA** | RGB dengan saluran transparansi alpha | `rgba(255, 87, 51, 0.8)` |
| **HSLA** | HSL dengan saluran transparansi alpha | `hsla(14, 100%, 60%, 0.8)` |
| **Spektrum Visual** | Klik atau drag di area spektrum warna untuk memilih secara visual | Pemilihan dengan klik dan arahkan |

Anda juga dapat mengetik nilai secara langsung ke dalam bidang teks di bagian bawah pemilih.

## Pemilih Format

Sebuah dropdown di bagian atas pemilih memungkinkan Anda beralih antara mode output **HEX**, **RGB**, **RGBA**, **HSL**, dan **HSLA**. Ketika Anda beralih format, warna saat ini secara otomatis dikonversi — tidak ada nilai yang hilang. Pilih format yang paling sesuai dengan alur kerja atau kebutuhan sistem desain Anda.

## Preset Warna

Di bawah area spektrum, baris swatch warna akses cepat menyediakan pemilihan satu klik untuk warna umum. Swatch ini **sadar terhadap tema**: mereka secara otomatis mencerminkan warna primer, sekunder, aksen, dan netral dari palet tema aktif. Hal ini memudahkan Anda untuk tetap konsisten dengan merek tanpa harus mengingat kode heksadesimal.

Untuk menerapkan preset, klik swatch. Pemilih langsung diperbarui untuk menampilkan warna yang dipilih di area spektrum dan bidang input.

## Opasitas / Alpha

Ketika menggunakan mode RGBA atau HSLA, slider **alpha horizontal** muncul di bawah spektrum. Drag untuk menetapkan transparansi dari 0% (penuh transparan) hingga 100% (penuh tidak transparan). Nilai opasitas juga dapat diedit sebagai input numerik di sebelah slider untuk kontrol yang lebih presisi.

Warna semi-transparan berguna untuk lapisan, efek hover, dan elemen desain bertingkat.

## Warna Saat Ini vs Warna Baru

Di bagian bawah pemilih, dua kotak berdampingan menampilkan warna **saat ini** yang diterapkan dan warna **baru** yang dipilih. Perbandingan ini memungkinkan Anda mengevaluasi perubahan sebelum mengonfirmasi. Klik **Terapkan** untuk menerima warna baru, atau klik di luar pemilih untuk membatalkan dan mempertahankan nilai saat ini.

## Di Mana Pemilih Ini Muncul

Pemilih warna adalah utilitas yang dibagikan yang digunakan di seluruh admin:

- **Pembuat Halaman** — Warna teks elemen, warna latar belakang, warna border, dan status hover di tab Style
- **Pembuat Header/Footer** — Warna teks widget, latar belakang, ikon, dan tautan
- **Pembuat Menu** — Warna tautan item menu dan status hover/aktif
- **Admin Katalog** — Warna badge produk dan warna aksen kategori

Setiap bidang yang menerima nilai warna membuka pemilih yang sama, sehingga pengalaman tetap konsisten di mana saja.

## Tips

- Gunakan swatch preset tema Anda untuk mempertahankan konsistensi merek di seluruh halaman dan komponen.
- Beralih ke mode HSL ketika Anda perlu membuat variasi lebih terang atau lebih gelap dari nuansa yang sama — cukup atur nilai Lightness.
- Salin kode heksadesimal dari bidang teks untuk menggunakannya kembali di bidang lain atau berbagi dengan desainer.
- Gunakan RGBA dengan opasitas yang dikurangi untuk efek overlay halus pada gambar dan bagian hero.
- Pemilih mengingat warna yang digunakan baru-baru ini selama sesi Anda, sehingga warna kustom yang sering digunakan tetap dapat diakses.
- Jika Anda menempelkan nilai warna dalam format apa pun yang didukung ke dalam bidang heksadesimal, pemilih akan mengenali dan mengkonversinya secara otomatis.
