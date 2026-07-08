---
title: 3D Product Configurator
---

3D Configurator memungkinkan pelanggan Anda melihat produk yang dapat dikonfigurasi dalam penampil 3D interaktif secara langsung di halaman produk. Saat pelanggan memilih opsi — seperti warna, bahan, atau variasi komponen — model 3D akan diperbarui secara real time untuk mencerminkan pilihan mereka. Pada perangkat mobile yang didukung, pelanggan juga dapat melihat produk dalam realitas teraugmentasi (AR), menempatkannya secara virtual di ruang mereka sendiri sebelum membeli.

3D Configurator bekerja dengan produk yang dapat dikonfigurasi. Setiap produk yang dapat dikonfigurasi dapat memiliki satu konfigurasi adegan 3D yang menghubungkan file model GLB dengan opsi konfigurasi produk.

## Sebelum memulai

Untuk membuat adegan 3D, Anda memerlukan:

- Sebuah **produk yang dapat dikonfigurasi** yang sudah dibuat di katalog Anda
- Sebuah **model 3D dasar** yang diunggah ke Perpustakaan Media Anda sebagai file GLB — ini adalah model yang telah dirakit dan muncul secara default
- Secara opsional, file GLB tambahan untuk pertukaran geometri (misalnya, bentuk leher yang berbeda), dan gambar tekstur untuk variasi bahan

Jika Anda belum membuat produk yang dapat dikonfigurasi dan opsi konfigurasinya, lakukan itu terlebih dahulu sebelum membuat adegan 3D.

## Membuat konfigurasi adegan

1. Navigasikan ke **Katalog > Konfigurasi Adegan 3D**
2. Klik **+ Tambah Konfigurasi Adegan 3D**
3. Pilih **Produk** yang adegan ini termasuk — hanya produk yang dapat dikonfigurasi yang tersedia
4. Pilih **Model 3D Dasar** dari Perpustakaan Media Anda — ini adalah file GLB yang dimuat secara default
5. Konfigurasikan pengaturan penampil (lihat di bawah)
6. Simpan catatan

Setelah disimpan, bidang **Node Tree** diisi secara otomatis. Ini adalah grafik adegan yang telah diparse yang diekstrak dari file GLB Anda — daftar setiap node yang dinamai di dalam model, yang akan Anda acu saat menambahkan peta node.

## Pengaturan penampil

Pengaturan ini mengontrol cara penampil 3D muncul di halaman produk Anda.

### Kamera dan pencahayaan

| Bidang | Deskripsi | Default |
|-------|-------------|---------|
| **Camera Orbit** | Posisi kamera awal dalam format `angle elevation distance` (misalnya, `0deg 75deg 2m`) | `0deg 75deg 2m` |
| **Camera Target** | Titik yang dilihat kamera, dalam meter dari pusat model (misalnya, `0m 0m 0m`) | `0m 0m 0m` |
| **Environment Image** | Gambar HDR dari Perpustakaan Media Anda yang digunakan untuk pencahayaan berbasis gambar — memberikan refleksi dan bayangan yang lebih realistis | Tidak ada |
| **Exposure** | Kecerahan keseluruhan adegan — nilai yang lebih rendah lebih gelap, nilai yang lebih tinggi lebih terang | `1.0` |

### Bayangan

| Bidang | Deskripsi | Default |
|-------|-------------|---------|
| **Shadow Intensity** | Seberapa kuat bayangan yang ditampilkan di bawah model — `0` tidak ada bayangan, `1` intensitas penuh | `0.5` |
| **Shadow Softness** | Seberapa kabur tepi bayangan — `0` tajam, `1` sangat lembut | `0.5` |

### Grading warna

| Bidang | Deskripsi |
|-------|-------------|
| **Tone Mapping** | Algoritma grading warna yang diterapkan pada adegan. **Commerce** menghasilkan warna yang cerah dan ramah produk. **Neutral** akurat dalam warna. **ACES** memberikan tampilan film yang sinematik. |
| **Bloom Strength** | Menambahkan efek cahaya pada bagian model yang memancarkan (dilampaukan). `0` menonaktifkan bloom. Nilai antara `1` dan `5` menghasilkan efek cahaya yang samar hingga dramatis. |

### Perilaku dan latar belakang

| Bidang | Deskripsi | Default |
|-------|-------------|---------|
| **Auto Rotate** | Apakah model berputar perlahan saat dimuat untuk menarik perhatian pelanggan | On |
| **AR Enabled** | Apakah pelanggan di perangkat yang didukung melihat tombol **Lihat dalam AR** | On |
| **Background** | Warna latar belakang penampil atau gradien CSS — masukkan nilai heksadesimal (misalnya, `#f5f5f5`) atau nilai gradien CSS | `#ffffff` |

### Thumbnail

Bidang **Thumbnail** menyimpan screenshot pratinjau dari penampil 3D, yang ditampilkan sebelum penampil dimuat. Anda dapat menangkap screenshot dari halaman produk yang aktif dan mengunggahnya ke Perpustakaan Media Anda, lalu menghubungkannya di sini untuk pengalaman muat halaman yang lebih halus.

## Mematikan dan mengaktifkan penampil 3D

Toggle **Enabled** mengontrol apakah penampil 3D ditampilkan di halaman produk.

Ketika dinonaktifkan, produk kembali ke konfigurator gambar 2D standar.

Ini memungkinkan Anda untuk menyiapkan konfigurasi adegan sebelum membuatnya terlihat oleh pelanggan.

## Menghubungkan opsi konfigurasi ke aksi 3D

Setelah adegan dasar dikonfigurasi, Anda dapat menghubungkan setiap opsi slot konfigurasi ke perubahan visual pada model 3D. Tautan ini disebut **Node Mappings** dan ditambahkan dalam bagian **Node Mappings** di bagian bawah formulir konfigurasi adegan.

### Bidang peta node

| Bidang | Deskripsi |
|-------|-------------|
| **Slot Option** | Opsi konfigurasi yang memicu perubahan ini (misalnya, "Red Leather") |
| **Action Type** | Apa perubahan visual yang terjadi (lihat jenis aksi di bawah) |
| **Target Node** | Nama node grafik adegan yang berubah — pilih dari nama yang terdaftar dalam **Node Tree** Anda |
| **Action Data** | Data spesifik aksi seperti kode warna heksadesimal, URL teksur, atau URL file GLB |
| **Sort Order** | Mengontrol urutan di mana beberapa peta untuk opsi yang sama diterapkan |

### Jenis aksi

| Aksi | Apa yang dilakukan |
|--------|-------------|
| **Material Color** | Mengubah warna material pada node target — berikan kode warna heksadesimal dalam **Action Data** |
| **Material Texture** | Mengganti teksur yang diterapkan pada material — tautkan ke aset gambar teksur dalam **Action Data** |
| **Geometry Swap** | Mengganti bagian model dengan file GLB yang berbeda — berguna untuk perubahan struktural seperti bentuk pegangan yang berbeda |
| **Visibility** | Menampilkan atau menyembunyikan node dalam adegan — atur `visible: true` atau `visible: false` dalam **Action Data** |

Beberapa peta dapat ditambahkan untuk satu opsi slot. Misalnya, memilih "Blue Denim" mungkin mengubah warna material *dan* menyembunyikan node trim kulit pada waktu yang sama.

## Aset geometri

Jika konfigurasi Anda mencakup aksi **Geometry Swap**, Anda perlu mendaftarkan file GLB pengganti sebagai Aset Geometri. Aset ini ditambahkan dalam bagian **Geometry Assets** dari formulir konfigurasi adegan.

| Bidang | Deskripsi |
|-------|-------------|
| **Label** | Nama deskriptif untuk aset geometri ini, misalnya, "V-Neck Collar" |
| **GLB File** | File GLB pengganti dari Perpustakaan Media Anda |
| **Target Node** | Node mana dalam model dasar yang aset geometri ini menggantikan |

Setelah menyimpan Aset Geometri, nama node-nya dipars dari GLB dan disimpan dalam **Node Data**, sehingga tersedia sebagai node target dalam peta Anda.

## Aset teksur

Gambar teksur yang digunakan dalam peta **Material Texture** dapat didaftarkan sebagai Aset Teksur untuk referensi yang lebih mudah. Aset ini ditambahkan dalam bagian **Texture Assets**.

| Bidang | Deskripsi |
|-------|-------------|
| **Label** | Nama deskriptif, misalnya, "Red Leather" |
| **Texture Image** | Gambar teksur dari Perpustakaan Media Anda |
| **Texture Type** | Saluran PBR yang teksur ini berlaku — Base Color, Normal Map, Roughness Map, Metalness Map, Ambient Occlusion, atau Emissive Map |

## Contoh: jaket yang dapat dikonfigurasi dengan opsi warna

**Skenario:** Jaket yang dapat dipesan dalam warna Hitam, Biru, atau Burgundy, dengan setiap warna diterapkan pada mesh tubuh jaket.

**Pengaturan:**

1. Buat konfigurasi adegan untuk produk jaket dengan file GLB jaket yang telah dirakit sebagai model dasar
2. Atur **Tone Mapping** ke Commerce dan **Auto Rotate** ke on
3. Dalam Node Mappings, tambahkan tiga entri — satu per opsi warna:

| Slot Option | Action Type | Target Node | Action Data |
|-------------|-------------|-------------|-------------|
| Black | Material Color | JacketBody | `{"color": "#1a1a1a"}` |
| Navy | Material Color | JacketBody | `{"color": "#1b2a4a"}` |
| Burgundy | Material Color | JacketBody | `{"color": "#6b2737"}` |

Ketika pelanggan memilih Navy di halaman produk, tampilan langsung memperbarui material JacketBody menjadi warna biru.

## Tips

Jaga semua format markdown, jalur gambar, blok kode, dan istilah teknis.

- Beri nama pada node GLB Anda secara jelas saat membuat model 3D Anda — nama node seperti "JacketBody" atau "CollarMesh" jauh lebih mudah digunakan dibandingkan nama yang dihasilkan secara otomatis seperti "Mesh_023"
- Gunakan **Commerce** tone mapping untuk sebagian besar produk — tone mapping ini dirancang untuk presentasi produk yang cerah dan menarik
- Nonaktifkan **Auto Rotate** untuk produk di mana sudut kamera default sudah menampilkan fitur penting, agar tidak mengganggu pelanggan saat halaman dimuat
- Uji tombol AR pada perangkat mobile sebenarnya sebelum mempromosikannya — ketersediaan AR bergantung pada perangkat dan browser pelanggan (iOS Safari dan Android Chrome dengan dukungan WebXR adalah yang paling andal)
- Unggah gambar **Thumbnail** untuk setiap konfigurasi scene — ini mencegah kotak putih kosong muncul sejenak saat viewer 3D dimuat
- Jika viewer 3D belum siap, nonaktifkan dengan toggle **Enabled** sehingga pelanggan melihat konfigurator gambar standar sebagai gantinya