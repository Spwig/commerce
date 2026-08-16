---
title: Inventaris & Gudang
---

Sistem gudang memungkinkan Anda mengelola inventaris di berbagai lokasi, menetapkan prioritas penyelesaian pesanan, dan melacak tingkat stok secara real-time. Navigasi ke **Produk > Gudang** di sidebar admin untuk mengelola lokasi gudang Anda.

![Daftar Gudang](/static/core/admin/img/help/inventory-warehouses/warehouse-list.webp)

## Gudang

### Daftar Gudang

Halaman gudang menampilkan semua lokasi inventaris Anda dalam bentuk kartu dengan:

- **Nama dan kode** — Identifikasi gudang (misalnya, "Gudang Utama", kode "MAIN-WH")
- **Wilayah Penjualan** — Penugasan wilayah geografis
- **Badges Status** — Aktif/tidak aktif, lokasi ritel
- **Statistik** — Produk yang tersedia, prioritas penyelesaian, persentase buffer stok
- **Lokasi** — Kota dan negara
- **Terakhir Diperbarui** — Kapan tingkat stok terakhir kali diperbarui

### Membuat Gudang

1. Klik **+ Tambah Gudang**
2. Isi bagian **Informasi Dasar**:
   - **Nama** — Label deskriptif (misalnya, "Gudang Timur AS")
   - **Kode** — Identifikasi unik singkat (misalnya, "US-EAST") — harus unik di seluruh gudang
   - **Wilayah Penjualan** — Tetapkan ke wilayah geografis untuk pengiriman
   - **Aktif** — Aktifkan untuk termasuk dalam penyelesaian pesanan
3. Isi bagian **Alamat** dengan alamat lengkap gudang
4. Konfigurasikan **Pengaturan Penyelesaian**:
   - **Prioritas Penyelesaian** — Angka yang lebih tinggi = prioritas lebih tinggi untuk penyelesaian pesanan
   - **Persentase Buffer Stok** — Persentase stok yang disisihkan sebagai buffer keselamatan (0–100)
   - **Lokasi Pengiriman** — Secara opsional hubungkan ke lokasi pengambilan jika gudang ini mendukung pengambilan oleh pelanggan
5. Konfigurasikan **Tampilan Pelanggan** (opsional):
   - **Nama Tampilan** — Label yang terlihat pelanggan (misalnya, "Dikirim dari Australia"). Biarkan kosong untuk menggunakan nama gudang.
   - **Tampilkan di Frontend** — Tampilkan asal gudang ini kepada pelanggan di halaman produk
6. Konfigurasikan **POS / Toko Ritel** (opsional):
   - **Lokasi Ritel** — Centang jika gudang ini juga berfungsi sebagai toko fisik dengan terminal POS
   - **Nama Tampilan POS** —Nama singkat yang ditampilkan di antarmuka POS
   - **Kelompok Toko** — Tetapkan ke kelompok toko POS untuk pewarisan pengaturan
7. Tambahkan **Informasi Kontak** jika diperlukan (nama, email, telepon)
8. Klik **Simpan"

### Prioritas Penyelesaian

Ketika pesanan masuk, sistem memilih gudang terbaik berdasarkan:

1. **Nilai Prioritas** — Gudang dengan prioritas yang lebih tinggi dipilih
2. **Ketersediaan Stok** — Harus memiliki stok yang cukup
3. **Pemetaan Wilayah** — Gudang di wilayah pelanggan lebih disukai

Contoh, jika Anda memiliki gudang AS (prioritas 100) dan gudang Eropa (prioritas 60), pesanan AS akan dipenuhi dari gudang AS terlebih dahulu.

### Buffer Stok

Buffer stok menyisihkan persentase inventaris yang tidak akan dijual secara online. Ini berguna untuk:

- Toko ritel fisik yang membutuhkan stok di lantai
- Stok keselamatan untuk mencegah penjualan berlebihan
- Inventaris yang disiapkan untuk pesanan eceran

Buffer 10% pada 100 unit berarti hanya 90 unit yang tersedia untuk pesanan online.

## Item Stok

Item stok merepresentasikan inventaris nyata dari produk tertentu di gudang tertentu.

### Melihat Tingkat Stok

1. Klik ikon **stok** pada setiap kartu gudang untuk melihat item stoknya
2. Atau navigasi ke tab **Inventaris** dari produk untuk melihat stok di seluruh gudang

Setiap item stok menunjukkan:

- **Nama Produk** dan variasi (jika berlaku)
- **Tersedia** — Total inventaris fisik
- **Dialokasikan** — Jumlah yang disisihkan untuk pesanan yang tertunda
- **Tersedia** — Tersedia dikurangi dialokasikan (apa yang bisa dijual)

### Menambah Stok

1. Navigasi ke **Produk > Item Stok** dan klik **+ Tambah Item Stok**, atau
2. Buka formulir edit produk dan gunakan bagian **Item Stok** secara langsung di bagian bawah
3. Pilih **produk** dan **gudang** (dan secara opsional **varian** untuk produk yang memiliki variasi)
4. Masukkan jumlah **Tersedia**
5. Tetapkan **batas stok rendah** — ambang batas ini untuk setiap item memicu peringatan stok rendah
6. Simpan

### Pergerakan Stok

Setiap perubahan pada inventaris dicatat sebagai **pergerakan stok**:

{"| Movement Type | Description |\n|--------------|-------------|\n| **Receipt** | Penambahan stok yang diterima dari pemasok |\n| **Sale** | Stok dikurangi untuk pesanan yang selesai |\n| **Return** | Stok dikembalikan dari pelanggan |\n| **Adjustment** | Koreksi manual (ketidaksesuaian jumlah) |\n| **Transfer** | Dipindahkan antar gudang |\n| **Reservation** | Ditahan sementara untuk keranjang belanja yang aktif |\n| **Damage** | Dikurangi karena rusak atau hilang |\n| **Recount** | Diperbaiki agar sesuai dengan jumlah stok fisik |\n\n| Movement Type | Description |\n|--------------|-------------|\n| **Receipt** | New stock received from supplier |\n| **Sale** | Stock deducted for a fulfilled order |\n| **Return** | Stock returned from a customer |\n| **Adjustment** | Manual correction (count discrepancy) |\n| **Transfer** | Moved between warehouses |\n| **Reservation** | Temporarily held for an active cart |\n| **Damage** | Written off as damaged or lost |\n| **Recount** | Corrected to match a physical stock count |\n\nStock movements provide a complete audit trail of inventory changes. Beyond the **Adjust stock levels** action, Spwig also offers bulk actions on the Stock Items list to transfer, write off, and recount stock across many items at once — see [Bulk Stock Actions](/help/stock-bulk-actions).\n\n## Inventory Tracking on Products\n\n### Enabling inventory tracking\n\nOn a product's **Inventory** section:\n\n1. Toggle **Track Inventory** to enable stock management for this product\n2. Set the **Low Stock Threshold** — triggers dashboard alerts when stock at any warehouse falls below this level\n3. Configure **Allow Backorders** if you want to accept orders when out of stock\n4. Optionally set an **Out of Stock Action** to override the site-wide or category behavior for this specific product\n\nAfter enabling tracking, manage actual stock quantities using the **Stock Items** inline section at the bottom of the product form, or through **Products > Stock Items**.\n\n### Multi-Warehouse Stock\n\nWhen inventory tracking is enabled, the Inventory tab shows stock levels across all warehouses in a summary table:\n\n- Total on hand across all locations\n- Per-warehouse breakdown\n- Available quantities after reservations and allocations\n\n## Low Stock Alerts\n\nThe system automatically monitors stock levels and alerts you when:\n- A product falls below its **low stock threshold**\n- A product reaches **zero available stock**\n\nLow stock alerts appear on:\n- The **Shop Dashboard** in the Actions Required section\n- The product list with a visual indicator\n\n## Tips\n\n- Start with a single warehouse and add more as your business grows.\n- Set fulfillment priorities based on shipping speed and cost to each region.\n- Use stock buffers for retail locations to ensure floor stock availability.\n- Review stock movements regularly to identify shrinkage or discrepancies.\n- Set low stock thresholds based on your reorder lead time — if it takes 2 weeks to restock, set the threshold to cover 2 weeks of sales.\n- Enable inventory tracking before going live to avoid overselling."