from urllib.parse import urlsplit
import re

from flask import Blueprint, abort, flash, redirect, render_template, request, session, url_for
from ..extensions import db
from ..models import Book, Category, Contact
from translations import tr

bp = Blueprint("main", __name__)


@bp.route("/")
def home():
    newest = Book.query.order_by(Book.id.desc()).limit(8).all()
    return render_template("index.html", books=newest)


@bp.route("/about", methods=["GET", "POST"])
def about():
    catalog_categories = {}
    for category in Category.query.all():
        catalog_categories[category.name] = category
        if category.name_en:
            catalog_categories[category.name_en] = category

    form_data = {
        "name": request.form.get("name", "").strip(),
        "email": request.form.get("email", "").strip().lower(),
        "message": request.form.get("message", "").strip(),
    }

    if request.method == "POST":
        error = None
        if not all(form_data.values()):
            error = tr("about.contact_required")
        elif (
            len(form_data["name"]) > 100
            or len(form_data["email"]) > 120
            or len(form_data["message"]) > 2000
        ):
            error = tr("about.contact_too_long")
        elif not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", form_data["email"]):
            error = tr("about.contact_email_invalid")

        if error:
            flash(error, "error")
        else:
            db.session.add(
                Contact(
                    name=form_data["name"],
                    email=form_data["email"],
                    message=form_data["message"],
                )
            )
            db.session.commit()
            flash(tr("about.contact_success"), "success")
            return redirect(url_for("main.about", _anchor="contact"))

    return render_template(
        "about.html",
        form_data=form_data,
        catalog_categories=catalog_categories,
    )


@bp.route("/privacy")
def privacy_policy():
    return render_template(
        "legal.html",
        title_key="legal.privacy.title",
        sections=(
            ("legal.privacy.data_title", "legal.privacy.data"),
            ("legal.privacy.use_title", "legal.privacy.use"),
            ("legal.privacy.rights_title", "legal.privacy.rights"),
        ),
    )


@bp.route("/terms")
def terms():
    return render_template(
        "legal.html",
        title_key="legal.terms.title",
        sections=(
            ("legal.terms.acceptance_title", "legal.terms.acceptance"),
            ("legal.terms.orders_title", "legal.terms.orders"),
            ("legal.terms.responsibility_title", "legal.terms.responsibility"),
        ),
    )


@bp.route("/set-language/<lang>")
def set_language(lang):
    if lang not in {"vi", "en"}:
        abort(404)

    session["language"] = lang
    flash(tr("flash.language_changed"), "success")
    referrer = request.referrer
    if referrer:
        parsed = urlsplit(referrer)
        if (
            (not parsed.netloc or parsed.netloc == request.host)
            and parsed.path.startswith("/")
            and not parsed.path.startswith("//")
        ):
            return redirect(parsed.path + (f"?{parsed.query}" if parsed.query else ""))
    return redirect(url_for("main.home"))