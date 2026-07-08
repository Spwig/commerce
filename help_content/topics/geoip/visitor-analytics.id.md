---
title: Analitik Pengunjung
---

Analitik Pengunjung memberi Anda gambaran jelas tentang bagaimana pelanggan bergerak melalui toko Anda. Anda dapat melihat halaman mana yang menarik kunjungan terbanyak, bagaimana tren lalu lintas secara keseluruhan seiring waktu, perangkat apa yang digunakan pelanggan Anda, dan bagaimana pengunjung baru dibandingkan dengan pengunjung kembali — semua tanpa memerlukan alat analitik eksternal.

## Gambaran umum layar analitik

Toko Anda melacak aktivitas pengunjung secara otomatis setelah sistem GeoIP aktif. Data dikelompokkan menjadi tiga tampilan, masing-masing memberi Anda tingkat detail yang berbeda.

### Ringkasan lalu lintas harian

Navigasikan ke **Pelanggan > Statistik Lalu Lintas Harian** untuk melihat lalu lintas toko Anda secara keseluruhan untuk setiap hari. Setiap baris mewakili satu hari kalender dan menampilkan:

| Kolom | Apa yang diberitahu kepadamu |
|--------|-------------------|
| **Tanggal** | Hari lalu lintas dicatat |
| **Total Tampilan** | Semua tampilan halaman, termasuk bot |
| **Pengunjung Unik** | Pengunjung berbeda (berdasarkan sesi) |
| **Tampilan Bot** | Tampilan dari crawler dan alat otomatis |
| **Pengunjung Baru** | Sesi tanpa riwayat sebelumnya |
| **Pengunjung Kembali** | Sesi dari pengunjung yang pernah dilihat sebelumnya |
| **Tampilan Desktop** | Tampilan dari browser desktop |
| **Tampilan Mobile** | Tampilan dari perangkat mobile |
| **Tampilan Tablet** | Tampilan dari perangkat tablet |

Gunakan navigasi hierarki tanggal di bagian atas daftar untuk melompat cepat ke bulan atau tahun tertentu. Total diperbarui setiap hari melalui proses latar belakang otomatis, sehingga angka untuk hari ini akan muncul pada pagi hari berikutnya.

### Statistik per halaman

Navigasikan ke **Pelanggan > Statistik Halaman Harian** untuk melihat lalu lintas yang dipecahkan berdasarkan halaman individu. Setiap baris menampilkan satu jalur URL pada satu hari, sehingga Anda dapat membandingkan kinerja halaman tertentu seiring waktu.

| Kolom | Apa yang diberitahu kepadamu |
|--------|-------------------|
| **Tanggal** | Hari statistik ini berlaku |
| **Jalur URL** | Jalur halaman yang dinormalisasi (misalnya, `/products/blue-widget`) |
| **Tampilan** | Total tampilan untuk halaman tersebut pada hari itu |
| **Pengunjung Unik** | Pengunjung berbeda yang melihat halaman tersebut |
| **Tampilan Bot** | Tampilan dari bot pada halaman tersebut |
| **Pengunjung Masuk** | Berapa banyak sesi yang dimulai di halaman ini (halaman ini adalah halaman pertama mereka) |

Gunakan kotak pencarian **Jalur URL** untuk mencari statistik untuk halaman tertentu. Misalnya, cari `/products/` untuk melihat semua lalu lintas halaman produk, atau cari slug produk tertentu untuk fokus pada satu item.

### Acara tampilan halaman individu

Navigasikan ke **Pelanggan > Tampilan Halaman** untuk log mentah dari setiap navigasi halaman yang dilacak. Ini adalah catatan hanya baca — Anda tidak dapat menambahkan atau mengedit entri. Gunakan untuk menyelidiki sesi tertentu atau memverifikasi bahwa pelacakan merekam dengan benar.

Setiap catatan menampilkan:
- **Jalur URL** — halaman yang dikunjungi
- **Sesi** — identifikasi pendek untuk sesi pengunjung
- **Sumber** — apakah kunjungan berasal dari frontend tanpa kepala atau toko ritel standar
- **Apakah Bot** — apakah pengunjung diidentifikasi sebagai lalu lintas otomatis
- **Apakah Halaman Masuk** — apakah ini adalah halaman pertama dalam sesi mereka
- **Timestamp** — waktu persis kunjungan tersebut

Anda dapat menyaring berdasarkan **Apakah Bot**, **Sumber**, dan **Apakah Halaman Masuk** menggunakan filter di sisi kiri, dan menavigasi berdasarkan tanggal menggunakan hierarki tanggal di bagian atas.

## Membaca tren lalu lintas

Ringkasan lalu lintas harian adalah alat terbaik Anda untuk mendeteksi tren. Cari pola seperti:

- **Lonjakan lalu lintas** setelah menjalankan promosi atau mengirim email pemasaran
- **Pertumbuhan bertahap** selama minggu dan bulan saat toko Anda mendapatkan visibilitas organik
- **Pola akhir pekan vs. hari kerja** untuk memahami kapan pelanggan Anda paling aktif
- **Pembagian mobile vs. desktop** untuk memutuskan apakah harus memprioritaskan perubahan desain yang dioptimalkan untuk mobile

Kolom **Pengunjung Baru** dan **Pengunjung Kembali** bersama memberi tahu seberapa baik Anda mempertahankan pelanggan. Toko yang sehat biasanya melihat campuran keduanya — proporsi tinggi pengunjung baru menunjukkan akuisisi yang kuat, sementara proporsi pengunjung kembali yang lebih tinggi menunjukkan loyalitas pelanggan yang sedang berkembang.

Tampilan statistik per halaman, diurutkan berdasarkan jumlah tampilan secara menurun (default), langsung menunjukkan kepada Anda halaman mana yang menghasilkan lalu lintas terbanyak pada hari tertentu.

Cari tahu:

- **Halaman dengan tingkat masuk tinggi tetapi tampilan rendah** — halaman yang menarik pengunjung dari pencarian atau iklan tetapi mungkin tidak menahan perhatian
- **Halaman dengan tampilan tinggi dan banyak pengunjung unik** — halaman tujuan populer yang layak tetap diperbarui
- **Halaman produk dengan jumlah tampilan yang meningkat** — produk yang mungkin sedang meningkatkan visibilitas pencarian

### Contoh: menemukan lalu lintas produk

Untuk memeriksa seberapa banyak lalu lintas yang diterima produk terlaris Anda minggu lalu:

1. Navigasikan ke **Customers > Daily Page Stats**
2. Gunakan hierarki tanggal untuk memilih minggu yang relevan
3. Di kotak pencarian, masukkan slug URL produk (misalnya, `/blue-widget`)
4. Tinjau **Views**, **Unique Visitors**, dan **Entries** selama hari-hari yang ditampilkan

## Data lokasi pengunjung

Navigasikan ke **Customers > Visitor Locations** untuk melihat tampilan tingkat sesi di mana pengunjung Anda berada. Setiap catatan mewakili satu sesi pengunjung dan mencakup:

- Negara dan kota (diselesaikan secara otomatis oleh sistem GeoIP)
- Jenis perangkat (desktop, mobile, tablet)
- Preferensi mata uang dan bahasa yang dipilih pengunjung
- Atribusi kampanye UTM (sumber, medium, nama kampanye)
- Bendera lalu lintas bot dan admin

Anda dapat menyaring pengunjung berdasarkan negara, jenis perangkat, sumber UTM, dan apakah mereka adalah bot atau staf admin. Gunakan filter **Is Bot** yang diatur ke false untuk fokus pada lalu lintas pelanggan asli, dan filter **Is Admin Traffic** untuk mengecualikan sesi pengujian Anda sendiri dari analisis.

## Tips

- Tampilan bot dilacak secara terpisah dan secara otomatis dikecualikan dari jumlah pengunjung unik — angka lalu lintas Anda mencerminkan aktivitas pelanggan asli
- Kolom **Entries** dalam statistik per halaman memberi tahu Anda halaman mana yang bertindak sebagai pintu depan toko Anda dari pencarian dan iklan; mengoptimalkan halaman-halaman tersebut memiliki dampak terbesar
- Saring lokasi pengunjung berdasarkan **UTM Source** untuk mengukur seberapa banyak lalu lintas yang sebenarnya dikirim oleh saluran pemasaran tertentu (misalnya, sebuah surat kabar email atau iklan Google)
- Statistik harian diagregasi semalam — jika Anda perlu memeriksa lalu lintas hari yang sama, gunakan log Page Views secara langsung
- Pemecahan perangkat dalam ringkasan harian membantu Anda memprioritaskan pekerjaan desain; jika lebih dari separuh kunjungan Anda adalah dari perangkat mobile, pastikan halaman produk dan proses checkout terlihat bagus di layar kecil