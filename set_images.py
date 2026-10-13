from biblio import create_app
from biblio.extensions import db
from biblio.models import Book

images = {
    "Nhà giả kim": "nha-gia-kim.jpg",
    "Dế Mèn phiêu lưu ký": "de-men-phieu-luu-ky.jpg",
    "Cha giàu cha nghèo": "cha-giau-cha-ngheo.jpg",
    "Nghĩ giàu làm giàu": "nghi-giau-lam-giau.jpg",
    "Lập trình Python cơ bản": "lap-trinh-python-co-ban.jpg",
    "Clean Code": "clean-code.jpg",
    "Cơ sở dữ liệu": "co-so-du-lieu.jpg",
    "Đắc nhân tâm": "dac-nhan-tam.jpg",
    "Thói quen nguyên tử": "thoi-quen-nguyen-tu.jpg",
    "Tuổi trẻ đáng giá bao nhiêu": "tuoi-tre-dang-gia-bao-nhieu.jpg",
    "Từ vựng tiếng Anh theo chủ đề": "tu-vung-tieng-anh.jpg",
    "Ngữ pháp tiếng Anh căn bản": "ngu-phap-tieng-anh.jpg",
    "Bố con cá gai": "bo_con_ca_gai.jpg",
    "Cây cam ngọt của tôi": "cay_cam_ngot_cua_toi.jpg",
    "Đồi gió hú":"doi_gio_hu.jpg",
    "Hai số phận":"hai_so_phan.jpg",
    "Hai vạn dặm dưới biển":"hai_van_dam_duoi_bien.jpg",
    "Không gia đình":"khong_gia_dinh.jpg","Ông già và biển cả":"ong_gia_va_bien_ca.jpg", "Trăm năm cô đơn":"tram_nam_co_don.jpg",
    "Chú bé mang pyjama sọc":"chu_be_mang_pỵama_soc", "Kiêu hãnh và định kiến":"kieu_hanh_va_dinh_kien.jpg","Người đàn ông mang tên OVE":"nguoi_dan_ong_mang_ten_ove.jpg",
}

app = create_app()
with app.app_context():
    for title, filename in images.items():
        book = Book.query.filter_by(title=title).first()
        if book:
            book.image = filename
    db.session.commit()
    print("Đã cập nhật ảnh cho sách.")