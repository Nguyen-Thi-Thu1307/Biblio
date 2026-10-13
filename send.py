from biblio import create_app
from biblio.extensions import db
from biblio.models import User, Category, Book

app = create_app()

with app.app_context():
    if Category.query.first():
        print("Dữ liệu mẫu đã tồn tại, bỏ qua.")
    else:
        names = ["Văn học", "Kinh tế", "Công nghệ", "Kỹ năng", "Ngoại ngữ"]
        cats = {n: Category(name=n) for n in names}
        db.session.add_all(cats.values())
        db.session.commit()

        admin = User(username="admin", email="admin@biblio.vn",
                     full_name="Quản trị viên", role="admin")
        admin.set_password("admin123")
        db.session.add(admin)

        data = [
            ("Nhà giả kim", "Paulo Coelho", "NXB Văn học", 79000, 30, "Văn học", "Hành trình theo đuổi giấc mơ."),
            ("Dế Mèn phiêu lưu ký", "Tô Hoài", "NXB Kim Đồng", 55000, 50, "Văn học", "Tác phẩm kinh điển dành cho thiếu nhi."),
            ("Cha giàu cha nghèo", "Robert Kiyosaki", "NXB Trẻ", 95000, 35, "Kinh tế", "Bài học về tài chính cá nhân."),
            ("Nghĩ giàu làm giàu", "Napoleon Hill", "NXB Lao động", 88000, 28, "Kinh tế", "13 nguyên tắc để thành công."),
            ("Lập trình Python cơ bản", "Nguyễn Văn A", "NXB Bách Khoa", 120000, 25, "Công nghệ", "Giáo trình Python cho người mới."),
            ("Clean Code", "Robert C. Martin", "NXB Thế Giới", 210000, 15, "Công nghệ", "Viết mã sạch và dễ bảo trì."),
            ("Cơ sở dữ liệu", "Trần Thị B", "NXB Giáo dục", 135000, 20, "Công nghệ", "Nền tảng SQL và thiết kế CSDL."),
            ("Đắc nhân tâm", "Dale Carnegie", "NXB Tổng hợp", 86000, 40, "Kỹ năng", "Nghệ thuật đối nhân xử thế."),
            ("Thói quen nguyên tử", "James Clear", "NXB Thế Giới", 140000, 22, "Kỹ năng", "Xây dựng thói quen tốt mỗi ngày."),
            ("Tuổi trẻ đáng giá bao nhiêu", "Rosie Nguyễn", "NXB Hội Nhà văn", 75000, 33, "Kỹ năng", "Dành cho người trẻ."),
            ("Từ vựng tiếng Anh theo chủ đề", "Nhiều tác giả", "NXB Đại học Quốc gia", 99000, 45, "Ngoại ngữ", "Học từ vựng hiệu quả."),
            ("Ngữ pháp tiếng Anh căn bản", "Mai Lan Hương", "NXB Tổng hợp", 110000, 38, "Ngoại ngữ", "Tổng hợp ngữ pháp cần thiết."),
            ("Bố con cá gai", "Cho Chang-in","NXB Hội Nhà Văn", 105000, 100, "Văn học"," Tiểu thuyết tâm lý xã hội."),
            ("Cây cam ngọt của tôi","José Mauro de Vasconcelos","NXB Hội Nhà Văn", 108000, 45,"Văn học","Bài học sâu sắc về tình yêu thương, lòng trắc ẩn và sự khắc nghiệt của việc phải lớn lên sớm."),
            ("Chú bé mang Pyjama sọc","John Boyne","NXB Hội Nhà Văn", 102000, 25,"Văn học","Sự tàn khốc, phi lý của chiến tranh, nạn diệt chủng Holocaust và vẻ đẹp trong sáng của tình bạn xuyên biên giới."),
            ("Đồi gió hú","Emily Brontë","NXB Hội Nhà Văn",135000,40,"Văn học","Bản chất cực đoan của tình yêu gắn liền với lòng hận thù, sự tự hủy hoại và những bi kịch gia đình kéo dài qua nhiều thế hệ."),
            ("Hai số phận","Jeffrey Archer","NXB Văn Học",195000,50,"Văn học","Bài ca về ý chí kiên cường, khát vọng vươn lên, sức mạnh của đồng tiền, sự thù hận và cái giá của sự thành công."),
            ("Hai vạn dặm dưới đáy biển","Jules Verne","NXB Văn Học",90000,120,"Văn học","Khát vọng chinh phục đại dương, ca ngợi sự tiến bộ của khoa học kỹ thuật và tinh thần tự do, bất khuất của con người trước cường quyền."),
            ("Không gia đình","Hector Malot","NXB Hội Nhà Văn",120000101,"Văn học","Ca ngợi lao động chân chính, lòng tự trọng, tình bạn, tình yêu thương con người và ý chí vượt qua nghịch cảnh của trẻ thơ."),
            ("Kiêu hãnh và định kiến","Jane Austen","NXB Hội Nhà Văn ",135000,120,"Văn học","Bản chất của tình yêu và hôn nhân đích thực; sự nguy hại của cái tôi kiêu hãnh và những định kiến vội vàng trong các mối quan hệ."),
            ("Người đàn ông mang tên OVE","Fredrik Backman","NXB Trẻ",160000,150,"Văn học","Sức mạnh chữa lành của tình người, lòng trắc ẩn và sự kết nối bất ngờ giữa những tâm hồn cô đơn."),
            ("Ông già và biển cả","Ernest Hemingway","NXB Hội Nhà Văn",75000,54,"Văn học","Ý chí bất khuất, kiên cường của con người trước số phận và định ước: Con người có thể bị hủy diệt nhưng không thể bị đánh bại."),
            ("Trăm năm cô đơn","Gabriel García Márquez","NXB Hội Nhà Văn",170000,60,"Văn học","Bản chất sâu thẳm của sự cô đơn gắn liền với định mệnh; mối quan hệ ruột thịt bị ghẻ lạnh; và lời cảnh báo về sự tự diệt vong của một gia tộc, một dân tộc nếu không có tình yêu thương cùng sự kết nối.")
        ]
        for title, author, pub, price, stock, cat, desc in data:
            db.session.add(Book(title=title, author=author, publisher=pub,
                                price=price, stock=stock, description=desc,
                                category_id=cats[cat].id))
        db.session.commit()
        print("Đã tạo dữ liệu mẫu.")