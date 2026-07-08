---
title: Diskon Staf POS dan Keamanan Terminal
---

Pengaturan diskon staf POS memungkinkan Anda mengontrol seberapa besar diskon yang dapat diterapkan oleh setiap staf di titik penjualan. Acara kunci terminal menyediakan jejak audit setiap kali terminal dikunci atau dikunci ulang — membantu Anda melacak siapa yang mengakses terminal dan apakah ada upaya login gagal yang terjadi.

## Batas Diskon Staf

Setiap staf yang menggunakan POS dapat memiliki izin diskon individu. Secara default, staf dapat menerapkan diskon hingga 10% untuk barang atau seluruh keranjang. Anda dapat meningkatkan atau menurunkan batas ini per orang, atau menunjuk staf sebagai manajer yang dapat menyetujui diskon yang melebihi batas standar.

### Mengatur Batas Diskon Staf

1. Navigasikan ke **POS > Diskon Staf**
2. Klik **+ Tambahkan Diskon Staf POS** atau klik staf yang sudah ada untuk mengedit
3. Pilih **Anggota Staf** dari daftar
4. Tetapkan batas diskon:

| Bidang | Deskripsi |
|-------|-------------|
| **Maksimal Diskon %** | Persentase maksimal diskon yang dapat diterapkan oleh orang ini (misalnya, `10` untuk 10%) |
| **Maksimal Jumlah Diskon** | Jumlah tetap maksimal per transaksi (biarkan kosong untuk tidak ada batas tetap) |
| **Dapat Menerapkan Diskon Item** | Izinkan diskon untuk item individu |
| **Dapat Menerapkan Diskon Keranjang** | Izinkan diskon untuk total keranjang seluruhnya |
| **Memerlukan Alasan** | Ketika dicentang, staf harus mengetik alasan sebelum menerapkan diskon apa pun |

5. Klik **Simpan**

### Cara Batas Diskon Berfungsi di POS

Ketika kasir mencoba menerapkan diskon:
- Jika diskon berada dalam batas mereka, diskon diterapkan secara langsung
- Jika diskon melebihi batas mereka, terminal meminta **persetujuan manajer**
- Seorang manajer memasukkan PIN mereka untuk mengizinkan pengecualian, dan diskon diterapkan

Alur kerja ini mencegah diskon bernilai tinggi yang tidak sah, sambil memungkinkan fleksibilitas ketika diskon yang sah diperlukan.

## Peran Manajer

Staf dengan bendera **Adalah Manajer** dapat menyetujui diskon yang melebihi batas staf lain. Manajer diidentifikasi di terminal melalui PIN yang mereka masukkan ketika persetujuan diminta.

### Menyiapkan Manajer

1. Buka catatan diskon staf
2. Centang **Adalah Manajer**
3. Masukkan **PIN Manajer** (4-6 digit) — PIN ini dihash secara aman saat disimpan
4. Klik **Simpan**

PIN manajer terpisah dari PIN kasir yang digunakan untuk mengunci/membuka kunci terminal. Seorang manajer dapat memiliki PIN manajer (untuk persetujuan diskon) dan PIN kasir (untuk akses terminal).

### Keamanan PIN Manajer

Ketika Anda memasukkan PIN dalam formulir admin dan menyimpannya, Spwig secara otomatis menghash-nya — PIN biasa tidak pernah disimpan. Bidang PIN biasa akan dihapus setelah disimpan, yang merupakan perilaku yang diharapkan.

## PIN Kasir dan Akses Kartu

Setiap staf juga dapat memiliki **PIN Kasir** untuk mengunci dan membuka kunci terminal:

- **PIN Kasir** — PIN 4-6 digit yang digunakan untuk membuka kunci terminal setelah terminal dikunci otomatis atau dikunci secara manual
- **Identifikasi Kartu** — Kartu yang terdaftar (kartu gesek atau NFC) juga dapat digunakan untuk membuka kunci terminal

Untuk menyiapkan PIN kasir, masukkan PIN tersebut ke dalam bidang **PIN Kasir** dan simpan. Seperti PIN manajer, PIN ini secara otomatis dihash saat disimpan.

## Acara Kunci Terminal

Setiap kali terminal dikunci atau dikunci ulang, Spwig mencatat acara kunci terminal. Hal ini menciptakan jejak audit keamanan yang lengkap.

### Melihat Acara Kunci

Navigasikan ke **POS > Acara Kunci Terminal** untuk melihat sejarah lengkap. Anda dapat menyaring acara berdasarkan:
- Terminal
- Jenis acara
- Rentang tanggal

### Jenis Acara

| Event | Makna |
|-------|---------|
| **Manual Lock** | Seorang staf dengan sengaja mengunci terminal |
| **Auto-Lock (Idle Timeout)** | Terminal dikunci secara otomatis karena tidak aktif |
| **Unlock by Cashier** | Kasir terautentikasi dan membuka kunci terminal |
| **Unlock by Manager** | Seorang manajer menggunakan kredensial mereka untuk membuka kunci |
| **Unlock by Card** | Terminal dibuka kunci menggunakan kartu swipe yang terdaftar |
| **Unlock by Biometric** | Terminal dibuka kunci menggunakan sidik jari atau pengenalan wajah |
| **Failed Unlock Attempt** | Upaya membuka kunci dilakukan dengan kredensial yang salah |
| **Lockout (3+ failures)** | Terminal dikunci setelah beberapa upaya gagal berulang kali |

### Apa yang terkandung dalam catatan kejadian kunci

Setiap kejadian mencatat:
- Terminal yang terlibat (**Terminal**)
- Jenis kejadian (**Event Type**)
- Siapa yang melakukan aksi (**Performed By**) dan siapa yang masuk saat terjadi kunci (**Locked By**)
- Apakah **Manager Override** digunakan
- Metode **Unlock** (PIN, kartu, atau biometrik)
- **Failed Attempts** sebelum kejadian ini (berguna untuk mengidentifikasi pola brute-force)
- **Cart Total** dan jumlah item saat kejadian terjadi
- Alamat IP dari permintaan

### Menyelidiki masalah keamanan

Jika Anda mencurigai akses tidak sah ke terminal:

1. Navigasikan ke **POS > Terminal Lock Events**
2. Filter berdasarkan terminal yang dimaksud
3. Cari kejadian tipe **Failed Unlock Attempt** atau **Lockout** — ini menunjukkan akses gagal berulang kali
4. Periksa bidang **Performed By** pada pembukaan kunci yang berhasil untuk melihat siapa yang mendapatkan akses
5. Bandingkan dengan catatan shift (**POS > Shifts**) untuk memverifikasi kasir yang seharusnya sedang bertugas

## Tips

- Tetapkan batas diskon berdasarkan tingkat senioritas staf — staf baru mungkin mulai dari 5%, staf berpengalaman dari 10-15%, dan manajer dapat menyetujui yang lebih tinggi.
- Aktifkan **Requires Reason** untuk staf dengan batas diskon yang lebih tinggi. Memiliki alasan dalam catatan membantu Anda menganalisis pola diskon dan mengidentifikasi penggunaan yang tidak sah.
- Periksa catatan kejadian kunci terminal secara mingguan jika toko Anda memiliki banyak staf atau tingkat pergantian staf yang tinggi — pola akses yang tidak teratur lebih mudah terlihat sebelum menjadi masalah.
- Jika seorang staf meninggalkan, segera hapus PIN kasir dan identifikasi kartu mereka untuk mencegah akses ke terminal.
- Gunakan kejadian kunci untuk mengidentifikasi terminal yang mungkin memerlukan penyesuaian timeout auto-lock — jika pelanggan sering memicu kunci tidak sengaja, timeout idle mungkin terlalu pendek.
- PIN manajer harus diubah secara berkala. Perbarui di catatan diskon staf — PIN baru akan dihash saat disimpan.