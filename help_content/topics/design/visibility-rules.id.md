---
title: Aturan Visibilitas
---

# Aturan Visibilitas

Aturan visibilitas memungkinkan Anda menampilkan atau menyembunyikan bagian toko Anda tergantung siapa yang mengunjungi dan di mana mereka berada. Anda dapat mengunci **elemen halaman**, **item menu**, dan **widget header/footer** dengan kondisi yang sama — pasar atau wilayah pelanggan, bahasa atau mata uang yang mereka tonton, waktu sehari, atau tanda pengguna individu seperti apakah mereka sudah masuk.

Semua dibangun dari **kelompok aturan**: bundelan yang dapat digunakan kembali, terdiri dari satu atau lebih kondisi. Anda membuat kelompok aturan sekali (misalnya, "pasar Selandia Baru" atau "anggota yang sudah masuk") lalu sambungkan ke setiap elemen, item menu, atau widget yang ingin Anda kendalikan. Suatu item tanpa kelompok aturan yang terkait akan selalu terlihat.

## Bagaimana visibilitas ditentukan

Ketika lebih dari satu kelompok aturan terpasang pada suatu item, item tersebut ditampilkan jika **salah satu** kelompok yang terkait cocok (mereka menggabungkan dengan OR). Dalam satu kelompok, Anda memilih apakah **semua** atau **salah satu** dari kondisinya harus cocok.

Aturan terbagi menjadi dua keluarga, dan Spwig menanganinya secara berbeda agar toko Anda tetap cepat dan ramah mesin pencari:

- **Aturan pasar** — kondisi berdasarkan wilayah/pasaran, bahasa, mata uang, dan waktu. Ini ditentukan di server untuk setiap URL pasar, jadi halaman yang sama dikirimkan secara identik kepada setiap pengunjung (dan setiap mesin pencari) di alamat tersebut. Hal ini menjaga halaman tetap bisa dicache dan aman untuk SEO.
- **Aturan pengguna individu** — status masuk pengguna, isi keranjang belanja, perangkat, dan lokasi tepat. Ini tergantung pada pengguna individu, jadi Spwig menyelesaikan secara pribadi untuk setiap orang setelah halaman dimuat. Mereka tidak per mai dikirimkan ke halaman yang dicache secara bersamaan.

Jika Anda menonaktifkan kelompok aturan, itu hanya berhenti berlaku — item yang terkait kembali menjadi terlihat. Menonaktifkan kelompok bukanlah cara untuk menyembunyikan sesuatu.

## Membuat dan menyambungkan aturan

Ada dua cara untuk bekerja dengan kelompok aturan.

### Sambungkan di mana Anda merancang

Di mana pun Anda dapat mengunci konten, Anda akan melihat **kontrol visibilitas** (ikon mata):

- **Page Builder** — pilih elemen, buka propertinya, dan gunakan kontrol visibilitas.
- **Menu Builder** — pilih item menu dan buka **Tab Visibilitas**. Ini berjalan pada **semua** item, termasuk item sub-menu (dropdown) yang tertanam di bawah yang lain — aturan pada anak hanya menyembunyikan anak tersebut, sementara bagian lain dari menu tetap utuh.
- **Header & Footer Builder** — pilih widget dan buka bagian **Kelompok Aturan Visibilitas** dari pengaturan widget tersebut.

Aturan yang bergantung pada pengguna individu — apakah mereka sudah masuk, apa yang ada di keranjang belanja mereka, atau perangkat mereka — diselesaikan untuk setiap pembeli tanpa melambatkan toko Anda atau memengaruhi mesin pencari. Toko depan Anda tetap cepat dan bisa dicache, dan setiap pengunjung tetap melihat navigasi yang ditujukan untuk mereka.

Di pengedit visibilitas Anda dapat:

- **Sambungkan** salah satu kelompok aturan yang sudah ada dengan menandai kotaknya.
- **Aturan cepat** — buat kelompok aturan sederhana secara langsung (misalnya, "hanya anggota", satu pasar, mata uang, perangkat, atau nilai keranjang minimum) dan sambungkan dalam satu langkah.
- **Kelola kelompok aturan** — lompat ke pembuat lengkap untuk aturan lanjutan.

Klik **Terapkan** dan itemnya langsung dikunci.

### Bangun aturan lanjutan

Untuk apa pun yang lebih rumit — menggabungkan beberapa kondisi, mengelompokkan, atau operator yang lebih presisi — pergi ke **Desain → Aturan Visibilitas** (kelompok aturan). Di sana Anda dapat menyusun aturan dengan logika AND/OR dan menggunakannya kembali di seluruh toko Anda.

## Kondisi umum

Jaga semua format markdown, jalur gambar, blok kode, dan istilah teknis.

| Kondisi | Gunakan untuk… |
|-----------|----------------|
| **Wilayah / pasar** | Tampilkan blok hanya untuk pengunjung di pasar tertentu (misalnya Selandia Baru) |
| **Mata uang yang dipilih** | Tampilkan catatan harga atau tawaran hanya ketika mata uang tertentu aktif |
| **Bahasa yang dipilih** | Tampilkan konten hanya dalam bahasa tertentu |
| **Tanggal / waktu / hari / jam kerja** | Jalankan banner selama jendela penjualan atau hanya selama jam operasional |
| **Status pengguna yang masuk** | Tampilkan konten "hanya anggota", atau undangan pendaftaran untuk tamu |
| **Jenis perangkat** | Tampilkan atau sembunyikan sesuatu di ponsel, tablet, atau desktop |
| **Nilai keranjang / item** | Tampilkan petunjuk pengiriman gratis sekali keranjang melewati ambang batas |

## Mempratinjau

Di pratinjau Builder Halaman, Anda dapat **mempratinjau sebagai pasar** dan **mempratinjau sebagai pengunjung** (yang masuk atau tamu, dengan keranjang contoh) untuk melihat apa yang akan dilihat setiap audiens — termasuk aturan per pengguna yang biasanya diselesaikan secara rahasia.

## Tips

- Bangun kumpulan kelompok aturan yang baik nama ("pasar Selandia Baru", "Anggota", "Hanya Ponsel") dan gunakan kembali di mana-mana — lebih mudah dikelola daripada aturan satu kali.
- Aturan pasar adalah pilihan yang aman untuk apa pun yang ingin diindeks mesin pencari, karena hasilnya sama untuk semua orang di URL pasar tertentu.
- Jika suatu item tiba-tiba menghilang, periksa kelompok aturan yang terkait — suatu item hanya disembunyikan ketika memiliki kelompok aktif dan tidak ada yang cocok dengan pengunjung saat ini.