---
title: Yêu cầu hệ thống
---

Spwig chạy trên hầu hết các máy chủ Linux hiện đại. Trang này đề cập đến các yêu cầu tối thiểu và được khuyến nghị, điều gì xảy ra trên các máy chủ nhỏ hơn, và các nhà cung cấp dịch vụ đám mây hoạt động tốt.

## Yêu cầu tối thiểu

| Tài nguyên | Tối thiểu | Khuyến nghị |
|----------|---------|-------------|
| **Hệ điều hành** | Ubuntu 22.04 LTS, Ubuntu 24.04 LTS hoặc Debian 12 | Ubuntu 24.04 LTS |
| **RAM** | 4 GB | 8 GB hoặc nhiều hơn |
| **Không gian đĩa** | 20 GB | 40 GB hoặc nhiều hơn |
| **CPU** | 1 vCPU | 2+ vCPUs |
| **Kiến trúc** | x86_64 (AMD64) | x86_64 |
| **Mạng** | Địa chỉ IP công khai (cho chế độ độc lập) | Địa chỉ IP công khai tĩnh |
| **Cổng** | 80 và 443 (độc lập) hoặc bất kỳ cổng thay thế nào (sidecar) | 80 và 443 |

> **Lưu ý:** Các máy chủ dựa trên ARM (ví dụ: AWS Graviton, Oracle Ampere) hiện không được hỗ trợ.

## Các cấp tài nguyên

Trình cài đặt tự động phát hiện RAM khả dụng của máy chủ và chọn cấp tài nguyên phù hợp.

### Cấp tiêu chuẩn (RAM 6 GB trở lên)

Tất cả các dịch vụ chạy với đầy đủ khả năng:

- Dịch vụ **dịch thuật AI** được bật — dịch thuật mô tả sản phẩm, nội dung trang và văn bản SEO thành nhiều ngôn ngữ trực tiếp từ bảng điều khiển quản trị của bạn
- Phân bổ bộ nhớ đầy đủ cho ứng dụng, cơ sở dữ liệu và các công việc nền
- Tối ưu hóa độ song song của công việc nền theo số lượng CPU của bạn

### Cấp nhỏ (RAM 4–6 GB)

Trình cài đặt thích nghi để tiết kiệm bộ nhớ:

- Dịch vụ dịch thuật AI được **tắt** để tiết kiệm khoảng 2 GB RAM. Bạn vẫn có thể quản lý dịch thuật thủ công hoặc sử dụng các công cụ dịch thuật bên ngoài — chỉ dịch thuật AI tích hợp bị ảnh hưởng.
- Giới hạn bộ nhớ cho ứng dụng và công việc nền được giảm
- Tất cả các tính năng khác hoạt động giống như cấp tiêu chuẩn

> **Lời khuyên:** Nếu bạn bắt đầu với máy chủ nhỏ và sau đó nâng cấp lên RAM 6 GB trở lên, hãy chạy lại trình cài đặt để bật dịch vụ dịch thuật.

## Các nhà cung cấp đám mây được khuyến nghị

Spwig hoạt động trên bất kỳ máy chủ Linux nào đáp ứng yêu cầu. Các nhà cung cấp này đã được kiểm tra và cung cấp giá trị tốt:

| Nhà cung cấp | Kế hoạch được khuyến nghị | RAM | Đĩa | Chi phí ước tính |
|----------|-----------------|-----|------|-----------------|
| **DigitalOcean** | Droplet cơ bản | 4 GB | 80 GB | 24 USD/tháng |
| **Linode (Akamai)** | 4 GB chia sẻ | 4 GB | 80 GB | 24 USD/tháng |
| **Vultr** | Tính toán đám mây | 4 GB | 100 GB | 24 USD/tháng |
| **Hetzner** | CX31 | 8 GB | 80 GB | 8 EUR/tháng |
| **OVH** | VPS khởi đầu | 4 GB | 80 GB | 7 EUR/tháng |

Đối với các cửa hàng dự kiến lượng truy cập lớn hoặc danh mục sản phẩm lớn (10.000+ sản phẩm), hãy bắt đầu với 8 GB RAM và 2+ vCPUs.

## Sử dụng không gian đĩa

Một lần cài đặt Spwig mới sử dụng khoảng 8 GB không gian đĩa:

| Thành phần | Kích thước |
|-----------|------|
| Hình ảnh Docker | ~4 GB |
| Cơ sở dữ liệu (cửa hàng trống) | ~200 MB |
| Mô hình dịch thuật AI (nếu được bật) | ~2 GB |
| Tệp ứng dụng và cấu hình | ~500 MB |
| Hệ điều hành và động cơ Docker | ~3 GB |

Lên kế hoạch thêm không gian cho:

- **Hình ảnh sản phẩm và phương tiện** — phụ thuộc vào kích thước danh mục của bạn. Dự trù 1–5 GB cho một cửa hàng điển hình với hàng trăm sản phẩm.
- **Tăng trưởng cơ sở dữ liệu** — tăng theo đơn hàng, khách hàng và dữ liệu phân tích. Một cửa hàng xử lý 100 đơn hàng mỗi ngày thường tăng khoảng 1 GB mỗi năm.
- **Sao lưu** — nếu lưu trữ sao lưu cục bộ, mỗi bản sao lưu đầy đủ có kích thước gần bằng kích thước cơ sở dữ liệu của bạn cộng với phương tiện. Với chính sách lưu trữ 30 ngày, dự trù 2–3× kích thước dữ liệu hiện tại của bạn.

## Tên miền và DNS

Tên miền là tùy chọn trong quá trình cài đặt nhưng cần thiết cho việc sử dụng sản xuất. Bạn cần:

- Một tên miền hoặc tên miền con (ví dụ: `shop.example.com`)
- Một **ký bản ghi A** chỉ đến địa chỉ IP công khai của máy chủ bạn
- Hoàn tất việc lan truyền DNS (thường mất 5–60 phút sau khi thêm bản ghi)

Trình cài đặt tự động nhận một chứng chỉ SSL miễn phí từ Let's Encrypt khi phát hiện tên miền hợp lệ. Bạn cũng có thể thêm tên miền sau khi cài đặt bằng cách sử dụng kịch bản `./configure-domain.sh`.

## Tường lửa

Nếu máy chủ của bạn có tường lửa (hầu hết nhà cung cấp đám mây bật nó mặc định), hãy đảm bảo các cổng sau được mở:

| Cổng | Giao thức | Mục đích |
|------|----------|---------|
| **22** | TCP | Truy cập SSH (để bạn quản lý máy chủ) |
| **80** | TCP | HTTP (yêu cầu để xác minh chứng chỉ Let's Encrypt) |
| **443** | TCP | HTTPS (giao thông an toàn của cửa hàng bạn) |

Trong chế độ sidecar, hãy mở cổng thay thế mà trình cài đặt chỉ định thay vì 80/443.

## Yêu cầu phần mềm

Trình cài đặt xử lý tự động tất cả việc cài đặt phần mềm. Để tham khảo, đây là các thành phần mà nó cài đặt hoặc kiểm tra:

- **Docker Engine** — runtime container (sẽ được cài đặt tự động nếu thiếu)
- **Docker Compose** — điều phối dịch vụ (được bao gồm trong Docker Engine)
- **curl** — được trình cài đặt sử dụng (có mặt trên hầu hết các hệ thống Linux)

Không phần mềm nào khác cần được cài đặt trước. Spwig không yêu cầu bạn cài đặt Python, Node.js, PostgreSQL, Redis hoặc Nginx thủ công — mọi thứ đều chạy bên trong các container Docker.