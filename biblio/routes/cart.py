from urllib.parse import urlsplit

from flask import Blueprint, flash, redirect, render_template, request, url_for
from ..decorators import get_current_user, login_required
from ..extensions import db
from ..models import Book, Cart, CartItem
from ..notifications import create_notification
from translations import tr


bp = Blueprint("cart", __name__, url_prefix="/cart")


def _get_or_create_cart(user):
    cart = Cart.query.filter_by(user_id=user.id).first()
    if cart is None:
        cart = Cart(user_id=user.id)
        db.session.add(cart)
        db.session.flush()
    return cart


def _cart_item_for_user(item_id, user):
    return (
        CartItem.query.join(Cart)
        .filter(CartItem.id == item_id, Cart.user_id == user.id)
        .first_or_404()
    )


def _safe_referrer(default_endpoint, **default_values):
    referrer = request.referrer
    if referrer:
        parsed = urlsplit(referrer)
        if (
            (not parsed.netloc or parsed.netloc == request.host)
            and parsed.path.startswith("/")
            and not parsed.path.startswith("//")
        ):
            path = parsed.path or url_for(default_endpoint, **default_values)
            return f"{path}?{parsed.query}" if parsed.query else path
    return url_for(default_endpoint, **default_values)


@bp.route("", methods=["GET"])
@bp.route("/", methods=["GET"])
@login_required
def view_cart():
    user = get_current_user()
    cart = Cart.query.filter_by(user_id=user.id).first()
    items = cart.items if cart else []
    total = sum(item.book.price * item.quantity for item in items)
    return render_template("cart.html", cart=cart, items=items, total=total)


@bp.route("/add/<int:book_id>", methods=["POST"])
@login_required
def add_to_cart(book_id):
    user = get_current_user()
    book = Book.query.get_or_404(book_id)
    raw_quantity = request.form.get("quantity")
    try:
        quantity = int(raw_quantity) if raw_quantity is not None else 1
    except ValueError:
        quantity = None
    if quantity is None or quantity < 1:
        flash(tr("flash.invalid_quantity"), "error")
        return redirect(_safe_referrer("books.detail", book_id=book.id))

    stock = book.stock or 0
    if stock < 1:
        flash(tr("flash.out_of_stock"), "warning")
        return redirect(_safe_referrer("books.detail", book_id=book.id))

    cart = _get_or_create_cart(user)
    item = CartItem.query.filter_by(cart_id=cart.id, book_id=book.id).first()
    new_quantity = quantity + (item.quantity if item else 0)
    if new_quantity > stock:
        flash(tr("flash.stock_limit", stock=stock, title=book.title), "warning")
        return redirect(_safe_referrer("books.detail", book_id=book.id))

    if item:
        item.quantity = new_quantity
    else:
        db.session.add(CartItem(cart=cart, book=book, quantity=quantity))
    create_notification(
        user.id,
        tr("notification.cart_added_title"),
        tr("notification.cart_added_body", title=book.title),
        url_for("cart.view_cart"),
    )
    db.session.commit()
    flash(tr("flash.added_to_cart", title=book.title), "success")
    return redirect(_safe_referrer("books.detail", book_id=book.id))


@bp.route("/update/<int:item_id>", methods=["POST"])
@login_required
def update_quantity(item_id):
    user = get_current_user()
    item = _cart_item_for_user(item_id, user)
    raw_quantity = request.form.get("quantity")
    try:
        quantity = int(raw_quantity) if raw_quantity is not None else None
    except ValueError:
        quantity = None
    if quantity is None or quantity < 1:
        flash(tr("flash.quantity_positive"), "error")
        return redirect(url_for("cart.view_cart"))

    stock = item.book.stock or 0
    if quantity > stock:
        flash(tr("flash.stock_limit", stock=stock, title=item.book.title), "warning")
        return redirect(url_for("cart.view_cart"))

    item.quantity = quantity
    create_notification(
        user.id,
        tr("notification.cart_updated_title"),
        tr("notification.cart_updated_body", title=item.book.title, quantity=quantity),
        url_for("cart.view_cart"),
    )
    db.session.commit()
    flash(tr("flash.cart_updated"), "success")
    return redirect(url_for("cart.view_cart"))


@bp.route("/remove/<int:item_id>", methods=["POST"])
@login_required
def remove_item(item_id):
    user = get_current_user()
    item = _cart_item_for_user(item_id, user)
    title = item.book.title
    db.session.delete(item)
    create_notification(
        user.id,
        tr("notification.cart_removed_title"),
        tr("notification.cart_removed_body", title=title),
        url_for("cart.view_cart"),
    )
    db.session.commit()
    flash(tr("flash.item_removed", title=title), "success")
    return redirect(url_for("cart.view_cart"))


@bp.route("/clear", methods=["POST"])
@login_required
def clear_cart():
    user = get_current_user()
    cart = Cart.query.filter_by(user_id=user.id).first()
    if cart:
        item_count = CartItem.query.filter_by(cart_id=cart.id).count()
        CartItem.query.filter_by(cart_id=cart.id).delete()
        if item_count:
            create_notification(
                user.id,
                tr("notification.cart_cleared_title"),
                tr("notification.cart_cleared_body"),
                url_for("cart.view_cart"),
            )
        db.session.commit()
    flash(tr("flash.cart_cleared"), "success")
    return redirect(url_for("cart.view_cart"))