---
title: Nhãn Người đăng ký
---

Các nhãn là các nhãn do bạn tự đặt để tổ chức danh sách người đăng ký của bạn trong Studio Chiến dịch — các ghi chú ngắn như `VIP`, `bán buôn`, hoặc `sự kiện-2026` mà bạn xác định và áp dụng cho bất kỳ người đăng ký nào phù hợp. Một khi một nhãn tồn tại, bạn có thể lọc danh sách Người đăng ký của mình theo nhãn đó, áp dụng hoặc xóa nhãn đó khỏi bất kỳ số lượng người nào cùng lúc, và — hữu ích nhất — sử dụng nó như một điều kiện khi xây dựng một Nhóm, để các chiến dịch và hành trình của bạn có thể nhắm đúng những người bạn đã đánh dấu.

## Nhãn là gì

Một nhãn đơn giản chỉ là một tên bạn chọn. Spwig không có sẵn bất kỳ nhãn nào, và nó bao giờ cũng áp dụng nhãn một cách tự động — bạn quyết định chúng được gọi là gì và ai được nhận chúng. Điều này khiến chúng phù hợp với mọi thứ cụ thể cho chính doanh nghiệp của bạn mà không cần phải khớp với một trạng thái mà Spwig đã theo dõi: một cấp độ trung thành, một tài khoản bán buôn, tất cả những người đã đăng ký tại hội chợ thương mại, hoặc một danh sách sự kiện một lần duy nhất như `sự kiện-2026`.

Mỗi nhãn cũng sẽ có một **Slug** — phiên bản đơn giản, an toàn cho URL của tên nhãn — được tạo tự động khi bạn tạo nhãn. Các đoạn hội thoại và bộ lọc sử dụng slug nội bộ; với tư cách là người bán hàng, bạn gần như không bao giờ cần xem xét nó.

## Tạo nhãn

Các nhãn có phần quản trị riêng. Mở **Studio Chiến dịch > Người đăng ký**, sau đó nhấp vào **Studio Chiến dịch** ở đầu trang để xem danh sách đầy đủ các phần của Studio Chiến dịch, và chọn **Nhãn Người đăng ký**.

1. Nhấp vào **Thêm nhãn người đăng ký**.
2. Nhập một **Tên** — đọc tốt nhất là ngắn và cụ thể, ví dụ: `VIP`, `Bán buôn`, hoặc `Sự kiện 2026`.
3. Spwig điền vào slug tương ứng khi bạn gõ. Bạn có thể để nguyên như được tạo.
4. Một trường **Màu sắc** tùy chọn cũng có sẵn nếu bạn muốn ghi nhận một mã màu hex (ví dụ: `#2563eb`) cho nhãn để tham khảo của riêng bạn.
5. Nhấp vào **Lưu**.

Bạn không cần phải rời khỏi công việc đang làm để tạo một nhãn, cả hai — một nút **+** màu xanh lá bên cạnh trường **Nhãn** trên trang chỉnh sửa của bất kỳ người đăng ký nào cũng mở ra cùng một biểu mẫu "Thêm nhãn" trong một khung bật lên. Và nếu bạn cố gắng gán nhãn hàng loạt người đăng ký trước khi bạn tạo bất kỳ nhãn nào, trình chọn nhãn sẽ cung cấp một nút **Tạo nhãn** để đưa bạn trực tiếp đến đó.

## Gán nhãn cho người đăng ký

Cách phổ biến nhất để áp dụng một nhãn là ở chế độ hàng loạt, từ danh sách Người đăng ký:

1. Mở **Studio Chiến dịch > Người đăng ký**.
2. Chọn ô chọn trên mỗi người đăng ký bạn muốn gán nhãn (hoặc **Chọn tất cả trên trang này**).
3. Từ danh sách thả xuống **Hành động hàng loạt**, chọn **Thêm nhãn cho các mục đã chọn…** (hoặc **Xóa nhãn khỏi các mục đã chọn…** để bỏ gán nhãn).
4. Nhấp vào **Xong**.
5. Chọn nhãn từ danh sách và nhấp vào **Thêm nhãn** (hoặc **Xóa nhãn**).

![Trình chọn nhãn hàng loạt sau khi chọn "Thêm nhãn cho các mục đã chọn..." cho bốn người đăng ký](/static/core/admin/img/help/subscriber-tags/bulk-tag-picker.webp)

Một khi được áp dụng, một nhãn sẽ hiện thị dưới dạng một miếng chip nhỏ trên thẻ người đăng ký trong danh sách, bên cạnh các biểu tượng trạng thái và nguồn của họ. Một bộ lọc **Nhãn** cũng xuất hiện trong bảng điều khiển lọc danh sách Người đăng ký một khi bạn có ít nhất một nhãn, vì vậy bạn có thể thu hẹp danh sách xuống để mọi người mang một nhãn cụ thể — hữu ích để kiểm tra xem ai có trong một danh sách trước khi bạn xây dựng một chiến dịch xung quanh nó.

![Danh sách Người đăng ký được lọc để chỉ có nhãn VIP, với nút Nhập CSV và các miếng chip nhãn hiển thị](/static/core/admin/img/help/subscriber-tags/subscriber-list-tag-chips.webp)

Bạn cũng có thể thêm hoặc xóa nhãn của một người đăng ký duy nhất trực tiếp từ trang chỉnh sửa của họ, sử dụng cùng một trường **Nhãn** mà hành động hàng loạt quản lý.

## Sử dụng nhãn trong các nhóm

Các nhóm là các danh sách đối tượng dựa trên quy tắc mà bạn hướng các chiến dịch và hành trình đến. Một khi bạn đã tạo ít nhất một nhãn, một **Có nhãn** điều kiện sẽ xuất hiện trong trình xây dựng quy tắc nhóm — nó không xuất hiện trên cài đặt ban đầu với không có nhãn nào được xác định, vì vậy bạn sẽ không thấy một tùy chọn chết trước khi nó hữu ích với bạn.

Để sử dụng, mở **Studio Chiến dịch > Nhóm**, thêm (hoặc chỉnh sửa) một nhóm động, và nhấp vào **+ Thêm điều kiện**:

1. Thiết lập trường điều kiện thành **Có nhãn**.
2. Chọn một toán tử — **là** cho một nhãn duy nhất, hoặc **là một trong số** khi bạn muốn diễn đạt theo cách đó.
3. Chọn nhãn từ danh sách thả xuống.

[![](A "Has tag" condition set to VIP, showing a live count of matching subscribers)](/static/core/admin/img/help/subscriber-tags/segment-has-tag-rule.webp)

Số lượng ở góc trên bên phải sẽ được cập nhật khi bạn xây dựng quy tắc, vì vậy bạn có thể xem chính xác số lượng người đăng ký hiện tại đáp ứng điều kiện trước khi lưu. Mỗi điều kiện **Has tag** hiện tại chỉ khớp với một thẻ tại một thời điểm — nếu bạn muốn một đối tượng bao gồm *mọi* thẻ (ví dụ: `VIP` hoặc `Wholesale`), hãy thêm một **Has tag** cho mỗi thẻ và đặt **Match** thành **any**.

Điều này làm cho các thẻ hữu ích hơn ngoài việc tổ chức: một đoạn được xây dựng dựa trên **Has tag** trở thành một đối tượng bạn có thể chọn làm **Segment** trên một cuộc phát sóng hoặc chiến dịch lặp lại, hoặc là cài đặt **Only for segment** trong một hành trình — vì vậy "mọi người được gán thẻ VIP" có thể có chuỗi chào mừng riêng, bản tin hàng tuần riêng, hoặc đơn giản là những người bạn chọn lần tiếp theo khi gửi thông báo một lần.

## Mẹo

- Giữ tên thẻ ngắn và cụ thể — chúng xuất hiện dưới dạng các nút nhỏ trên thẻ người đăng ký, vì vậy `VIP` sẽ dễ đọc hơn so với `Very Important Person - Tier 1`.
- Sử dụng bộ lọc **Tag** để kiểm tra xem ai thực sự được gán thẻ trước khi xây dựng một đoạn hoặc gửi chiến dịch xung quanh nó.
- Việc gán thẻ là tích lũy — việc xóa một thẻ khỏi người đăng ký không bao giờ ảnh hưởng đến các thẻ khác mà họ có, và không bao giờ chạm đến trạng thái, nguồn hoặc sự đồng ý của họ.
- Kết hợp các thẻ với các điều kiện khác (như **Opted into marketing** hoặc **Total spent**) trên cùng một đoạn để có đối tượng chính xác hơn, không chỉ là một thẻ duy nhất.
- Một người đăng ký có thể mang nhiều thẻ như bạn muốn — không có giới hạn, vì vậy bạn có thể sử dụng chúng cho nhiều mục đích chồng chéo (một cấp bậc trung thành *và* một danh sách sự kiện *và* một ghi chú nguồn).
- Nếu một thẻ không còn hữu ích, việc xóa nó khỏi **Subscriber tags** sẽ xóa nó khỏi mọi người đăng ký mà nó đã được áp dụng và khỏi bất kỳ quy tắc đoạn nào tham chiếu đến nó — các đoạn sử dụng nó sẽ đơn giản là ngừng khớp với điều kiện đó.