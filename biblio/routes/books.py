from flask import Blueprint, jsonify, render_template, request
from ..models import Book, Category

bp = Blueprint("books", __name__, url_prefix="/books")


@bp.route("/")
def list_books():
    q = request.args.get("q", "").strip()
    category_id = request.args.get("category", type=int)
    sort = request.args.get("sort", "name_asc")

    query = Book.query
    if q:
        like = f"%{q}%"
        query = query.filter(Book.title.ilike(like) | Book.author.ilike(like))
    if category_id:
        query = query.filter(Book.category_id == category_id)

    sorts = {
        "name_asc": Book.title.asc(),
        "price_asc": Book.price.asc(),
        "price_desc": Book.price.desc(),
    }
    query = query.order_by(sorts.get(sort, Book.title.asc()))

    return render_template(
        "books/list.html",
        books=query.all(),
        categories=Category.query.order_by(Category.name).all(),
        q=q, category_id=category_id, sort=sort,
    )


@bp.route("/suggestions")
def search_suggestions():
    q = request.args.get("q", "").strip()
    if not q:
        return jsonify([])

    like = f"%{q}%"
    books = (
        Book.query.with_entities(Book.title, Book.author)
        .filter(Book.title.ilike(like) | Book.author.ilike(like))
        .order_by(Book.title.asc())
        .limit(6)
        .all()
    )
    return jsonify([{"title": book.title, "author": book.author} for book in books])


@bp.route("/<int:book_id>")
def detail(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template("books/detail.html", book=book)