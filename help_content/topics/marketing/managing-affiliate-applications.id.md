---
title: Mengelola Aplikasi Afiliasi
---

Ketika mitra potensial mengajukan untuk bergabung dengan program afiliasi Anda, mereka akan muncul dalam antrian aplikasi Anda yang menunggu tinjauan. Panduan ini menunjukkan cara Anda mengevaluasi, menyetujui, dan menolak aplikasi afiliasi untuk membangun jaringan mitra berkualitas yang selaras dengan merek Anda.

Mengelola aplikasi secara hati-hati memastikan Anda bekerja dengan afiliasi yang dapat dipercaya yang akan mewakili toko Anda secara profesional dan mendorong penjualan yang autentik.

![Tampilan Daftar Aplikasi](/static/core/admin/img/help/managing-affiliate-applications/applications-list.webp)

## Sumber Aplikasi

Aplikasi afiliasi mencapai antrian Anda melalui beberapa saluran:

### Aplikasi dari Portal Umum

Sebagian besar aplikasi berasal dari portal afiliasi umum di `/affiliate/` di toko Anda. Ketika mitra afiliasi potensial mengklik **Menjadi Afiliasi**, mereka menyelesaikan formulir pendaftaran yang menciptakan catatan aplikasi.

### Pengguna Tamu vs Pengguna Terdaftar

Jika Anda telah mengaktifkan **Izinkan Pendaftaran Tamu** di pengaturan afiliasi, pengguna non-pelanggan dapat langsung mengajukan. Jika tidak, pengguna harus terlebih dahulu membuat akun pelanggan di toko Anda sebelum mereka dapat mengajukan untuk menjadi afiliasi.

### Persyaratan Tinjauan Manual

Ketika **Memerlukan Persetujuan** diaktifkan di pengaturan afiliasi Anda (dianjurkan), semua aplikasi berada dalam status **Menunggu** yang menunggu tinjauan Anda. Jika dinonaktifkan, aplikasi disetujui secara otomatis dan afiliasi mendapatkan akses langsung ke dasbor mereka.

## Melihat Aplikasi

Navigasikan ke **Program Afiliasi > Aplikasi** (atau **Pemasaran > Keanggotaan Afiliasi** di admin) untuk melihat semua aplikasi program.

Tampilan daftar menunjukkan:

| Kolom | Deskripsi |
|--------|-------------|
| **Afiliasi** | Nama dan alamat email pendaftar |
| **Program** | Program afiliasi yang mereka ajukan |
| **Status** | Menunggu, disetujui, atau ditolak |
| **Tanggal Pendaftaran** | Kapan mereka mengirimkan aplikasi |
| **Metode Pembayaran** | Metode pembayaran yang mereka pilih (PayPal atau transfer bank) |

### Menyaring Aplikasi

Gunakan penyaring admin untuk menyempitkan aplikasi:

- **Status**: Lihat hanya aplikasi yang menunggu tinjauan
- **Program**: Saring berdasarkan program tertentu jika Anda menjalankan beberapa program afiliasi
- **Rentang Tanggal**: Cari aplikasi dari periode waktu tertentu

### Badge Aplikasi yang Menunggu

Sidebar admin menampilkan jumlah badge di sebelah **Afiliasi** ketika Anda memiliki aplikasi yang menunggu tindakan.

## Meninjau Aplikasi

Klik aplikasi apa pun untuk melihat profil pendaftar lengkap. Tampilan detail ini menunjukkan semua informasi yang Anda butuhkan untuk membuat keputusan persetujuan yang tepat.

![Kartu Detail Aplikasi](/static/core/admin/img/help/managing-affiliate-applications/application-detail-card.webp)

### Informasi Profil Afiliasi

Periksa detail penting tentang pendaftar:

**Informasi Dasar**
- **Alamat Email**: Digunakan untuk login dan komunikasi
- **Nama Perusahaan/Bisnis**: Organisasi mereka (jika berlaku)
- **URL Situs Web**: Platform promosi utama mereka
- **Nomor Telepon**: Informasi kontak

**Informasi Pembayaran**
- **Metode Pembayaran**: PayPal atau transfer bank
- **Email PayPal**: Diperlukan jika mereka memilih pembayaran PayPal
- **Detail Rekening Bank**: Diperlukan jika mereka memilih transfer bank (nomor rekening, nomor routing, kode SWIFT)

**Saluran Promosi**
Banyak aplikasi mencakup catatan tentang di mana afiliasi berencana mempromosikan produk Anda — akun media sosial, saluran YouTube, daftar email, atau blog.

### Detail Program

Periksa program mana yang mereka ajukan dan tinjau tingkat komisi, masa cookie, dan ambang batas pembayaran minimum. Pastikan pendaftar cocok dengan audiens target program.

### Riwayat Aplikasi

Jika seorang pendaftar sebelumnya ditolak atau telah mengajukan ke beberapa program, riwayat ini muncul dalam tampilan detail.

## Kriteria Persetujuan

Gunakan daftar pemeriksa ini untuk mengevaluasi setiap aplikasi secara konsisten:

### Kelayakan Bisnis

- [ ] **Situs Web atau Media Sosial Aktif**: Apakah pendaftar memiliki platform yang aktif dengan konten nyata?
- [ ] **Audiens yang Relevan**: Apakah audiens mereka cocok dengan demografi pelanggan target Anda?
- [ ] **Konten Berkualitas**: Apakah konten mereka profesional, terdokumentasi dengan baik, dan selaras dengan nilai-nilai merek Anda?
- [ ] **Platform yang Terbentuk**: Apakah mereka memiliki pengikut yang terlibat atau lalu lintas yang bermakna?

### Informasi Pembayaran

- [ ] **Detail Pembayaran yang Valid**: Apakah mereka menyediakan alamat email PayPal yang berfungsi atau informasi rekening bank yang lengkap?
- [ ] **Identitas yang Cocok**: Apakah detail pembayaran selaras dengan nama bisnis mereka atau informasi pribadi?

### Kesesuaian Merek

- [ ] **Kesesuaian yang Tepat**: Apakah konten, nada, dan gaya mereka selaras dengan citra merek Anda?
- [ ] **Tidak Ada Konflik**: Apakah mereka sudah mempromosikan pesaing langsung?
- [ ] **Standar Profesional**: Apakah mereka mempertahankan standar kualitas yang Anda nyaman asosiasikan?

### Pencegahan Penipuan

- [ ] **Tidak Ada Tanda Merah**: Periksa tanda seperti alamat email umum, profil yang tidak lengkap, atau pola situs web mencurigakan
- [ ] **Tidak Ada Pelanggaran Sebelumnya**: Apakah mereka sebelumnya ditolak karena penipuan atau pelanggaran ketentuan?
- [ ] **Harapan yang Masuk Akal**: Apakah rencana promosi yang mereka nyatakan realistis dan dapat dicapai?

Jika aplikasi memenuhi semua kriteria, setujui. Jika gagal dalam pemeriksaan kritis (risiko penipuan, ketidaksesuaian merek, informasi pembayaran tidak valid), tolak dengan alasan yang jelas.

## Menyetujui Aplikasi

Ikuti langkah-langkah berikut untuk menyetujui satu atau lebih aplikasi:

### Persetujuan Aplikasi Tunggal

1. Buka halaman detail aplikasi
2. Tinjau semua informasi profil dengan hati-hati
3. Verifikasi detail pembayaran sudah lengkap dan valid
4. Klik tombol **Simpan dan Lanjutkan Mengedit** jika Anda perlu membuat catatan
5. Pilih **Setujui** dari dropdown status
6. Klik **Simpan**

### Persetujuan Massal

Untuk beberapa aplikasi yang memenuhi syarat:

1. Navigasikan ke daftar aplikasi di **Program Afiliasi > Aplikasi**
2. Centang kotak di sebelah aplikasi yang ingin Anda setujui
3. Pilih **Setujui aplikasi yang dipilih** dari dropdown **Tindakan**
4. Klik **Go**
5. Konfirmasi tindakan massal ketika diminta

### Apa yang Terjadi Setelah Persetujuan

Ketika Anda menyetujui aplikasi:

- Status afiliasi berubah menjadi **Disetujui**
- Mereka menerima notifikasi email (jika template email dikonfigurasi)
- Mereka mendapatkan akses ke dasbor afiliasi untuk membuat tautan pelacakan
- Mereka dapat mulai mempromosikan produk Anda dan memperoleh komisi

Afiliasi yang disetujui muncul dalam daftar afiliasi dengan status **Aktif** dan dapat segera mempromosikan program Anda.

## Menolak Aplikasi

Tolak aplikasi yang tidak memenuhi kriteria Anda untuk melindungi merek Anda dan mencegah penipuan.

### Kapan Menolak

Alasan umum penolakan:

- **Tidak Ada Platform Aktif**: Pendaftar tidak memiliki situs web, blog, atau kehadiran media sosial
- **Konflik Pesaing**: Mereka secara utama mempromosikan pesaing langsung
- **Ketidakcocokan Merek**: Gaya konten, bahasa, atau nilai mereka bertentangan dengan merek Anda
- **Informasi Pembayaran Tidak Valid**: Tidak ada atau jelas palsu detail pembayaran
- **Aktivitas Mencurigakan**: Email umum, profil tidak lengkap, atau indikator penipuan
- **Pelanggaran Ketentuan**: Mitra afiliasi sebelumnya yang melanggar ketentuan program

### Cara Menolak

1. Buka halaman detail aplikasi
2. Tinjau informasi pendaftar untuk memastikan penolakan tepat
3. Tambahkan catatan di bidang **Catatan** yang menjelaskan alasan (hanya untuk referensi internal)
4. Ubah dropdown **Status** menjadi **Ditolak**
5. Klik **Simpan**

### Setelah Penolakan

Ketika Anda menolak aplikasi:

- Status afiliasi berubah menjadi **Ditolak**
- Mereka kehilangan akses ke dasbor afiliasi (jika mereka memiliki akses)
- Mereka tidak dapat membuat tautan pelacakan atau memperoleh komisi
- Tidak ada notifikasi otomatis yang dikirim (Anda dapat menyesuaikan ini di template email)

Afiliasi yang ditolak tetap ada di database Anda untuk catatan. Anda dapat mengubah status mereka menjadi **Disetujui** nanti jika situasi berubah.

## Pengaturan Persetujuan Otomatis

Kontrol apakah aplikasi memerlukan tinjauan manual dalam konfigurasi program afiliasi Anda:

### Tinjauan Manual (Dianjurkan)

Navigasikan ke program Anda di **Pemasaran > Program Afiliasi** dan pastikan **Persetujuan Otomatis** tidak dicentang. Pengaturan ini berarti:

- Semua aplikasi dimulai sebagai **Menunggu**
- Anda meninjau setiap pendaftar sebelum mereka mendapatkan akses
- Kontrol kualitas yang lebih baik dan pencegahan penipuan
- Lebih banyak pekerjaan untuk Anda, tetapi lebih aman untuk merek Anda

Gunakan tinjauan manual ketika Anda ingin memeriksa mitra secara hati-hati, bekerja dengan influencer terpilih, atau mempertahankan standar merek yang ketat.

### Mode Persetujuan Otomatis

Centang **Persetujuan Otomatis** di pengaturan program Anda untuk menerima semua aplikasi secara otomatis. Ini berarti:

- Aplikasi melewati status menunggu dan langsung ke **Disetujui**
- Afiliat mendapatkan akses langsung ke dasbor mereka
- Lebih sedikit pekerjaan untuk Anda, tetapi risiko penipuan lebih tinggi
- Terbaik untuk program rujukan terbuka dengan banyak mitra

Gunakan persetujuan otomatis untuk program rujukan umum di mana Anda ingin memaksimalkan partisipasi dan menerima variasi kualitas.

## Tindakan Massal

Proses beberapa aplikasi secara efisien menggunakan tindakan massal antarmuka admin:

### Menyetujui Beberapa Aplikasi

1. Navigasikan ke **Program Afiliasi > Aplikasi**
2. Gunakan penyaring untuk menampilkan hanya aplikasi **Menunggu**
3. Centang kotak untuk semua aplikasi yang ingin Anda setujui
4. Pilih **Setujui aplikasi yang dipilih** dari dropdown **Tindakan**
5. Klik **Go** dan konfirmasi

### Menyaring untuk Efisiensi

Gabungkan penyaring untuk memproses aplikasi dalam batch:

- **Program + Status**: Setujui semua aplikasi yang menunggu untuk program influencer Anda
- **Tanggal + Status**: Tinjau aplikasi dari minggu terakhir
- **Metode Pembayaran + Status**: Proses semua aplikasi PayPal bersama

Pendekatan pengelompokan ini membantu Anda meninjau aplikasi yang mirip bersama, membuat lebih mudah untuk menerapkan standar yang konsisten.

## Tips

- **Tinjau dalam 24-48 jam** — Waktu respons cepat menciptakan kesan pertama yang positif dan mencegah pendaftar kehilangan minat atau mendaftar ke pesaing
- **Verifikasi detail pembayaran sejak awal** — Menangkap alamat email PayPal yang tidak valid atau detail rekening bank yang tidak lengkap pada tahap aplikasi mencegah masalah pembayaran nanti
- **Periksa konten mereka terlebih dahulu** — Kunjungi situs web atau profil media sosial pendaftar sebelum menyetujui untuk memverifikasi bahwa mereka memiliki konten nyata dan audiens yang terlibat
- **Dokumentasikan alasan penolakan** — Gunakan bidang catatan untuk mencatat mengapa Anda menolak aplikasi. Ini membantu menjaga konsistensi dan melindungi Anda jika pendaftar mengajukan ulang nanti
- **Tetapkan persyaratan program yang jelas** — Perbarui halaman landing portal afiliasi Anda untuk secara jelas menyatakan apa yang Anda cari dalam mitra (ukuran audiens minimum, jenis konten, dll.) untuk mengurangi aplikasi yang tidak memenuhi syarat
- **Perhatikan pendaftar ulang** — Beberapa afiliasi yang ditolak mengajukan ulang dengan alamat email yang berbeda. Periksa URL situs web, nama perusahaan, dan detail pembayaran untuk menangkap duplikat
- **Mulai dengan ketat** — Lebih mudah untuk menyetujui secara lebih longgar seiring waktu daripada menghapus afiliasi yang bermasalah nanti. Mulailah dengan kriteria persetujuan yang ketat dan longgarkan jika Anda membutuhkan lebih banyak mitra