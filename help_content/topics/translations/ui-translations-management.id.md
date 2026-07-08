---
title: Manajemen Terjemahan UI
---

Halaman Terjemahan UI memungkinkan Anda untuk menyesuaikan bagaimana string antarmuka depan—tombol, label, pesan kesalahan, dan teks UI lainnya—tampil dalam setiap bahasa. Berbeda dengan terjemahan konten produk atau halaman, ini adalah elemen antarmuka tetap yang dilihat pelanggan selama berbelanja di toko Anda. Sesuaikan mereka untuk cocok dengan suara merek Anda atau meningkatkan kejelasan untuk audiens spesifik Anda.

Halaman ini menampilkan semua string UI yang dapat diterjemahkan dan memungkinkan Anda mengganti terjemahan default yang disediakan oleh Spwig.

## Memahami Terjemahan UI

Terjemahan UI adalah string teks yang menyusun antarmuka toko Anda:

**Contoh String UI**:
- Tombol: "Add to Cart", "Checkout", "Search"
- Label: "Price", "Quantity", "Shipping Address"
- Pesan: "Item added to cart", "Order confirmed", "Invalid email address"
- Navigasi: "Home", "Shop", "Contact Us"
- Bidang formulir: "Email", "Password", "First Name"

Spwig menyertakan terjemahan default untuk sekitar 300 string UI dalam semua bahasa yang didukung. Halaman Terjemahan UI memungkinkan Anda mengganti default-default ini dengan terjemahan khusus Anda sendiri.

## Mengapa Menyesuaikan Terjemahan UI?

**Suara Merek**: Ubah "Add to Cart" menjadi "Buy Now" atau "Get Yours" untuk cocok dengan kepribadian merek Anda

**Variasi Regional**: Sesuaikan terjemahan untuk pasar tertentu (British English vs American English, European Spanish vs Latin American Spanish)

**Kejelasan**: Jika terjemahan default tidak masuk akal untuk produk atau audiens Anda, ganti dengan teks yang lebih jelas

**Istilah Khusus Industri**: Gunakan istilah yang diharapkan oleh pelanggan Anda (misalnya, "Book Appointment" alih-alih "Add to Cart" untuk toko berbasis layanan)

## Mencari String

Gunakan kotak pencarian untuk menemukan string UI tertentu:

**Cari berdasarkan teks Inggris**: Ketik "add to cart" untuk menemukan terjemahan tombol tersebut

**Cari berdasarkan terjemahan**: Ketik teks dalam bahasa apa pun untuk menemukan terjemahan yang cocok

**Cari berdasarkan kunci**: Jika Anda mengetahui kunci terjemahan (misalnya, `cart.add_item`), cari langsung kuncinya

Halaman ini diperbarui secara instan saat Anda mengetik, menampilkan hanya string yang cocok.

## Melihat Detail Terjemahan

Setiap string UI menampilkan:

**Teks Sumber Inggris** - Versi Inggris default (titik acuan Anda)

**Kunci Terjemahan** - Penanda internal yang digunakan dalam kode (misalnya, `cart.add_to_cart`)

**Kolom Bahasa** - Terjemahan saat ini untuk setiap bahasa aktif

**Status Penggantian** - Apakah Anda telah menyesuaikan terjemahan (ditekankan jika diganti)

## Membuat Penggantian Terjemahan

Untuk menyesuaikan terjemahan string UI:

1. **Cari string** menggunakan pencarian (misalnya, cari "add to cart")
2. **Klik sel bahasa** yang ingin Anda sesuaikan
3. **Masukkan terjemahan khusus Anda** di editor pop-up
4. **Simpan** - Penggantian Anda langsung berlaku

Terjemahan default asli tetap dipertahankan - Anda membuat penggantian yang memiliki prioritas lebih tinggi.

## Mengembalikan ke Default

Untuk menghapus penggantian khusus dan memulihkan terjemahan default:

1. **Klik terjemahan yang diganti** (yang ditandai)
2. **Klik "Revert to Default"** di editor
3. **Konfirmasi** - Terjemahan default dipulihkan secara langsung

Anda dapat mengembalikan penggantian bahasa individual tanpa memengaruhi penggantian Anda di bahasa lain.

## Menyaring Berdasarkan Status Penggantian

Gunakan dropdown penyaring untuk melihat:

**Semua String** - Setiap string UI di sistem (~300 total)

**Hanya yang Diganti** - String di mana Anda telah membuat terjemahan khusus

**Hanya Default** - String yang masih menggunakan terjemahan default Spwig

Ini membantu Anda meninjau string yang telah Anda sesuaikan dan mengidentifikasi celah.

## Contoh Penyesuaian Umum

| Default Inggris | Penggantian Khusus | Kasus Penggunaan |
|----------------|----------------|----------|
| Add to Cart | Buy Now | Panggilan tindakan yang lebih langsung |
| Checkout | Secure Checkout | Menekankan keamanan |
| Search | Find Products | Lebih spesifik untuk e-commerce |
| Contact Us | Get in Touch | Tone yang lebih ramah |
| Subscribe | Join Our Newsletter | Penawaran nilai yang lebih jelas |

## Validasi Terjemahan

Ketika memasukkan terjemahan khusus, validasi bahwa:

**Panjang sesuai ruang UI** - Terjemahan mungkin lebih panjang/disingkat dari Inggris (kata-kata Jerman sering lebih panjang, misalnya)

**Mempertahankan makna** - Jangan mengubah fungsi dalam terjemahan (tombol "Cancel" tidak boleh mengatakan "Delete")

**Istilah yang konsisten** - Gunakan terjemahan yang sama untuk istilah yang diulang di seluruh antarmuka

**Formalitas yang tepat** - Cocokkan nada pasar target Anda (formal vs santai)

## Konsistensi Multi-Bahasa

Ketika menyesuaikan string untuk beberapa bahasa:

1. **Mulai dengan bahasa default Anda** - Tetapkan dasar
2. **Sesuaikan bahasa lainnya** untuk cocok dengan maksud yang sama
3. **Uji dalam setiap bahasa** untuk memverifikasi tata letak dan makna
4. **Gunakan penutur asli** ketika mungkin untuk meninjau penyesuaian non-Inggris

Penyesuaian yang tidak konsisten di berbagai bahasa menciptakan pengalaman pelanggan yang membingungkan.

## Ekspor/Impor Berkelompok

Untuk penyesuaian yang luas, pertimbangkan alur kerja ekspor/impor:

1. **Ekspor** terjemahan saat ini sebagai JSON atau CSV
2. **Edit dalam spreadsheet** atau editor teks (lebih mudah untuk perubahan berkelompok)
3. **Impor** terjemahan yang diperbarui kembali ke sistem

Alur kerja ini tersedia melalui halaman Pekerjaan Terjemahan untuk mengelola proyek terjemahan berskala besar.

## Tips

- **Cari sebelum menyesuaikan** - Pastikan Anda mengedit string yang benar; beberapa string serupa melayani tujuan yang berbeda
- **Uji di frontend setelah menyimpan** - Verifikasi terjemahan khusus Anda muncul dengan benar di UI aktual
- **Jaga terjemahan ringkas** - Lebih pendek biasanya lebih baik untuk tombol dan label
- **Dokumentasikan penggantian Anda** - Buat catatan mengapa Anda menyesuaikan string tertentu untuk referensi di masa depan
- **Gunakan istilah yang konsisten** - Jika Anda menyesuaikan "Cart" menjadi "Basket", lakukan secara konsisten di semua string terkait
- **Pertimbangkan tata letak mobile** - Terjemahan yang panjang mungkin membalik atau memotong di layar kecil
- **Periksa setelah pembaruan bahasa** - Ketika Spwig menambahkan terjemahan default baru, tinjau dan sesuaikan untuk mempertahankan konsistensi

Ingat: Pertahankan semua format markdown, jalur gambar, blok kode, dan istilah teknis tepat seperti yang ditunjukkan dalam aturan pelestarian.