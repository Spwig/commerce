---
title: Editor Bayangan
---

Editor bayangan memungkinkan Anda menambahkan kedalaman dan dimensi ke elemen dengan bayangan kotak dan teks yang dapat dikonfigurasi. Bayangan menciptakan hierarki visual, menarik perhatian pada elemen penting, dan memberikan toko online Anda nuansa modern yang rapi. Buka **tab Gaya** dari elemen apa pun dan cari kelompok **Efek** untuk mengakses editor bayangan.

![Editor Bayangan](/static/core/admin/img/help/shadow-editor/shadow-editor.webp)

## Jenis Bayangan

Editor menyediakan dua tab di bagian atas:

- **Bayangan Kotak** — Menambahkan bayangan di sekitar kotak pembatas seluruh elemen. Gunakan ini untuk kartu, tombol, kontainer, gambar, dan bagian.
- **Bayangan Teks** — Menambahkan bayangan di belakang karakter teks saja. Gunakan ini untuk judul atau teks yang ditempatkan di atas gambar untuk meningkatkan keterbacaan.

Setiap tab memiliki konfigurasi yang independen. Anda dapat menerapkan bayangan kotak dan bayangan teks pada elemen yang sama jika diperlukan.

## Properti Bayangan

Setiap lapisan bayangan didefinisikan oleh properti berikut:

| Properti | Deskripsi | Rentang |
|----------|-------------|-------|
| **Offset X** | Jarak horizontal bayangan dari elemen | -50px hingga 50px |
| **Offset Y** | Jarak vertikal bayangan dari elemen | -50px hingga 50px |
| **Radius Blur** | Seberapa lembut atau kabur bayangan terlihat. Nilai yang lebih tinggi menghasilkan bayangan yang lebih lembut. | 0px hingga 100px |
| **Radius Penyebaran** | Memperluas atau mengurangi ukuran bayangan relatif terhadap elemen (hanya bayangan kotak) | -50px hingga 50px |
| **Warna** | Warna bayangan, dapat dikonfigurasi dengan dukungan opasitas penuh melalui pemilih warna | Warna apa pun dengan alpha |
| **Inset** | Toggle untuk menggambar bayangan di dalam elemen, bukan di luar (hanya bayangan kotak) | On / Off |

Atur nilai menggunakan penggeser atau ketikkan angka yang tepat langsung ke dalam bidang input.

## Bayangan Berganda

Anda dapat menumpuk beberapa lapisan bayangan pada satu elemen untuk menciptakan efek kedalaman yang kompleks dan realistis:

- Klik tombol **+** untuk menambahkan lapisan bayangan baru
- Setiap lapisan muncul sebagai baris dalam daftar bayangan dengan kontrolnya sendiri
- Drag lapisan untuk mengurutkan ulangnya — bayangan ditampilkan dalam urutan daftar, dengan lapisan pertama di atas
- Toggle ikon **mata** pada lapisan apa pun untuk menyembunyikan sementara tanpa menghapus konfigurasi
- Klik ikon **sampah** untuk menghapus lapisan

Menggabungkan bayangan gelap yang ketat dengan bayangan lebar yang lembut menciptakan efek "dangkat" alami yang meniru kedalaman fisik.

## Preset Bayangan

Preset yang dapat diterapkan cepat memungkinkan Anda menambahkan gaya bayangan umum dengan satu klik:

| Preset | Deskripsi |
|--------|-------------|
| **Kecil** | Bayangan ringan dan dekat untuk sedikit kenaikan (kartu, input) |
| **Sedang** | Kedalaman sedang untuk elemen interaktif (tombol, dropdown) |
| **Besar** | Bayangan yang menonjol untuk elemen mengambang (modal, popovers) |
| **Lembut** | Penyebaran lebar dengan opasitas rendah untuk efek sinar lembut dan kabur |
| **Tajam** | Penyebaran minimal dengan opasitas tinggi untuk efek tepi tajam dan terdefinisi |
| **Inset** | Bayangan dalam untuk tampilan tertekan atau terkikis |

Setelah menerapkan preset, Anda dapat menyesuaikan properti individu untuk menyempurnakan hasilnya.

## Perbandingan Bayangan Saat Ini vs Baru

Di bagian bawah editor, dua kotak perbandingan menampilkan **bayangan saat ini** (yang disimpan) dan **bayangan baru** (perubahan Anda yang belum disimpan). Tampilan sampingan ini memudahkan Anda mengevaluasi perbedaan sebelum mengonfirmasi. Klik **Terapkan** untuk menerima, atau klik di luar untuk membuang perubahan Anda.

## Di Mana Terdapat

Editor bayangan tersedia di lokasi berikut:

- **Pembangun Halaman** — Tab Gaya, kelompok Efek pada bagian, kontainer, kolom, dan elemen individu
- **Pembangun Header/Footer** — Pengaturan bayangan tingkat widget untuk elemen seperti logo, bar pencarian, dan item navigasi

Setiap elemen yang mendukung kelompok gaya Efek akan menampilkan kontrol editor bayangan.

## Tips

- Gunakan bayangan yang ringan (preset Kecil atau Lembut) untuk sebagian besar elemen — bayangan berat dapat membuat desain terasa berantakan.
- Gabungkan bayangan gelap dekat dengan bayangan terang jauh untuk efek kenaikan yang paling alami.
- Bayangan inset bekerja dengan baik pada bidang input dan kontainer untuk menciptakan efek panel yang terkikis.
- Bayangan teks harus minimal — offset 1px dengan sedikit blur meningkatkan keterbacaan pada latar belakang gambar tanpa terlihat ketinggalan zaman.
- Uji bayangan Anda di latar belakang terang dan gelap jika tema Anda mendukung toggle mode gelap.

Ingat: Pertahankan semua format markdown, jalur gambar, blok kode, dan istilah teknis tepat seperti yang ditunjukkan dalam aturan preservasi.