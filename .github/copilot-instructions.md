## Tổng quan

Biblio là website thương mại điện tử bán sách, xây dựng bằng Python, Flask và SQLite. Giao diện, nội dung và thông báo dành cho người dùng phải dùng tiếng Việt; giao diện sử dụng Bootstrap 5.

Trước khi sửa code, hãy đọc cấu trúc và cách triển khai hiện có. Phân biệt rõ tính năng đã hoạt động với tính năng mới được yêu cầu; không xem nội dung tài liệu này là bằng chứng rằng một tính năng đã được triển khai.

## Quy tắc làm việc

- Mỗi lần chỉ thực hiện **một việc** theo yêu cầu hiện tại. Không tự ý mở rộng sang tính năng hay thay đổi khác.
- Không xóa, thay thế hoặc viết lại code cũ khi chưa hỏi và được người dùng đồng ý. Ưu tiên thay đổi nhỏ, tương thích với hành vi hiện có.
- Chỉ sửa các file cần thiết; không đổi cấu trúc dự án hoặc thêm thư viện mới nếu chưa được hỏi.
- Nếu yêu cầu chưa rõ hoặc có nhiều lựa chọn ảnh hưởng đáng kể đến hành vi, hãy hỏi trước khi quyết định.
- Sau khi sửa, chạy kiểm tra hoặc test phù hợp trong phạm vi thay đổi và báo rõ kết quả.

## Quy ước code

- Giữ Flask application factory và cấu trúc hiện có. Đặt model trong `biblio/models.py`; tách từng nhóm route thành Blueprint riêng trong `biblio/routes/`; đăng ký Blueprint tại application factory.
- Dùng Flask-SQLAlchemy để truy cập SQLite; không viết truy vấn SQL thủ công nếu ORM hiện có đáp ứng được.
- Dùng Flask-Login cho đăng nhập, đăng xuất và bảo vệ route; kiểm tra quyền admin ở phía server. Không tự tạo một cơ chế xác thực song song.
- Viết comment trong code bằng tiếng Việt, chỉ khi comment giúp giải thích điều không hiển nhiên. Đặt tên biến, hàm, class và endpoint rõ ràng, nhất quán với code hiện có.
- Dùng template Jinja kế thừa layout chung; dùng Bootstrap 5 cho thành phần giao diện. Tránh lặp cấu trúc HTML nếu có thể dùng template chung hoặc partial sẵn có.
- Kiểm tra dữ liệu đầu vào ở phía server, xử lý lỗi minh bạch và hiển thị thông báo tiếng Việt phù hợp. Không dựa vào kiểm tra ở trình duyệt để bảo vệ dữ liệu.
- Giá sách lưu bằng số nguyên theo VND; hiển thị nhất quán theo định dạng Việt Nam. Kiểm tra tồn kho khi thêm giỏ và khi tạo đơn.
- Không lưu mật khẩu dạng văn bản thuần; dùng cơ chế băm mật khẩu an toàn của dự án.

## Phạm vi tính năng

### Khách chưa đăng nhập

- Xem trang chủ, danh mục và danh sách sách.
- Tìm kiếm sách; lọc theo thể loại và sắp xếp kết quả.
- Xem chi tiết sách, giá và tình trạng còn hàng.
- Đăng ký và đăng nhập tài khoản.

### Người dùng đã đăng nhập

- Quản lý thông tin tài khoản theo các chức năng được yêu cầu.
- Thêm sách vào giỏ; xem giỏ và cập nhật số lượng hoặc xóa mặt hàng.
- Tạo đơn hàng với thông tin nhận hàng; xem lịch sử và trạng thái đơn.
- Chỉ cho phép người dùng truy cập đơn hàng của chính mình.

### Quản trị viên

- Quản lý sách, thể loại, giá và tồn kho.
- Quản lý đơn hàng và cập nhật trạng thái theo quy ước của dự án.
- Quản lý tài khoản hoặc phân quyền chỉ khi có yêu cầu cụ thể.
- Bảo vệ mọi chức năng quản trị bằng kiểm tra quyền admin ở phía server.

Danh sách trên mô tả phạm vi sản phẩm, không khẳng định các tính năng đã có sẵn. Chỉ triển khai phần được yêu cầu trong mỗi lần làm việc.
