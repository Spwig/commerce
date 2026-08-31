---
title: Tag Pelanggan Berlangganan
---

Tag adalah label Anda sendiri untuk mengatur audiens Campaign Studio Anda — penanda singkat seperti `VIP`, `wholesale`, atau `event-2026` yang Anda definisikan dan terapkan pada pelanggan berlangganan mana pun yang sesuai. Setelah sebuah tag ada, Anda dapat memfilter daftar Pelanggan Berlangganan Anda berdasarkan tag tersebut, menerapkannya atau menghapusnya dari sejumlah orang sekaligus, dan — yang paling berguna — menggunakannya sebagai kondisi saat membangun Segmen, sehingga kampanye dan perjalanan Anda dapat menargetkan tepat orang-orang yang telah Anda beri tag.

## Apa itu tag

Tag hanyalah nama yang Anda pilih. Spwig tidak memiliki tag bawaan, dan tidak pernah menerapkannya secara otomatis — Anda yang menentukan namanya dan siapa yang menerimanya. Hal ini menjadikannya cocok untuk apa pun yang spesifik untuk bisnis Anda sendiri yang tidak sesuai dengan status yang sudah dilacak oleh Spwig: tingkat loyalitas, akun grosir, semua orang yang mendaftar di pameran dagang, atau daftar acara sekali seperti `event-2026`.

Setiap tag juga memiliki **Slug** — versi nama yang disederhanakan dan aman untuk URL — yang dihasilkan secara otomatis saat Anda membuatnya. Segmen dan filter menggunakan slug secara internal; sebagai pedagang, Anda hampir tidak akan pernah perlu melihatnya.

## Membuat tag

Tag memiliki bagian admin sendiri. Buka **Campaign Studio > Subscribers**, lalu klik **Campaign Studio** di bagian atas halaman untuk melihat daftar lengkap bagian Campaign Studio, dan pilih **Subscriber tags**.

1. Klik **Add subscriber tag**.
2. Masukkan **Name** — singkat dan spesifik paling mudah dibaca, misalnya `VIP`, `Wholesale`, atau `Event 2026`.
3. Spwig mengisi **Slug** yang sesuai saat Anda mengetik. Anda dapat membiarkannya seperti yang dihasilkan.
4. Field **Colour** opsional juga tersedia jika Anda ingin mencatat warna hex (misalnya `#2563eb`) terhadap tag untuk referensi Anda sendiri.
5. Klik **Save**.

Anda juga tidak perlu meninggalkan apa yang sedang Anda lakukan untuk membuatnya — tanda **+** hijau di samping field **Tags** di halaman edit pelanggan berlangganan mana pun membuka formulir "tambah tag" yang sama dalam popup. Dan jika Anda mencoba memberi tag pelanggan berlangganan secara massal sebelum Anda membuat tag apa pun, pemilih tag menawarkan pintasan **Create a tag** yang langsung membawa Anda ke sana.

## Memberi tag pelanggan berlangganan

Cara paling umum untuk menerapkan tag adalah secara massal, dari daftar Pelanggan Berlangganan:

1. Buka **Campaign Studio > Subscribers**.
2. Centang kotak centang pada setiap pelanggan berlangganan yang ingin Anda beri tag (atau **Select all on this page**).
3. Dari dropdown **Bulk actions**, pilih **Add tag to selected…** (atau **Remove tag from selected…** untuk menghapus tag orang-orang).
4. Klik **Go**.
5. Pilih tag dari daftar dan klik **Add tag** (atau **Remove tag**).

![Pemilih tag massal setelah memilih "Add tag to selected…" untuk empat pelanggan berlangganan](/static/core/admin/img/help/subscriber-tags/bulk-tag-picker.webp)

Setelah diterapkan, tag muncul sebagai chip kecil di kartu pelanggan berlangganan dalam daftar, di samping lencana status dan sumber mereka. Filter **Tag** juga muncul di panel filter daftar Pelanggan Berlangganan setelah Anda memiliki setidaknya satu tag, sehingga Anda dapat menyempitkan daftar menjadi semua orang yang memiliki tag tertentu — berguna untuk memeriksa siapa yang ada dalam audiens sebelum Anda membangun kampanye di sekitarnya.

![Daftar Pelanggan Berlangganan yang difilter ke tag VIP, dengan tombol Import CSV dan chip tag terlihat](/static/core/admin/img/help/subscriber-tags/subscriber-list-tag-chips.webp)

Anda juga dapat menambahkan atau menghapus tag pelanggan berlangganan tunggal langsung dari halaman edit mereka sendiri, menggunakan field **Tags** yang sama yang dikelola oleh tindakan massal.

## Menggunakan tag dalam segmen

Segmen adalah audiens berbasis aturan yang disimpan yang Anda arahkan ke kampanye dan perjalanan. Setelah Anda membuat setidaknya satu tag, kondisi **Has tag** menjadi tersedia dalam pembangun aturan segmen — itu tidak muncul pada instalasi baru tanpa tag yang didefinisikan, sehingga Anda tidak akan melihat opsi mati sebelum berguna bagi Anda.

Untuk menggunakannya, buka **Campaign Studio > Segments**, tambahkan (atau edit) segmen dinamis, dan klik **+ Add condition**:

1. Atur field kondisi ke **Has tag**.
2. Pilih operator — **is** untuk satu tag, atau **is any of** jika Anda lebih suka merumuskannya dengan cara itu.
3. Pilih tag dari dropdown.

[![Kondisi 'Memiliki tag' diatur ke VIP, menunjukkan jumlah peserta yang sesuai secara langsung](/static/core/admin/img/help/subscriber-tags/segment-has-tag-rule.webp)](https://spwig.com)

Jumlah di sudut kanan atas akan diperbarui saat Anda membuat aturan, sehingga Anda dapat melihat secara tepat berapa jumlah peserta yang saat ini memenuhi syarat sebelum Anda menyimpannya. Setiap kondisi **Memiliki tag** saat ini hanya cocok dengan satu tag sekaligus — jika Anda ingin audiens yang cocok dengan *salah satu* beberapa tag (misalnya, `VIP` atau `Eceran`), tambahkan satu kondisi **Memiliki tag** per tag dan atur **Pencocokan** menjadi **apa saja**.

Inilah yang membuat tag berguna di luar organisasi: sebuah segmen yang dibangun dengan **Memiliki tag** menjadi audiens yang dapat Anda pilih sebagai **Segmen** pada sebuah siaran atau kampanye berulang, atau sebagai pengaturan **Hanya untuk segmen** dalam perjalanan — jadi, "semua yang memiliki tag VIP" dapat memiliki rangkaian selamat datang sendiri, surat kabar berulang sendiri, atau hanya saja siapa yang Anda pilih kali berikutnya saat Anda mengirim pengumuman satu kali.

## Tips

- Pertahankan nama tag singkat dan spesifik — mereka muncul sebagai chip kecil pada kartu peserta, jadi `VIP` lebih baik daripada `Sangat Penting - Tingkat 1`.
- Gunakan filter **Tag** untuk memeriksa kembali siapa yang sebenarnya memiliki tag sebelum Anda membuat segmen atau mengirim kampanye di sekitarnya.
- Penambahan tag bersifat kumulatif — menghapus sebuah tag dari seorang peserta tidak pernah memengaruhi tag lain yang dimilikinya, dan tidak pernah menyentuh status, sumber, atau persetujuannya.
- Gabungkan tag dengan kondisi-kondisi lain dari pembuat aturan (seperti **Telah mengizinkan pemasaran** atau **Total pengeluaran**) pada segmen yang sama untuk audiens yang lebih tepat, bukan hanya sekadar sebuah tag sendiri-sendirian.
- Seorang peserta dapat membawa sebanyak-banyaknya tag yang Anda inginkan — tidak ada batasan, jadi Anda dapat menggunakan tag untuk beberapa tujuan yang tumpang tindih (tier loyalitas *dan* daftar acara *dan* catatan sumber).
- Jika sebuah tag sudah tidak lagi berguna, menghapusnya dari **Tag peserta** akan menghapusnya dari setiap peserta yang pernah menerimanya dan dari aturan segmen mana pun yang merujuk padanya — segmen yang menggunakan tag tersebut akan berhenti mencocokkan pada kondisi tersebut.

Simpan semua format markdown, jalur gambar, blok kode, dan istilah teknis.