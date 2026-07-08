---
title: Elemen Kustom
---

Elemen kustom memungkinkan Anda membuat blok pembangun halaman yang dapat digunakan kembali yang disesuaikan dengan kebutuhan toko Anda. Anda merancang elemen secara visual menggunakan alat pembangun halaman yang sudah ada, lalu secara opsional menghubungkannya dengan data toko yang sedang berjalan — seperti nama produk, harga, atau gambar — sehingga elemen tersebut secara otomatis diisi dengan konten nyata ketika ditempatkan di halaman. Setelah dibuat, elemen kustom Anda akan muncul di perpustakaan elemen pembangun halaman bersama dengan blok bawaan.

![Perpustakaan Elemen Kustom](/static/core/admin/img/help/custom-elements/custom-elements-list.webp)

## Kapan menggunakan elemen kustom

Elemen kustom paling bernilai ketika Anda menemukan diri Anda membuat tata letak yang sama berulang kali. Sebagai ganti membuat ulang "kartu produk unggulan" dari awal di setiap halaman, Anda membuatnya sekali sebagai elemen kustom dan meletakkannya di mana saja yang Anda butuhkan. Jika elemen tersebut terikat data, maka secara otomatis akan menampilkan informasi produk terkini — tidak diperlukan pembaruan manual ketika harga atau nama berubah.

Penggunaan umum:

- Kartu penyorotan produk yang menampilkan nama, harga, dan gambar utama
- Blok promosi kategori dengan banner, judul, dan tautan
- Panel penampil merek dengan logo dan deskripsi
- Teks promosi artikel blog dengan gambar unggulan, judul, dan kutipan

## Membuat elemen kustom baru

1. Navigasikan ke **Desain > Elemen Kustom**
2. Klik **+ Tambah Elemen Kustom**
3. Spwig segera membuat elemen draf dan membuka **Pembangun Visual** — Anda tidak perlu mengisi formulir terlebih dahulu
4. Dalam Pembangun Visual, bangun tata letak elemen menggunakan alat pembangun halaman yang tersedia
5. Ketika Anda puas dengan desain, konfigurasikan pengaturan elemen (nama, pengikatan data, ikon) di bilah samping
6. Aktifkan **Aktif** saat Anda siap mempublikasikan elemen ke perpustakaan
7. Simpan elemen

Elemen sekarang tersedia di panel elemen pembangun halaman di bawah kategori yang Anda tetapkan.

## Pembangun Visual

Pembangun Visual adalah kanvas khusus untuk merancang elemen Anda. Ini bekerja seperti pembangun halaman standar tetapi fokus pada satu elemen daripada seluruh halaman. Anda dapat:

- Menambahkan dan mengatur ulang elemen anak (blok teks, gambar, kontainer, dll.)
- Menetapkan gaya, jarak, dan tata letak untuk setiap elemen anak
- Melihat bagaimana elemen akan terlihat dengan data contoh

Perubahan di Pembangun Visual disimpan langsung ke definisi elemen. Tidak ada langkah publikasi terpisah — menyimpan di pembangun langsung memperbarui elemen untuk halaman yang sudah menggunakan elemen tersebut.

## Mengonfigurasi pengaturan elemen

Setiap elemen kustom memiliki pengaturan berikut:

| Bidang | Deskripsi |
|-------|-------------|
| **Nama** | Nama tampilan yang ditampilkan di perpustakaan elemen |
| **Slug** | Identifikasi yang aman untuk URL, dihasilkan secara otomatis dari nama |
| **Deskripsi** | Catatan opsional tentang apa tujuan elemen ini |
| **Model Target** | Model toko yang akan diikatkan data darinya (lihat di bawah) |
| **Ikon** | Ikon yang ditampilkan di perpustakaan elemen |
| **Kategori** | Mengelompokkan elemen terkait bersama di perpustakaan |
| **Aktif** | Apakah elemen tersedia di pembangun halaman |

## Pengikatan data

Pengikatan data menghubungkan bagian tata letak elemen Anda dengan data toko yang sedang berjalan. Ketika editor halaman meletakkan elemen yang terikat data di halaman, mereka memilih catatan spesifik (misalnya, produk), dan semua bidang yang terikat akan diisi secara otomatis dari catatan tersebut.

### Memilih model target

Pengaturan **Model Target** menentukan jenis data toko yang dapat ditampilkan oleh elemen. Model yang tersedia adalah:

| Model | Apa yang disediakan |
|-------|-----------------|
| **Produk** | Nama, harga, status stok, gambar, deskripsi, SKU, kategori, merek, dan lainnya |
| **Kategori** | Nama, deskripsi, gambar, banner, jumlah produk, dan URL |
| **Merek** | Nama, logo, deskripsi, cerita merek, dan URL |
| **Artikel Blog** | Judul, kutipan, gambar unggulan, penulis, tanggal terbit, dan URL |

Biarkan **Model Target** kosong untuk membuat elemen statis tanpa data dinamis. Elemen statis berguna untuk komponen desain tetap seperti banner dekoratif atau pengisi tata letak.

### Cara kerja pengikatan


Dalam Visual Builder, Anda dapat menandai elemen anak individual sebagai terikat data dengan memilih bidang model yang harus ditampilkan.

Sebagai contoh:
- Sebuah elemen anak **teks** dapat diikat ke **Nama Produk**, sehingga menampilkan nama produk yang dipilih
- Sebuah elemen anak **gambar** dapat diikat ke **Gambar Utama**, sehingga menampilkan foto utama produk
- Sebuah elemen anak **teks** dapat diikat ke **Harga**, sehingga selalu mencerminkan harga saat ini

Setiap ikatan memetakan satu bidang konten elemen ke satu bidang model. Anda dapat menambahkan beberapa ikatan ke satu elemen kustom — misalnya, mengikat blok teks ke **Nama Produk** dan blok gambar terpisah ke **Gambar Utama** secara bersamaan.

### Preset gambar miniatur

Untuk ikatan gambar, Anda dapat secara opsional menentukan **Preset Miniatur** (seperti `thumbnail` atau `medium`). Ini mengontrol ukuran gambar yang dimuat, membantu halaman dimuat lebih cepat dengan menyajikan gambar dengan ukuran yang sesuai untuk tata letak elemen.

## Menonaktifkan dan mengaktifkan kembali elemen

Menonaktifkan elemen menghilangkannya dari perpustakaan elemen sehingga tidak dapat ditambahkan ke halaman baru. Halaman yang sudah ada dan menggunakan elemen tersebut tidak terpengaruh — elemen tersebut tetap ditampilkan di halaman-halaman tersebut.

Untuk menonaktifkan:
1. Navigasikan ke **Desain > Elemen Kustom**
2. Klik nama elemen
3. Hilangkan centang **Aktif**
4. Simpan

Untuk mengaktifkan kembali, ikuti langkah yang sama dan centang **Aktif** kembali.

## Memfilter perpustakaan elemen

Daftar elemen mendukung pemfilteran berdasarkan:
- **Aktif / Tidak Aktif** — tampilkan hanya elemen yang diterbitkan atau hanya elemen draf
- **Model Target** — filter berdasarkan model yang elemen tersebut terikat
- **Kategori** — filter berdasarkan kategori elemen
- **Cari** — cari berdasarkan nama, slug, atau deskripsi

Ini membantu ketika Anda memiliki banyak elemen kustom dan perlu menemukan satu tertentu dengan cepat.

## Contoh: kartu penekanan produk

**Tujuan:** Sebuah elemen kartu yang menampilkan gambar utama, nama, dan harga produk.

| Pengaturan | Nilai |
|---------|-------|
| Nama | Kartu Penekanan Produk |
| Model Target | Produk |
| Kategori | Produk |
| Ikon | fas fa-box |

Dalam Visual Builder, tambahkan:
- Sebuah elemen **Gambar** yang terikat ke **Gambar Utama** dengan preset miniatur `medium`
- Sebuah elemen **Teks** yang terikat ke **Nama Produk**
- Sebuah elemen **Teks** yang terikat ke **Harga**

Setelah disimpan dan diaktifkan, elemen muncul di pembangun halaman di bawah kategori Produk. Ketika editor halaman menambahkannya ke halaman, mereka memilih produk yang ingin ditampilkan, dan kartu akan otomatis terisi.

## Tips

- Beri elemen nama yang deskriptif yang mencakup tujuan dan jenis data — contohnya, "Kartu Penekanan Produk" daripada "Kartu 1" — sehingga perpustakaan tetap mudah dinavigasi saat berkembang
- Gunakan bidang **Kategori** untuk mengelompokkan elemen terkait (Produk, Blog, Promosi) — ini menjaga perpustakaan elemen tetap terorganisir untuk editor halaman Anda
- Uji elemen yang terikat data dengan menambahkannya ke halaman draf dan memilih catatan nyata sebelum diterbitkan, untuk memastikan ikatan menarik informasi yang benar
- Menonaktifkan elemen yang sudah usang daripada menghapusnya — ini mempertahankan halaman yang masih merujuk pada elemen tersebut dan memberi Anda pilihan untuk mengaktifkannya kembali
- Elemen statis (tidak ada model target) ideal untuk pola tata letak yang digunakan ulang di seluruh situs, seperti pemisah, panel CTA, atau spasi merek