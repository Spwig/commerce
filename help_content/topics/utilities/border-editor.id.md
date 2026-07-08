---
title: Editor Border
---

Editor Border memberikan kontrol yang presisi terhadap border elemen, termasuk gaya, warna, lebar per sisi, dan radius sudut per sudut. Ia terbuka sebagai panel mengapung dengan tampilan langsung dan dua tab untuk pengaturan dasar dan lanjutan.

![Editor Border](/static/core/admin/img/help/border-editor/border-editor.webp)

## Tampilan Langsung

Sebuah kotak pratinjau di bagian atas editor menampilkan perubahan border secara real-time. Kotak ini menampilkan kata "Preview" di dalam persegi panjang berborder yang diperbarui secara instan saat Anda menyesuaikan nilai gaya, warna, lebar, dan radius.

## Mode Dasar vs Lanjutan

Editor dibagi menjadi dua tab:

| Tab | Apa yang Tersedia |
|-----|------------------|
| **Dasar** | Gaya border, warna, lebar (dengan kontrol per sisi), dan radius border (dengan kontrol per sudut) |
| **Lanjutan** | Penyetelan radius sudut individual dan properti eksperimental Shape Sudut |

Sebagian besar pekerjaan border dilakukan sepenuhnya di tab Dasar. Tab Lanjutan berguna ketika Anda membutuhkan kontrol presisi terhadap sudut individual atau ingin bereksperimen dengan fitur CSS yang lebih baru.

## Gaya Border

Sebuah dropdown dengan sembilan opsi yang mengontrol penampilan garis border:

| Gaya | Deskripsi |
|-------|-----------|
| **Tidak Ada** | Tidak ada border (menghilangkan border yang ada) |
| **Solid** | Sebuah garis kontinu tunggal (default) |
| **Garis Putus-putus** | Serangkaian garis pendek |
| **Titik** | Serangkaian titik bulat |
| **Ganda** | Dua garis solid sejajar |
| **Groove** | Border yang terukir, efek 3D yang tampak tertekan ke permukaan |
| **Ridge** | Border yang terangkat, efek 3D (kebalikan dari groove) |
| **Inset** | Membuat elemen terlihat tertanam atau tertekan |
| **Outset** | Membuat elemen terlihat terangkat atau muncul ke luar |

Menetapkan gaya ke Tidak Ada akan menghilangkan border sepenuhnya, terlepas dari pengaturan lebar atau warna.

## Warna Border

Sebuah bidang input teks yang dipasangkan dengan tombol Pemilih Warna. Masukkan nilai heksadesimal secara langsung (misalnya `#3b82f6`) atau klik swatch warna untuk membuka Pemilih Warna lengkap dengan mode input heksadesimal, RGB, dan HSL plus area visual warna. Warna default adalah hitam (`#000000`).

## Lebar Border

Mengontrol ketebalan border dalam piksel. Tab Dasar menampilkan empat input sisi individual:

| Sisi | Input |
|------|-------|
| **Atas** | Input numerik, minimum 0 |
| **Kanan** | Input numerik, minimum 0 |
| **Bawah** | Input numerik, minimum 0 |
| **Kiri** | Input numerik, minimum 0 |

Sebuah **tombol toggle tautan** (ikon rantai) di sebelah label mengontrol apakah semua empat sisi terhubung:

- **Terhubung** (default) — mengubah nilai apa pun akan memperbarui semua empat sisi sekaligus
- **Tidak Terhubung** — setiap sisi dapat memiliki lebar berbeda, berguna untuk efek seperti border bawah saja atau border aksen kiri

## Radius Border

Mengontrol kelengkungan setiap sudut. Tab Dasar menampilkan empat input sudut:

| Sudut | Label |
|--------|-------|
| **Kiri Atas** | TL |
| **Kanan Atas** | TR |
| **Kiri Bawah** | BL |
| **Kanan Bawah** | BR |

Sebuah **tombol toggle tautan** bekerja dengan cara yang sama seperti lebar border:

- **Terhubung** (default) — semua empat sudut berbagi nilai radius yang sama
- **Tidak Terhubung** — setiap sudut dapat memiliki nilai radius berbeda

Nilai radius umum:

| Nilai | Efek |
|-------|------|
| 0px | Sudut persegi tajam |
| 4-8px | Kelengkungan halus, cocok untuk kartu dan tombol |
| 12-16px | Kelengkungan yang terlihat, tampilan modern yang lembut |
| 50% | Lingkaran penuh atau bentuk pil (tergantung dimensi elemen) |

Pemilih unit mendukung px, em, rem, dan % untuk nilai lebar dan radius.

## Bentuk Sudut (Lanjutan)

Tab Lanjutan mencakup properti eksperimental **Bentuk Sudut**. Fitur CSS ini mengontrol apakah sudut yang dibulatkan menggunakan bentuk standar yang melengkung atau bentuk "scoop" yang lebih sudut. Dukungan browser terbatas, dan editor menampilkan peringatan kompatibilitas ketika browser saat ini tidak mendukung properti ini.

## Aksi Footer

| Tombol | Aksi |
|--------|------|
| **Reset** | Mengembalikan semua nilai ke keadaan saat editor dibuka |
| **Batal** | Menutup editor tanpa menerapkan perubahan |
| **Terapkan** | Menyimpan pengaturan border dan menutup editor |

## Di Mana Tampil

Editor Border tersedia di beberapa pembangun:

- **Pembangun Halaman** — pilih elemen apa pun, buka tab Gaya, dan klik bagian Border
- **Pembangun Header/Footer** — tambahkan border ke bagian header, kontainer navigasi, dan area footer
- **Pembangun Menu** — gayakan border pada item menu dan kontainer dropdown

Editor membaca gaya border yang dihitung saat ini dari elemen hidup di canvas, sehingga selalu terbuka dengan nilai yang sudah ada yang benar.

## Tips

- **Gunakan border secara terbatas** — border tipis 1px dalam abu-abu terang menciptakan pemisah bersih antar bagian tanpa menambah bobot visual.
- **Gabungkan radius dengan bayangan** — sudut melengkung yang dipasangkan dengan bayangan kotak lembut (melalui Editor Bayangan) menghasilkan efek kartu yang rapi.
- **Coba border satu sisi** — lepaskan sisi dan atur hanya border bawah atau kiri untuk garis aksen, pemisah bagian, atau indikator sidebar.
- **Gunakan radius persentase untuk pil** — atur semua sudut ke 50% pada tombol atau badge untuk menciptakan bentuk pil yang beradaptasi dengan ukuran konten apa pun.
- **Periksa pratinjau** — kotak pratinjau langsung diperbarui secara instan, jadi eksperimen secara bebas sebelum menerapkan.
