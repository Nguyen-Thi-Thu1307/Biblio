import re

from flask import Blueprint, jsonify, request, url_for
from sqlalchemy import or_

from ..models import Book, Category
from translations import get_language, tr

bp = Blueprint("chatbot", __name__, url_prefix="/chatbot")

_STOP_WORDS = {
    "cho", "có", "cuốn", "gì", "hay", "là", "loại", "nào", "nhé",
    "sách", "tôi", "tìm", "từ", "và", "về", "với", "muốn", "một",
    "cần", "được", "gợi", "ý", "tham", "khảo", "bạn", "mình", "xin",
    "co", "cuon", "gi", "la", "loai", "nao", "nha", "toi", "tim",
    "va", "ve", "voi", "mot", "duoc", "goi", "khao", "ban", "minh",
}
_SEARCH_FIELDS = (
    Book.title,
    Book.author,
    Book.description,
    Book.description_en,
    Category.name,
    Category.name_en,
)


@bp.post("/message")
def message():
    payload = request.get_json(silent=True) or {}
    if not isinstance(payload, dict):
        return jsonify(error=tr("chatbot.invalid_message")), 400

    text = payload.get("message", "")
    if not isinstance(text, str):
        return jsonify(error=tr("chatbot.invalid_message")), 400

    text = text.strip()
    if not text or len(text) > 240:
        return jsonify(error=tr("chatbot.invalid_length")), 400

    terms = list(
        dict.fromkeys(
            term
            for term in re.findall(r"[a-z0-9À-ỹ]+", text.lower())
            if len(term) > 1 and term not in _STOP_WORDS
        )
    )[:8]

    if not terms:
        return jsonify(
            reply=tr("chatbot.ask_preferences"),
            books=[],
        )

    matches = (
        Book.query.outerjoin(Category, Book.category_id == Category.id)
        .filter(Book.stock > 0)
        .filter(
            or_(
                *(field.ilike(f"%{term}%") for term in terms for field in _SEARCH_FIELDS)
            )
        )
        .limit(50)
        .all()
    )

    def relevance(book):
        fields = (
            (book.title or "", 5),
            (book.author or "", 4),
            (book.category.name if book.category else "", 3),
            (book.description or "", 1),
            (book.description_en or "", 1),
        )
        return sum(
            weight
            for term in terms
            for value, weight in fields
            if term in value.lower()
        )

    matches.sort(key=lambda book: (relevance(book), book.stock), reverse=True)
    recommendations = [
        {
            "title": book.title,
            "author": book.author,
            "category": (
                (book.category.name_en if get_language() == "en" and book.category.name_en else book.category.name)
                if book.category
                else ""
            ),
            "price": f"{book.price:,}".replace(",", ".") + " ₫",
            "url": url_for("books.detail", book_id=book.id),
        }
        for book in matches[:3]
    ]

    if recommendations:
        reply = tr("chatbot.recommendations_found")
    else:
        reply = tr("chatbot.no_recommendations")

    return jsonify(reply=reply, books=recommendations)