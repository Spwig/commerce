---
title: Cấu Hình Sản Phẩm 3D
---

Cấu hình 3D cho phép khách hàng của bạn xem các sản phẩm có thể cấu hình trong trình xem 3D tương tác trực tiếp trên trang sản phẩm. Khi khách hàng chọn các tùy chọn — như màu sắc, chất liệu hoặc các biến thể thành phần — mô hình 3D sẽ được cập nhật theo thời gian thực để phản ánh lựa chọn của họ. Trên các thiết bị di động được hỗ trợ, khách hàng cũng có thể xem sản phẩm trong thực tế tăng cường (AR), đặt nó ảo trong không gian của họ trước khi mua hàng.

Cấu hình 3D hoạt động với các sản phẩm có thể cấu hình. Mỗi sản phẩm có thể cấu hình có thể có một cấu hình cảnh 3D duy nhất liên kết tệp mô hình GLB với các tùy chọn cấu hình của sản phẩm.

## Trước khi bắt đầu

Để thiết lập một cảnh 3D, bạn cần:

- Một **sản phẩm có thể cấu hình** đã được tạo trong danh mục của bạn
- Một **mô hình 3D cơ bản** được tải lên thư viện phương tiện của bạn dưới dạng tệp GLB — đây là mô hình được lắp ráp hiển thị mặc định
- Tùy chọn, các tệp GLB bổ sung cho việc thay đổi hình học (ví dụ: các hình dạng cổ tay khác nhau), và hình ảnh văn bản cho các biến thể chất liệu

Nếu bạn chưa tạo sản phẩm có thể cấu hình và các tùy chọn cấu hình của nó, hãy thực hiện điều đó trước khi thiết lập cảnh 3D.

## Tạo cấu hình cảnh

1. Di chuyển đến **Danh mục > Cấu hình Cảnh 3D**
2. Nhấp **+ Thêm Cấu hình Cảnh 3D**
3. Chọn **Sản phẩm** mà cảnh này thuộc về — chỉ các sản phẩm có thể cấu hình mới có sẵn
4. Chọn **Mô hình 3D Cơ bản** từ Thư viện Phương tiện của bạn — đây là tệp GLB được tải mặc định
5. Cấu hình cài đặt trình xem (xem bên dưới)
6. Lưu bản ghi

Sau khi lưu, trường **Cây Nút** được điền tự động. Đây là đồ thị cảnh được phân tích được trích xuất từ tệp GLB của bạn — nó liệt kê tất cả các nút được đặt tên bên trong mô hình, mà bạn sẽ tham khảo khi thêm ánh xạ nút.

## Cài đặt trình xem

Các cài đặt này kiểm soát cách trình xem 3D hiển thị trên trang sản phẩm của bạn.

### Máy ảnh và ánh sáng

| Trường | Mô tả | Mặc định |
|-------|-------------|---------|
| **Vị trí máy ảnh quay** | Vị trí máy ảnh ban đầu theo định dạng `góc độ cao khoảng cách` (ví dụ: `0deg 75deg 2m`) | `0deg 75deg 2m` |
| **Điểm máy ảnh hướng đến** | Điểm mà máy ảnh nhìn thấy, tính bằng mét từ tâm mô hình (ví dụ: `0m 0m 0m`) | `0m 0m 0m` |
| **Hình ảnh môi trường** | Một hình ảnh HDR từ Thư viện Phương tiện của bạn được sử dụng cho ánh sáng dựa trên hình ảnh — tạo phản ánh và bóng hơn thực tế | Không |
| **Độ phơi sáng** | Độ sáng tổng thể của cảnh — giá trị thấp hơn sẽ tối hơn, giá trị cao hơn sẽ sáng hơn | `1.0` |

### Bóng

| Trường | Mô tả | Mặc định |
|-------|-------------|---------|
| **Độ đậm bóng** | Độ mạnh của bóng được chiếu dưới mô hình — `0` là không bóng, `1` là độ đậm tối đa | `0.5` |
| **Độ mờ bóng** | Độ mờ của mép bóng — `0` là sắc nét, `1` là rất mờ | `0.5` |

### Phân loại màu sắc

| Trường | Mô tả |
|-------|-------------|
| **Phép ánh xạ màu sắc** | Thuật toán phân loại màu sắc được áp dụng cho cảnh. **Thương mại** tạo ra các màu sắc sôi động, thân thiện với sản phẩm. **Trung lập** là chính xác về màu sắc. **ACES** mang lại vẻ ngoài phim ảnh cinematic. |
| **Độ mạnh phát sáng** | Thêm hiệu ứng phát sáng cho các phần tự phát sáng của mô hình. `0` tắt phát sáng. Giá trị từ `1` đến `5` tạo hiệu ứng phát sáng nhẹ đến mạnh mẽ. |

### Hành vi và nền

| Trường | Mô tả | Mặc định |
|-------|-------------|---------|
| **Quay tự động** | Liệu mô hình có quay chậm khi tải để thu hút sự chú ý của khách hàng hay không | Bật |
| **Kích hoạt AR** | Liệu khách hàng trên các thiết bị được hỗ trợ có thể thấy nút **Xem trong AR** hay không | Bật |
| **Nền** | Màu nền hoặc gradient CSS của trình xem — nhập một mã màu hex (ví dụ: `#f5f5f5`) hoặc giá trị gradient CSS | `#ffffff` |

### Hình thu nhỏ

Trường **Hình thu nhỏ** lưu trữ ảnh chụp màn hình xem trước của trình xem 3D, được hiển thị trước khi trình xem được tải. Bạn có thể chụp ảnh màn hình từ trang sản phẩm trực tiếp và tải lên thư viện phương tiện của bạn, sau đó liên kết nó ở đây để có trải nghiệm tải trang mượt hơn.

## Kích hoạt và tắt trình xem 3D

Nút **Kích hoạt** kiểm soát liệu trình xem 3D có được hiển thị trên trang sản phẩm hay không.

Khi bị tắt, sản phẩm sẽ quay lại sử dụng trình cấu hình hình ảnh 2D tiêu chuẩn.

Điều này cho phép bạn chuẩn bị cấu hình cảnh trước khi hiển thị cho khách hàng.

## Kết nối các tùy chọn cấu hình với hành động 3D

Sau khi cấu hình cảnh cơ bản, bạn có thể liên kết từng tùy chọn vị trí cấu hình với sự thay đổi trực quan trên mô hình 3D. Những liên kết này được gọi là **Node Mappings** và được thêm vào phần **Node Mappings** ở phía dưới biểu mẫu cấu hình cảnh.

### Các trường Node mapping

| Trường | Mô tả |
|-------|-------------|
| **Tùy chọn vị trí** | Tùy chọn cấu hình kích hoạt thay đổi này (ví dụ: "Đen da") |
| **Loại hành động** | Sự thay đổi trực quan xảy ra (xem các loại hành động bên dưới) |
| **Node mục tiêu** | Tên của node trong cây cảnh sẽ thay đổi — chọn từ các tên được liệt kê trong **Node Tree** của bạn |
| **Dữ liệu hành động** | Dữ liệu cụ thể cho hành động như mã màu hex, URL văn bản, hoặc URL tệp GLB |
| **Thứ tự sắp xếp** | Điều khiển thứ tự mà các bản ánh xạ cho cùng một tùy chọn được áp dụng |

### Các loại hành động

| Hành động | Điều nó làm |
|--------|-------------|
| **Màu sắc vật liệu** | Thay đổi màu sắc của vật liệu trên node mục tiêu — cung cấp mã màu hex trong **Dữ liệu hành động** |
| **Văn bản vật liệu** | Thay thế văn bản được áp dụng cho vật liệu — liên kết đến tài sản hình ảnh văn bản trong **Dữ liệu hành động** |
| **Thay thế hình học** | Thay thế một phần của mô hình bằng tệp GLB khác — hữu ích cho các thay đổi cấu trúc như hình dạng tay cầm khác |
| **Tính năng hiển thị** | Hiển thị hoặc ẩn node trong cảnh — đặt `visible: true` hoặc `visible: false` trong **Dữ liệu hành động** |

Có thể thêm nhiều bản ánh xạ cho một tùy chọn vị trí. Ví dụ, việc chọn "Áo Jean Xanh" có thể thay đổi màu sắc vật liệu *và* ẩn node viền da cùng lúc.

## Tài sản hình học

Nếu cấu hình của bạn bao gồm các hành động **Thay thế hình học**, bạn cần đăng ký các tệp GLB thay thế như Tài sản Hình học. Những tài sản này được thêm vào phần **Tài sản Hình học** trong biểu mẫu cấu hình cảnh.

| Trường | Mô tả |
|-------|-------------|
| **Nhãn** | Tên mô tả cho tài sản hình học này, ví dụ: "Cổ áo V" |
| **Tệp GLB** | Tệp GLB thay thế từ Thư viện Truyền thông của bạn |
| **Node mục tiêu** | Node nào trong mô hình cơ bản mà tài sản hình học này thay thế |

Sau khi lưu Tài sản Hình học, tên node sẽ được phân tích từ tệp GLB và lưu trữ trong **Dữ liệu Node**, làm cho chúng có sẵn như các node mục tiêu trong các bản ánh xạ của bạn.

## Tài sản văn bản

Các hình ảnh văn bản được sử dụng trong các bản ánh xạ **Văn bản vật liệu** có thể được đăng ký như Tài sản Văn bản để dễ tham khảo hơn. Những tài sản này được thêm vào phần **Tài sản Văn bản**.

| Trường | Mô tả |
|-------|-------------|
| **Nhãn** | Tên mô tả, ví dụ: "Đen da" |
| **Hình ảnh văn bản** | Hình ảnh văn bản từ Thư viện Truyền thông của bạn |
| **Loại văn bản** | Kênh PBR mà văn bản này áp dụng — Màu cơ bản, Bản đồ pháp tuyến, Bản đồ độ nhám, Bản đồ kim loại, Bản đồ ánh sáng môi trường, hoặc Bản đồ phát sáng |

## Ví dụ: áo khoác có thể cấu hình với các tùy chọn màu sắc

**Tình huống:** Một chiếc áo khoác có thể đặt hàng với các màu Đen, Hải quân, hoặc Nâu rượu vang, với mỗi màu được áp dụng cho lưới cơ thể áo khoác.

**Thiết lập:**

1. Tạo cấu hình cảnh cho sản phẩm áo khoác với tệp GLB áo khoác đã lắp ráp làm mô hình cơ bản
2. Đặt **Tone Mapping** thành Commerce và **Auto Rotate** thành bật
3. Trong Node Mappings, thêm ba mục — một mục cho mỗi tùy chọn màu:

| Tùy chọn vị trí | Loại hành động | Node mục tiêu | Dữ liệu hành động |
|-------------|-------------|-------------|-------------|
| Đen | Màu sắc vật liệu | JacketBody | `{"color": "#1a1a1a"}` |
| Hải quân | Màu sắc vật liệu | JacketBody | `{"color": "#1b2a4a"}` |
| Nâu rượu vang | Màu sắc vật liệu | JacketBody | `{"color": "#6b2737"}` |

Khi khách hàng chọn màu Hải quân trên trang sản phẩm, trình xem sẽ cập nhật ngay lập tức vật liệu JacketBody thành màu hải quân.

## Một số mẹo

Giữ nguyên tất cả định dạng markdown, đường dẫn hình ảnh, khối mã và các thuật ngữ kỹ thuật.

- Đặt tên các nút GLB một cách rõ ràng khi tạo mô hình 3D của bạn — tên nút như "JacketBody" hoặc "CollarMesh" sẽ dễ sử dụng hơn rất nhiều so với tên được tạo tự động như "Mesh_023"
- Sử dụng bản ánh xạ màu sắc **Commerce** cho hầu hết các sản phẩm — nó được tối ưu hóa để trình bày sản phẩm sinh động và hấp dẫn
- Tắt tính năng **Auto Rotate** cho các sản phẩm mà góc máy mặc định đã hiển thị các tính năng quan trọng nhất, để tránh làm cho khách hàng bị mất phương hướng khi tải trang
- Kiểm tra nút AR trên thiết bị di động thực tế trước khi quảng bá nó — khả năng sử dụng AR phụ thuộc vào thiết bị và trình duyệt của khách hàng (iOS Safari và Android Chrome với hỗ trợ WebXR là đáng tin cậy nhất)
- Tải lên hình ảnh **Thumbnail** cho mỗi cấu hình cảnh — điều này ngăn chặn việc hiển thị một hộp trắng trống khi trình xem 3D đang tải
- Nếu trình xem 3D vẫn chưa sẵn sàng, hãy tắt nó bằng nút **Enabled** để khách hàng có thể xem trình cấu hình hình ảnh tiêu chuẩn thay vào đó