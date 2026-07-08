---
title: Dasbor Toko
---

Dasbor Toko memberikan Anda pandangan lengkap mengenai kinerja toko Anda — pendapatan, pesanan, produk teratas, lalu lintas pengunjung, dan lebih banyak lagi — semuanya dalam satu tempat. Gunakan untuk memahami apa yang terjual, dari mana pelanggan Anda berasal, dan bagaimana toko Anda berperforma seiring waktu.

Navigasikan ke **Manajemen > Metrik Sistem** dan klik **Dasbor Toko** dari bilah alat.

![Gambar overview Dasbor Toko](/static/core/admin/img/help/shop-dashboard/overview.webp)

## Memilih periode waktu

Dasbor menyaring semua metrik berdasarkan periode yang dipilih. Gunakan pemilih periode di bagian atas halaman untuk memilih:

| Periode | Apa yang ditampilkan |
|--------|---------------|
| Hari ini | Hari ini vs kemarin |
| Minggu ini | Senin hingga hari ini vs minggu lalu |
| Bulan ini | Bulan ini vs bulan lalu |
| Tahun ini | Tahun ini vs periode yang sama tahun lalu |
| 30 hari terakhir | Jendela 30 hari yang berjalan |
| 90 hari terakhir | Jendela 90 hari yang berjalan |
| Kustom | Masukkan tanggal awal dan akhir tertentu |

Sebagian besar tampilan menampilkan **perbandingan** dengan periode yang sama di masa lalu, sehingga Anda dapat melihat apakah performa sedang meningkat atau menurun. Matikan sakelar **Bandingkan** jika Anda hanya ingin melihat angka saat ini.

## Kartu aksi

Di bagian atas dasbor, kartu aksi menyoroti item yang memerlukan perhatian Anda saat ini:

- **Pesanan tidak selesai** — pesanan yang menunggu penyelesaian
- **Keranjang yang ditinggalkan** — sesi di mana pelanggan menambahkan barang tetapi tidak menyelesaikan checkout
- **Pesan yang belum dibaca** — pertanyaan pelanggan yang menunggu jawaban
- **Peringatan stok rendah** — produk yang stoknya sedang menipis

Klik kartu aksi mana pun untuk langsung beralih ke bagian admin yang relevan.

## Kinerja penjualan

Bagian kinerja penjualan menampilkan angka pendapatan utama Anda untuk periode yang dipilih:

- **Total pendapatan** — penjualan kotor sebelum potongan
- **Total pesanan** — jumlah pesanan yang selesai
- **Nilai rata-rata pesanan** — pendapatan dibagi dengan jumlah pesanan
- **Laba bersih** — pendapatan dikurangi biaya barang dan biaya (jika dikonfigurasi)

Setiap angka menampilkan panah dan persentase yang menunjukkan perubahan dari periode perbandingan.

## Grafik penjualan seiring waktu

Grafik utama memplot penjualan atau pesanan Anda selama periode yang dipilih. Spwig secara otomatis memilih kelompok yang paling berguna:

- Periode pendek (hingga satu minggu) dikelompokkan berdasarkan hari
- Periode sedang (hingga tiga bulan) dikelompokkan berdasarkan minggu
- Periode panjang dikelompokkan berdasarkan bulan

Anda dapat mengganti kelompok menggunakan kontrol **Kelompok berdasarkan** di atas grafik. Sorotkan titik mana pun untuk melihat nilai tepat untuk tanggal tersebut.

## Produk teratas

Tabel produk teratas mencantumkan produk terlaris dalam periode yang dipilih, diurutkan berdasarkan pendapatan. Setiap baris menampilkan:

- **Nama produk**
- **Jumlah yang terjual**
- **Pendapatan yang dihasilkan**

Gunakan ini untuk mengidentifikasi produk terbaik Anda dan memutuskan di mana untuk fokus promosi atau restok stok.

## Analitik pengunjung

Bagian analitik pengunjung menampilkan jumlah orang yang mengunjungi toko Anda dan bagaimana mereka berperilaku:

- **Total pengunjung** — pengunjung unik ke toko Anda
- **Tampilan halaman** — total halaman yang dilihat
- **Rasio keluar** — persentase pengunjung yang hanya melihat satu halaman
- **Tampilan seiring waktu** — grafik yang menampilkan volume lalu lintas selama periode yang dipilih

Panel **Geografi** menampilkan dari mana pengunjung Anda berasal, dipecah berdasarkan negara dan (jika tersedia) kota.

## Sumber lalu lintas

Panel sumber lalu lintas menampilkan bagaimana pengunjung menemukan toko Anda:

| Sumber | Deskripsi |
|--------|-------------|
| Langsung | Pengunjung yang mengetik URL Anda atau menggunakan bookmark |
| Pencarian organik | Pengunjung dari mesin pencari |
| Sosial | Pengunjung dari platform media sosial |
| Referral | Pengunjung dari situs web lain yang mengarah ke Anda |
| Email | Pengunjung yang mengklik tautan dalam email |

Gunakan informasi ini untuk memahami saluran pemasaran mana yang menghasilkan lalu lintas terbanyak dan di mana untuk berinvestasi.

## Funnel konversi

Funnel konversi menampilkan bagaimana pengunjung berpindah dari menjelajah ke menyelesaikan pembelian:

1. **Pengunjung** — total pengunjung unik
2. **Penglihatan produk** — pengunjung yang melihat setidaknya satu produk
3. **Tambah ke keranjang** — pengunjung yang menambahkan item ke keranjang mereka
4. **Mulai proses checkout** — pengunjung yang memulai proses checkout
5. **Pesanan selesai** — pengunjung yang melakukan pemesanan

Persentase di setiap langkah menunjukkan tingkat penurunan. Penurunan besar antara "tambah ke keranjang" dan "mulai proses checkout" menunjukkan adanya hambatan dalam alur checkout Anda.

## Kinerja voucher

Jika Anda menjalankan promosi voucher, bagian ini menunjukkan bagaimana voucher tersebut berkinerja selama periode yang dipilih:

- **Total penggunaan voucher** — seberapa banyak kali voucher digunakan
- **Total diskon yang diberikan** — jumlah semua diskon voucher yang diterapkan
- **Pendapatan dengan voucher** — total pendapatan dari pesanan yang mencakup voucher

## Segmentasi pelanggan

Panel segmentasi pelanggan membagi basis pelanggan Anda menjadi kelompok-kelompok:

- **Pelanggan baru** — pembeli untuk pertama kalinya dalam periode yang dipilih
- **Pelanggan kembali** — pelanggan yang pernah melakukan pembelian sebelumnya
- **Checkout sebagai tamu** — pesanan yang ditempatkan tanpa membuat akun

Memahami rasio pelanggan baru terhadap pelanggan kembali membantu Anda memutuskan apakah harus berinvestasi lebih banyak dalam akuisisi (pemasaran) atau retensi (program loyalitas).

## Ringkasan afiliasi dan loyalitas

Jika toko Anda memiliki program afiliasi atau skema loyalitas yang aktif, metrik kinerja ringkasan muncul di sini — total komisi yang diperoleh, total poin yang diberikan, dan afiliasi atau penukar terbaik.

## Tips

- Periksa dashboard setiap pagi hari Senin untuk tinjauan mingguan yang cepat — periode "Minggu ini" memberikan gambaran jelas tentang kinerja terbaru
- Gunakan rentang tanggal **Kustom** untuk mengukur dampak kampanye tertentu: atur tanggal mulai dan akhir ke periode kampanye
- Jika funnel konversi menunjukkan penurunan besar pada **Mulai proses checkout**, pertimbangkan menyederhanakan alur checkout Anda atau menambahkan badge kepercayaan
- Jumlah keranjang yang dibatalkan tinggi bersama dengan konversi yang rendah dapat menunjukkan masalah harga atau biaya pengiriman — tinjau biaya checkout Anda
- Bandingkan periode tahun ke tahun menggunakan periode **Tahun ini** untuk memahami pola musiman dalam bisnis Anda
- Ekspor atau ambil screenshot tabel produk teratas sebelum keputusan restocking besar untuk memastikan Anda memesan jumlah yang benar