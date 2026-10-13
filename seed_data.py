from biblio import create_app
from biblio.extensions import db
from biblio.models import Book, Category


CATEGORIES = (
    ("Văn học", "Literature"),
    ("Kinh tế", "Economics"),
    ("Công nghệ", "Technology"),
    ("Kỹ năng", "Personal Development"),
    ("Ngoại ngữ", "Foreign Languages"),
    ("Thiếu nhi", "Children's Books"),
    ("Lịch sử", "History"),
    ("Khoa học", "Science"),
)

BOOKS = (
    ("Những mùa gió", "Nguyễn An", 89000, 24, "Văn học", "Tập truyện ngắn về những đổi thay trong cuộc sống.", "A collection of short stories about changes in life."),
    ("Bên kia ô cửa", "Lê Minh Hà", 96000, 18, "Văn học", "Câu chuyện về gia đình và những lựa chọn.", "A story about family and the choices we make."),
    ("Dòng sông ký ức", "Trần Hoài Nam", 105000, 16, "Văn học", "Hành trình trở về miền quê tuổi thơ.", "A journey back to the countryside of childhood memories."),
    ("Khởi nghiệp từ con số không", "Phạm Quốc Bảo", 125000, 20, "Kinh tế", "Những bước cơ bản để xây dựng một dự án kinh doanh.", "Practical first steps for building a business venture."),
    ("Quản lý tài chính cá nhân", "Nguyễn Thu Hương", 118000, 30, "Kinh tế", "Cách lập ngân sách và quản lý chi tiêu hằng ngày.", "How to budget and manage everyday expenses."),
    ("Tư duy đầu tư dài hạn", "Đỗ Thành Công", 149000, 14, "Kinh tế", "Nhập môn các nguyên tắc đầu tư và quản trị rủi ro.", "An introduction to investing principles and risk management."),
    ("Python qua bài tập thực hành", "Lê Hoàng Phúc", 159000, 22, "Công nghệ", "Bài tập lập trình Python từ cơ bản đến ứng dụng.", "Hands-on Python exercises from fundamentals to practical applications."),
    ("Nhập môn trí tuệ nhân tạo", "Vũ Thanh Tùng", 185000, 12, "Công nghệ", "Giới thiệu các khái niệm nền tảng của trí tuệ nhân tạo.", "An introduction to the fundamental concepts of artificial intelligence."),
    ("Web căn bản với Flask", "Nguyễn Hải Đăng", 172000, 17, "Công nghệ", "Hướng dẫn xây dựng ứng dụng web nhỏ bằng Flask.", "A guide to building small web applications with Flask."),
    ("Giao tiếp tự tin mỗi ngày", "Mai Phương Linh", 99000, 25, "Kỹ năng", "Các phương pháp luyện tập giao tiếp trong công việc.", "Practical ways to build confidence in workplace communication."),
    ("Lập kế hoạch hiệu quả", "Trương Gia Huy", 108000, 21, "Kỹ năng", "Công cụ thực tế để xác định mục tiêu và theo dõi tiến độ.", "Practical tools for setting goals and tracking progress."),
    ("Tập trung trong thời đại số", "Hoàng Ngọc Mai", 115000, 19, "Kỹ năng", "Gợi ý xây dựng thói quen tập trung và làm việc sâu.", "Ideas for building focus and deep-work habits in the digital age."),
    ("Tiếng Anh giao tiếp theo chủ đề", "Đặng Khánh Vy", 132000, 28, "Ngoại ngữ", "Mẫu câu và từ vựng cho các tình huống thường gặp.", "Useful phrases and vocabulary for common situations."),
    ("Tự học tiếng Nhật nhập môn", "Phan Nhật Minh", 145000, 15, "Ngoại ngữ", "Làm quen với chữ viết và mẫu câu tiếng Nhật căn bản.", "An introduction to Japanese writing systems and basic expressions."),
    ("Từ vựng tiếng Pháp căn bản", "Bùi Ngọc Anh", 121000, 13, "Ngoại ngữ", "Từ vựng tiếng Pháp thông dụng dành cho người mới học.", "Everyday French vocabulary for beginner learners."),
    ("Khu vườn của bé", "Nguyễn Thảo Nhi", 68000, 32, "Thiếu nhi", "Câu chuyện nhẹ nhàng giúp trẻ khám phá thiên nhiên.", "A gentle story that helps children explore nature."),
    ("Chuyến tàu đến xứ sở mây", "Lâm Bảo Ngọc", 74000, 26, "Thiếu nhi", "Cuộc phiêu lưu kỳ thú dành cho độc giả nhỏ tuổi.", "An exciting adventure for young readers."),
    ("Những dấu mốc lịch sử Việt Nam", "Phạm Đức Long", 158000, 11, "Lịch sử", "Tổng quan một số sự kiện và giai đoạn lịch sử Việt Nam.", "An overview of key events and periods in Vietnamese history."),
    ("Chuyện kể về các nền văn minh", "Đinh Minh Châu", 169000, 10, "Lịch sử", "Khám phá những nền văn minh tiêu biểu trong lịch sử thế giới.", "Explore influential civilizations throughout world history."),
    ("Vũ trụ quanh ta", "Lê Quang Vinh", 142000, 16, "Khoa học", "Giới thiệu kiến thức thiên văn dành cho độc giả phổ thông.", "An accessible introduction to astronomy for general readers."),
)


def seed_data():
    category_names = tuple(name for name, _ in CATEGORIES)
    categories = {
        category.name: category
        for category in Category.query.filter(Category.name.in_(category_names)).all()
    }
    added_categories = 0

    for name, name_en in CATEGORIES:
        if name not in categories:
            category = Category(name=name, name_en=name_en)
            db.session.add(category)
            categories[name] = category
            added_categories += 1
        elif not categories[name].name_en:
            categories[name].name_en = name_en

    db.session.flush()

    added_books = 0
    for title, author, price, stock, category_name, description, description_en in BOOKS:
        exists = Book.query.filter_by(title=title, author=author).first()
        if exists:
            if not exists.description_en:
                exists.description_en = description_en
            continue

        db.session.add(
            Book(
                title=title,
                author=author,
                price=price,
                stock=stock,
                description=description,
                description_en=description_en,
                category_id=categories[category_name].id,
            )
        )
        added_books += 1

    db.session.commit()
    return added_categories, added_books


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        category_count, book_count = seed_data()
        print(f"Đã thêm {category_count} thể loại và {book_count} cuốn sách mẫu.")
