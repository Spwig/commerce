---
title: Layanan Terhosting Spwig
---

Spwig menyertakan tiga layanan cloud opsional yang dapat digunakan toko Anda tanpa perlu Anda mengonfigurasikan atau menghosting apa pun sendiri: **GeoIP** mendeteksi di mana pengunjung Anda berada, **Geocoder** mengubah alamat pelanggan menjadi koordinat peta, dan **Push** mengirimkan notifikasi instan ke aplikasi admin Spwig mobile Anda. Pada edisi Community (gratis), setiap layanan dilengkapi dengan kuota bulanan yang cukup besar. Ketika layanan mana pun mendekati batasnya, Spwig akan memperingatkan Anda di admin agar Anda dapat memutuskan apakah akan melakukan upgrade sebelum pelanggan Anda menyadarinya.

## Ketiga layanan terhosting

### GeoIP — deteksi negara pengunjung

GeoIP mencari tahu negara setiap pengunjung berdasarkan alamat IP mereka. Toko Anda menggunakan informasi ini untuk secara otomatis menampilkan mata uang yang tepat ketika seorang pelanggan tiba, dan untuk mengisi ulang bidang negara selama proses checkout. Misalnya, pengunjung dari Jerman akan melihat harga dalam euro, dan pengunjung dari Jepang akan melihat harga dalam yen — tanpa perlu memilih secara manual.

Setiap halaman yang dimuat di mana GeoIP melakukan pencarian dihitung sebagai bagian dari kuota bulanan Anda. Pengunjung ulang dari sesi browser yang sama tidak mengonsumsi pencarian setiap kali; hasilnya dikacaukan untuk sesi tersebut. Pencarian GeoIP hanya terjadi di toko, bukan di panel admin Anda.

### Geocoder — alamat ke koordinat

Geocoder menerjemahkan alamat yang diketik oleh pelanggan menjadi koordinat geografis (latitude dan longitude). Toko Anda menggunakan koordinat ini untuk dua tujuan: menghitung biaya pengiriman berbasis jarak ketika Anda memiliki titik pengambilan atau aturan pengiriman berbasis jari, dan memungkinkan saran otomatis alamat pada halaman checkout sehingga pelanggan dapat menemukan alamat mereka dengan cepat.

Pencarian geocoder dipicu ketika pelanggan memilih atau mengonfirmasi alamat selama checkout. Seperti GeoIP, hasilnya dikacaukan sehingga alamat yang sama hanya dicari sekali per sesi.

### Push — notifikasi aplikasi admin

Push mengirimkan notifikasi real-time ke aplikasi mobile merchant Spwig Anda. Ketika pesanan baru tiba, ketika stok turun di bawah ambang batas, atau ketika pelanggan mengirimkan pesan, Push mengirimkan notifikasi instan ke perangkat Anda sehingga Anda dapat merespons tanpa perlu terus membuka panel admin.

Setiap notifikasi yang dikirim ke perangkat Anda dihitung sebagai satu permintaan push terhadap kuota bulanan Anda.

## Tier gratis Community

Pada edisi Community Spwig, setiap layanan disertakan tanpa biaya hingga batas permintaan bulanan. Batas yang tepat ditetapkan oleh Spwig dan dapat bervariasi; dashboard admin Anda selalu menampilkan angka saat ini untuk instalasi Anda. Rencana berbayar (Starter, Growth, Pro, Pro Plus) dan instalasi self-hosted dengan lisensi berbayar memiliki batas yang lebih tinggi untuk setiap layanan.

Ketika layanan mencapai 100% dari kuota Community, permintaan ke layanan tersebut dihentikan hingga bulan kalender berikutnya mengatur ulang penghitungan. Dampaknya tergantung pada layanan yang terkena:

| Layanan | Yang terjadi pada 100% |
|---------|----------------------|
| GeoIP | Deteksi otomatis mata uang kembali ke mata uang default toko Anda. Pelanggan masih dapat mengubah mata uang secara manual. |
| Geocoder | Saran otomatis alamat berhenti menawarkan saran. Pelanggan masih dapat mengetik alamat mereka secara manual. Perhitungan biaya pengiriman tetap menggunakan koordinat terakhir yang diketahui. |
| Push | Notifikasi baru ke aplikasi admin dikirimkan tetapi tidak terkirim hingga bulan berikutnya atau upgrade. |

Toko Anda tetap beroperasi secara normal dalam semua kasus — tidak ada pesanan yang hilang dan pelanggan masih dapat menyelesaikan pembelian. Efeknya terbatas pada fitur kenyamanan.

## Membaca tile dashboard

Tile **Penggunaan layanan Spwig** muncul di halaman utama dashboard admin Anda. Ini menampilkan bar progres untuk setiap dari tiga layanan.

Setiap baris dalam tile mengikuti tata letak yang sama:

- **Nama layanan** (kiri) — GeoIP, Pencarian alamat (Geocoder), atau Notifikasi push.
- **Bar progres** (tengah) — terisi dari kiri ke kanan seiring peningkatan penggunaan.

Warna dari bar berubah seiring mendekatnya batas:
  - **Hijau** — penggunaan di bawah 80%.

Semua berjalan dengan normal.
  - **Amber** — penggunaan berada antara 80% hingga 99%.

Layanan masih berjalan tetapi mendekati batas.
  - **Merah** — penggunaan telah mencapai 100%.

Layanan kini dibatasi untuk bulan ini.
- **Jumlah penggunaan** (kanan) — jumlah persis permintaan yang digunakan dari total yang diperbolehkan, misalnya `3.241 / 10.000`.

Label dalam tanda kurung menunjukkan jendela waktu, biasanya `(bulan ini)`.

Jika tile tidak dapat menghubungi server pembaruan Spwig untuk mengambil penggunaan saat ini (misalnya, jika server Anda tidak memiliki akses internet keluar), kolom jumlah menampilkan tanda hubung (`—`) untuk layanan tersebut. Ini tidak berarti layanan rusak; ini berarti tampilan penggunaan sementara tidak tersedia.

### Tombol Upgrade

Ketika layanan apa pun mencapai 80% atau lebih, tombol **Upgrade** muncul di sudut kanan atas tile. Klik tombol tersebut akan membuka halaman upgrade Spwig di mana Anda dapat membandingkan rencana dan meningkatkan batas layanan Anda. Tombol ini akan hilang ketika penggunaan kembali di bawah 80% di awal bulan berikutnya.

## Banner peringatan kuota

Selain tile dashboard, sebuah banner muncul di bagian atas setiap halaman admin ketika layanan apa pun melewati ambang batas 80%. Banner hanya muncul pada instalasi Community.

**Banner Amber — mendekati batas (80–99%)**

> **Mendekati batas layanan berbasis cloud:** Salah satu layanan Spwig Anda melebihi 80% dari kuota tier Community Anda. Upgrade untuk meningkatkan batas sebelum mencapai batas tersebut.

Banner ini adalah peringatan awal. Layanan Anda masih berjalan, dan Anda masih punya waktu untuk memutuskan apakah akan melakukan upgrade sebelum akhir bulan.

**Banner Merah — batas tercapai (100%)**

> **Batas layanan Spwig tercapai:** Salah satu layanan berbasis cloud Anda telah mencapai kuota tier Community. Upgrade untuk menjaga layanan tetap berjalan tanpa gangguan.

Banner ini muncul ketika setidaknya satu layanan mencapai 100% dan kini dibatasi. Klik tombol **Upgrade** pada banner mana pun akan membuka halaman upgrade yang sama dengan tombol tile.

Banner akan hilang secara otomatis di awal bulan kalender berikutnya ketika penghitungnya direset, atau segera setelah Anda melakukan upgrade ke rencana berbayar.

## Peringatan email pada 90%

Ketika layanan apa pun melewati 90% dari kuotanya, Spwig juga mengirimkan email peringatan sekali saja ke alamat yang dikonfigurasikan di pengaturan toko Anda (**Pengaturan > Pengaturan Toko > Kontak > Email Admin**). Email dikirim paling banyak sekali per layanan per bulan kalender, sehingga Anda tidak akan terkena banjir pesan. Tidak ada email yang dikirim pada 100% karena pada titik tersebut banner di dalam admin sudah menjelaskan situasi dengan jelas.

Jika Anda tidak menerima email, periksa apakah alamat email admin Anda telah diatur dengan benar di bawah **Pengaturan > Pengaturan Toko**.

## Memperbarui rencana Anda

Ketika Anda melakukan upgrade dari Community ke rencana berbayar apa pun, batas yang lebih tinggi langsung berlaku — tidak diperlukan restart toko atau perubahan konfigurasi. Tile dashboard akan menampilkan batas baru yang lebih tinggi pada waktu berikutnya tile diperbarui (dalam lima menit).

Untuk melakukan upgrade, klik tombol **Upgrade** pada tile dashboard atau banner kuota, atau kunjungi halaman upgrade Spwig secara langsung. Rencana berbayar mencakup tiga layanan berbasis cloud yang sama (GeoIP, Geocoder, Push) dengan batas bulanan yang lebih tinggi, serta akses ke pengiriman email yang dihosting Spwig dan dukungan prioritas.

## Self-hosting dan lisensi Pro

Jika Anda menjalankan instalasi Spwig self-hosted dengan lisensi berbayar, tier lisensi Anda menentukan batas layanan Anda, sama seperti rencana berbasis cloud yang setara. Toko Anda tetap membutuhkan akses internet keluar untuk menghubungi `updates.spwig.com` agar platform dapat mengambil dan memverifikasi konfigurasi tier Anda. Penghitung penggunaan yang ditampilkan di tile dashboard diambil dari akhir titik layanan berbasis cloud di `geoip.spwig.com`, `geocoder.spwig.com`, dan `push.spwig.com`.

Saat ini tidak ada opsi untuk mengganti GeoIP, Geocoder, atau Push dengan alternatif self-hosted — layanan ini hanya disediakan oleh infrastruktur Spwig dan termasuk dalam semua edisi.

## Tips

Jaga semua format markdown, jalur gambar, blok kode, dan istilah teknis.


- **Periksa tile secara teratur di akhir bulan yang sibuk** — acara penjualan atau promosi dapat meningkatkan secara signifikan jumlah pencarian GeoIP dan Geocoder.

Tile memberi Anda pemberitahuan sebelum pelanggan terdampak.
- **Fallback mata uang tidak terlihat oleh sebagian besar pelanggan** — jika GeoIP mencapai batasnya, pelanggan akan melihat mata uang default toko Anda.

Ini jarang menjadi masalah serius untuk toko yang utamanya melayani satu pasar; hal ini lebih penting untuk toko yang benar-benar internasional.
- **Pengisian alamat otomatis adalah kemudahan, bukan penghalang** — ketika Geocoder dibatasi, pelanggan masih dapat mengetik dan mengirim alamat mereka secara normal.

Jika Anda mengadakan promosi yang sering dan meningkatkan lalu lintas checkout, pertimbangkan untuk meningkatkan sebelum periode sibuk.
- **Pembatasan push tidak menyebabkan kehilangan notifikasi secara permanen** — notifikasi yang dikirim selama periode pembatasan tidak dikirim ulang secara retroaktif saat bulan berubah atau setelah upgrade.

Jika Anda sangat bergantung pada push untuk notifikasi pesanan yang bersifat waktu-sensitive, meningkatkan sebelum batas tercapai memastikan Anda tidak melewatkan apa pun.
- **Cache 5 menit berarti tile tidak sepenuhnya real-time** — angka penggunaan diperbarui sekitar setiap lima menit di latar belakang.

Selama periode lalu lintas yang tidak biasa tinggi, penggunaan aktual mungkin sedikit lebih tinggi dari yang ditampilkan oleh tile.
- **Atur alamat email admin Anda** — email peringatan 90% hanya berfungsi jika **Pengaturan > Pengaturan Toko > Email Admin** diisi.

Sebaiknya memastikan ini diatur dengan benar agar Anda mendapatkan peringatan sebelum masalah terjadi.