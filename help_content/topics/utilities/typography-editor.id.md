---
title: Editor Tipografi
---

Editor Tipografi adalah utilitas gaya yang dapat dibagikan yang memberi Anda kendali penuh atas penampilan teks. Ia akan muncul sebagai panel mengapung setiap kali Anda mengedit properti tipografi pada elemen apa pun di Page Builder, Header/Footer Builder, atau Menu Builder.

![Editor Tipografi](/static/core/admin/img/help/typography-editor/typography-editor.webp)

## Preview Langsung

Editor menampilkan perbandingan sampingan di bagian atas panel:

| Kotak | Tujuan |
|-----|---------|
| **Saat Ini** | Menampilkan "The quick brown fox..." dalam gaya tipografi yang sudah ada |
| **Baru** | Diperbarui secara real-time saat Anda menyesuaikan pengaturan, menampilkan hasil sebelum Anda menerapkannya |

Ini memungkinkan Anda membandingkan sebelum dan sesudah tanpa melakukan perubahan apa pun.

## Tab Font

Tab Font adalah tampilan default ketika editor terbuka.

**Font Family** — Dropdown yang dapat dicari dengan lebih dari 70 font yang dikelompokkan berdasarkan kategori. Setiap font ditampilkan dalam gaya tipografi masing-masing sehingga Anda dapat melihat bagaimana penampilannya sebelum memilih. Font dimuat saat diperlukan dari Google Fonts.

**Font Size** — Input numerik dengan pemilih unit yang mendukung px, em, rem, dan %. Defaultnya adalah 16px.

**Font Weight** — Slider dari 100 (Thin) hingga 900 (Black):

| Nilai | Nama |
|-------|------|
| 100 | Thin |
| 200 | Extra Light |
| 300 | Light |
| 400 | Regular |
| 500 | Medium |
| 600 | Semi Bold |
| 700 | Bold |
| 800 | Extra Bold |
| 900 | Black |

Tidak semua font mendukung sembilan bobot tersebut. Editor menampilkan bobot yang tersedia untuk keluarga font yang dipilih.

**Font Style** — Tombol toggle untuk Normal, Italic, dan Oblique.

## Tab Spacing

Atur ulang ruang di sekitar dan antar karakter:

| Kontrol | Fungsi | Default |
|---------|-------------|---------|
| **Line Height** | Ruang vertikal antar baris teks | normal |
| **Letter Spacing** | Ruang horizontal antar karakter individu | normal |
| **Word Spacing** | Ruang horizontal antar kata | normal |
| **Text Indent** | Penjajaran baris pertama dalam sebuah paragraf | 0 |

Setiap kontrol ruang mencakup pemilih unit (px, em, rem, %).

## Tab Style

Kontrol dekorasi teks dan efek visual:

- **Text Decoration** — Tidak ada, Garis Bawah, Garis Atas, atau Garis Melintang
- **Decoration Style** — Padat, Garis Putus-putus, Titik, Ganda, atau Gelombang (berlaku saat dekorasi aktif)
- **Decoration Color** — Pemilih warna untuk garis dekorasi, defaultnya adalah warna teks
- **Text Shadow** — Efek bayangan opsional dengan kontrol offset, blur, dan warna

## Tab Transform

Ubah kapitalisasi teks tanpa mengedit konten:

| Opsi | Hasil |
|--------|--------|
| **None** | Teks muncul seperti yang ditulis |
| **Uppercase** | SEMUA HURUF DIKAPITALISASI |
| **Lowercase** | semua huruf dalam huruf kecil |
| **Capitalize** | Huruf Pertama Dari Setiap Kata Di Kapitalisasi |

Kontrol tambahan pada tab ini mencakup **Text Align** (kiri, tengah, kanan, justify), **Vertical Align**, dan **Text Direction** (LTR atau RTL).

## Font Family yang Tersedia

Editor mencakup perpustakaan terpilih dari font sistem dan Google Fonts, dikelompokkan berdasarkan kategori:

| Kategori | Font
|----------|-------
| **Sistem** | Default Sistem, Arial, Helvetica Neue, Helvetica, Segoe UI, Roboto, Ubuntu, Verdana, Tahoma, Trebuchet MS
| **Sans-Serif (Modern)** | Inter, Montserrat, Poppins, DM Sans, Space Grotesk, Plus Jakarta Sans, Outfit, Manrope, Figtree, Josefin Sans
| **Sans-Serif (Klasik)** | Open Sans, Lato, Nunito, Nunito Sans, Source Sans 3, Raleway, Rubik, Work Sans, Mulish, Cabin, Karla, Barlow, Lexend
| **Serif** | Playfair Display, Merriweather, Lora, Libre Baskerville, Cormorant Garamond, Source Serif 4, EB Garamond, Crimson Pro, Bitter, Fraunces, Spectral, Cardo, Alegreya
| **Serif (Sistem)** | Georgia, Times New Roman, Palatino, Book Antiqua, Garamond, Cambria
| **Monospace** | Source Code Pro, Fira Code, JetBrains Mono, Roboto Mono, IBM Plex Mono, Space Mono, Inconsolata, Consolas, Monaco, Menlo, Courier New, SF Mono
| **Display** | Oswald, Bebas Neue, Anton, Archivo Black, Rajdhani, Righteous, Abril Fatface, Archivo, Impact, Arial Black

Font Google dimuat secara otomatis saat dipilih. Font sistem menggunakan rantai fallback CSS yang tepat untuk rendering yang andal di berbagai platform.

## Di Mana Tampil

Editor Tipografi tersedia di mana saja yang membutuhkan penyesuaian gaya teks:

- **Page Builder** — Pilih elemen apa pun, buka tab Style, dan klik bagian Typography
- **Header/Footer Builder** — Gaya teks pada tautan navigasi, teks logo, item menu, dan konten footer
- **Menu Builder** — Kontrol tipografi untuk label menu dan item sub-menu
- **Catalog Admin** — Digunakan dalam deskripsi produk dan editor konten di mana kontrol tipografi tersedia

Editor selalu diakses melalui antarmuka yang konsisten, terlepas dari konteksnya.

## Tips

- **Pasangkan font secara sengaja** — gunakan font display atau serif untuk judul dan sans-serif yang bersih untuk teks utama. Kombinasi klasik seperti Playfair Display + Inter atau Montserrat + Merriweather bekerja dengan baik.
- **Batasi jumlah keluarga font per halaman** — dua atau tiga keluarga font per halaman biasanya cukup. Lebih dari itu dapat memperlambat waktu muat dan menciptakan kekacauan visual.
- **Gunakan unit relatif untuk teks responsif** — em dan rem berskala dengan ukuran font dasar, membuat tipografi Anda beradaptasi secara otomatis dengan berbagai ukuran layar.
- **Periksa ketersediaan berat** — jika teks terlihat sama pada 400 dan 500, font yang dipilih mungkin tidak mendukung berat tersebut. Editor menunjukkan berat mana saja yang disediakan oleh setiap font.
- **Pratinjau di semua perangkat** — teks yang terlihat bagus pada ukuran desktop mungkin terlalu kecil atau terlalu besar di perangkat mobile. Gunakan pratinjau perangkat Page Builder untuk memverifikasi.
- **Gunakan pratinjau langsung** — selalu bandingkan Current vs New dalam kotak pratinjau sebelum menerapkan untuk menghindari perubahan tak terduga.