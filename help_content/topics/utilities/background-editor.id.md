---
title: Editor Latar Belakang
---

Editor latar belakang memberi Anda kendali penuh terhadap latar belakang elemen dengan empat jenis: warna padat, gradien, gambar, dan video. Ia juga mendukung status Normal dan Hover yang terpisah sehingga Anda dapat membuat efek visual interaktif. Buka **tab Style** dari elemen apa pun dan cari bagian **Latar Belakang** untuk mengakses editor.

![Editor Latar Belakang](/static/core/admin/img/help/background-editor/background-editor.webp)

## Status Normal dan Hover

Di bagian atas editor latar belakang, tombol toggle berpindah antara status **Normal** dan **Hover**. Setiap status memiliki konfigurasi latar belakang yang independen:

- **Normal** — Latar belakang default yang ditampilkan saat halaman dimuat
- **Hover** — Latar belakang yang diterapkan saat pengunjung menggerakkan kursor mereka di atas elemen

Dua blok pratinjau kecil di samping toggle menampilkan latar belakang Normal dan Hover secara berdampingan, sehingga Anda dapat melihat kontrasnya secara sekilas. Konfigurasikan status Normal terlebih dahulu, lalu beralih ke Hover untuk menambahkan efek interaktif jika diinginkan.

## Jenis Latar Belakang

Pilih jenis latar belakang dari baris ikon di bagian atas panel editor:

| Jenis | Deskripsi |
|------|-------------|
| **Warna** | Isian padat menggunakan satu nilai warna. Cepat diterapkan dan ringan. |
| **Gradien** | Campuran halus antara dua atau lebih warna, baik linear maupun radial. Termasuk preset bawaan seperti Ocean, Sunset, Forest, dan Berry. Untuk pengeditan gradien lanjutan, lihat topik [Gradient Creator](gradient-creator). |
| **Gambar** | Gambar yang diunggah atau satu yang dipilih dari perpustakaan media. Mendukung kontrol posisi, ukuran, dan pengulangan. |
| **Video** | URL video latar belakang dengan gambar poster opsional yang ditampilkan saat video dimuat atau di perangkat mobile. |

Hanya satu jenis yang dapat aktif sekaligus per status. Beralih jenis tidak menghapus konfigurasi sebelumnya — Anda dapat beralih kembali dan pengaturan Anda akan tetap disimpan.

## Latar Belakang Warna

Ketika Warna dipilih:

- **Input Hex** — Ketikkan kode hex secara langsung (misalnya, `#1A1A2E`)
- **Swatch Warna** — Klik swatch preset untuk pemilihan cepat. Swatch ini sadar tema dan mencerminkan palet tema aktif Anda.
- **Tombol Edit** — Membuka pemilih warna lengkap dengan spektrum, slider, dan opsi format (lihat topik [Color Picker](color-picker))

Latar belakang warna ditampilkan secara instan dan tidak memiliki dampak kinerja, membuatnya ideal untuk bagian, kartu, dan kontainer.

## Latar Belakang Gradien

Ketika Gradien dipilih:

- **Gradien Preset** — Pilih dari gradien bawaan: Ocean, Sunset, Forest, Berry, dan lainnya
- **Gradien Kustom** — Klik **Edit** untuk membuka pembuat gradien di mana Anda dapat mengatur arah, tipe (linear atau radial), dan titik warna
- **Slider Sudut** — Sesuaikan arah gradien untuk gradien linear (0-360 derajat)

Gradien menambah kedalaman visual tanpa memerlukan aset gambar dan menyesuaikan sempurna dengan ukuran layar apa pun.

## Latar Belakang Gambar

Ketika Gambar dipilih:

- **Unggah atau Perpustakaan Media** — Klik tempat penampung gambar untuk mengunggah gambar baru atau memilih satu dari perpustakaan media Anda
- **Ukuran** — Pilih **Cover** (mengisi elemen, mungkin memotong), **Contain** (cocok di dalam elemen), atau ukuran kustom
- **Posisi** — Tetapkan titik fokus menggunakan grid 9 titik (kiri atas, tengah, kanan bawah, dll.) atau masukkan persentase X/Y kustom
- **Ulang** — Nyalakan atau matikan pengulangan. Berguna untuk pola tiling
- **Overlay** — Tambahkan lapisan warna di atas gambar dengan opasitas yang dapat disesuaikan, berguna untuk memastikan keterbacaan teks

Selalu optimalkan gambar sebelum mengunggah. Gambar besar yang tidak dikompresi memperlambat waktu muat halaman.

## Latar Belakang Video

Ketika Video dipilih:

- **URL Video** — Masukkan URL langsung ke file video MP4 atau WebM
- **Gambar Poster** — Unggah gambar cadangan yang ditampilkan saat video dimuat dan di perangkat yang tidak memutar video secara otomatis
- **Otomatis / Loop / Diamankan** — Latar belakang video berjalan otomatis, berulang, dan diamankan secara default untuk mematuhi kebijakan browser

Jaga video latar belakang tetap pendek (10-30 detik), dikompresi, dan visual yang halus.


Mereka harus meningkatkan bagian tersebut tanpa mengganggu konten.

## Di Mana Ia Muncul

Editor latar belakang tersedia untuk setiap elemen yang mendukung latar belakang:

- **Page Builder** — Bagian, kontainer, kolom, dan elemen individu semuanya memiliki bagian Latar Belakang di tab Style
- **Header/Footer Builder** — Latar belakang baris dan latar belakang widget individu
- **Menu Builder** — Latar belakang kontainer menu dan panel dropdown

Antarmuka editor yang sama digunakan di mana saja, sehingga alur kerja Anda tetap konsisten di seluruh pembangun.

## Tips

- Gunakan lapisan warna semi-transparan pada latar belakang gambar untuk memastikan teks tetap terbaca terlepas dari konten gambar.
- Preset gradien adalah cara cepat untuk menambahkan minat visual — terapkan satu, lalu sesuaikan sudut atau warna untuk cocok dengan merek Anda.
- Tetapkan latar belakang Normal dan Hover pada kartu interaktif untuk memberikan umpan balik visual yang jelas kepada pengunjung saat mereka menjelajahi konten Anda.
- Untuk latar belakang gambar, selalu tetapkan titik fokus agar bagian paling penting dari gambar tetap terlihat pada semua ukuran layar.
- Pilih latar belakang warna atau gradien daripada gambar untuk bagian di mana kecepatan muat kritis, seperti konten di atas lipatan.
- Uji latar belakang video di perangkat mobile — sebagian besar browser mobile akan menampilkan gambar poster daripada memainkan video.