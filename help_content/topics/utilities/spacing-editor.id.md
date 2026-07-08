---
title: Editor Spasi
---

Editor spasi visual memungkinkan Anda mengonfigurasi margin dan padding menggunakan diagram model kotak yang intuitif. Kontrol spasi yang presisi memastikan tata letak yang konsisten dan pengalaman membaca yang nyaman di seluruh toko online Anda. Buka **tab Style** dari elemen apa pun dan cari bagian **Spasi** untuk mengakses editor.

![Editor Spasi](/static/core/admin/img/help/spacing-editor/spacing-editor.webp)

## Diagram Model Kotak

Editor menampilkan diagram model kotak visual dengan tiga lapisan bersarang:

- **Margin** (lingkaran luar, biasanya ditampilkan dalam warna oranye) — Ruang di luar batas elemen, memisahkan elemen tersebut dari elemen tetangganya
- **Padding** (lingkaran dalam, biasanya ditampilkan dalam warna hijau) — Ruang antara batas elemen dan kontennya
- **Content** (area tengah) — Konten aktual elemen, seperti teks atau gambar

Setiap sisi diagram (atas, kanan, bawah, kiri) memiliki pegangan yang dapat digeser dan input numerik. Geser pegangan ke luar untuk meningkatkan nilai, atau ke dalam untuk menurunkannya. Anda juga dapat mengklik langsung pada nilai sisi untuk mengetikkan angka yang tepat.

## Tab Margin dan Padding

Dua tab di bagian atas editor beralih antara tampilan **Margin** dan **Padding**. Ketika Margin dipilih, lingkaran luar ditekankan dan dapat diedit. Ketika Padding dipilih, lingkaran dalam ditekankan dan dapat diedit. Lingkaran yang tidak aktif tetap terlihat sebagai referensi tetapi redup.

Kedua tab berbagi kontrol dan opsi unit yang sama, sehingga alur kerja identik untuk konfigurasi margin dan padding.

## Kontrol Per Sisi

Setiap sisi memiliki input nilai independen dan pemilih unit:

| Sisi | Deskripsi |
|------|-------------|
| **Atas** | Ruang di atas elemen (margin) atau di atas konten (padding) |
| **Kanan** | Ruang di sebelah kanan elemen atau konten |
| **Bawah** | Ruang di bawah elemen atau konten |
| **Kiri** | Ruang di sebelah kiri elemen atau konten |

Klik pada nilai sisi mana pun di diagram untuk memilihnya, lalu ketikkan angka atau gunakan tombol panah atas/bawah untuk meningkatkan nilai sebesar 1. Tahan tombol Shift saat menekan tombol panah untuk meningkatkan nilai sebesar 10.

## Unit

Pemilih unit di sebelah setiap input nilai memungkinkan Anda memilih satuan pengukuran:

| Unit | Deskripsi |
|------|-------------|
| **px** | Piksel. Ukuran tetap, konsisten di semua perangkat. Terbaik untuk nilai spasi presisi dan kecil. |
| **em** | Relatif terhadap ukuran font elemen. Membesar saat perubahan tata letak. |
| **rem** | Relatif terhadap ukuran font akar. Memberikan skala konsisten di seluruh halaman. |
| **%** | Persentase dari lebar elemen induk. Berguna untuk tata letak responsif yang cair. |
| **auto** | Memungkinkan browser menghitung nilai secara otomatis. Umum digunakan untuk pusat horizontal dengan margin kiri/kanan. |

Pilih unit yang sesuai dengan niat Anda — gunakan `px` untuk celah tetap, `rem` untuk spasi yang dapat disesuaikan yang menghormati token tata letak tema, dan `%` untuk tata letak yang harus beradaptasi dengan lebar kontainer.

## Menghubungkan Sisi

Ikon **hubungkan** di tengah diagram memicu mode terhubung:

- **Terhubung** (ikon rantai terhubung) — Mengubah nilai sisi mana pun akan memperbarui semua empat sisi menjadi nilai yang sama. Berguna untuk spasi yang seragam.
- **Tidak terhubung** (ikon rantai terputus) — Setiap sisi dikontrol secara independen. Gunakan ini ketika Anda membutuhkan nilai berbeda untuk atas/bawah dan kiri/kanan.

Klik ikon hubungkan untuk beralih antar mode. Ketika Anda beralih dari tidak terhubung ke terhubung, semua empat sisi diatur ke nilai sisi yang paling baru diedit.

## Preset Cepat

Baris tombol preset di bawah diagram menyediakan konfigurasi spasi satu klik:

| Preset | Nilai |
|--------|--------|
| **Tidak ada** | 0 di semua sisi |
| **Kecil** | Spasi kompak yang cocok untuk tata letak rapat dan elemen inline |
| **Sedang** | Spasi seimbang untuk penggunaan umum pada kartu dan bagian |
| **Besar** | Spasi luas untuk area hero dan bagian dengan penekanan tinggi |
| **XL** | Spasi ekstra lebar untuk banner lebar penuh dan bagian tingkat atas halaman |

Preset berlaku untuk tab aktif saat ini (Margin atau Padding) dan mengatur semua empat sisi sekaligus. Setelah menerapkan preset, Anda dapat menyesuaikan sisi individu sesuai kebutuhan.

## Di Mana Terdapat

Editor spasi tersedia untuk setiap elemen yang mendukung spasi tata letak:

- **Pembangun Halaman** — Tab Style, bagian Spasi pada bagian, kontainer, kolom, dan elemen individu
- **Pembangun Header/Footer** — Kontrol spasi baris dan widget untuk celah vertikal dan horizontal
- **Pembangun Menu** — Pengaturan padding item menu dan margin kontainer

Antarmuka editor yang sama digunakan di semua lokasi, memastikan pengalaman yang konsisten di seluruh pembangun.

## Tips

- Gunakan nilai spasi yang konsisten di seluruh halaman Anda — pilih 2-3 ukuran standar dan tetap gunakan untuk tata letak yang bersih dan profesional.
- Atur margin ke **auto** pada kiri dan kanan untuk memusatkan elemen lebar tetap secara horizontal di dalam induknya.
- Pilih unit `rem` untuk spasi jika tema Anda menggunakan tata letak responsif, sehingga spasi berskala proporsional dengan ukuran teks.
- Gunakan mode terhubung untuk mengatur padding seragam dengan cepat, lalu lepaskan dan haluskan sisi individu jika konten membutuhkan spasi asimetris.
- Hindari padding berlebihan di perangkat mobile — uji spasi Anda pada lebar viewport sempit untuk memastikan konten tidak terkompresi atau terlalu dipadatkan.