from functools import wraps
from flask import session, redirect, url_for, flash, request, abort
from urllib.parse import urlsplit
from .extensions import db
from .models import User
from translations import tr


def get_current_user():
    uid = session.get("user_id")
    return db.session.get(User, uid) if uid else None


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        user = get_current_user()
        if not user or not user.is_active:
            language = session.get("language")
            session.clear()
            if language in {"vi", "en"}:
                session["language"] = language
            flash(tr("flash.login_required"), "warning")
            next_url = request.path
            if request.method == "POST":
                referrer = request.referrer
                if referrer:
                    parsed = urlsplit(referrer)
                    if (
                        (not parsed.netloc or parsed.netloc == request.host)
                        and parsed.path.startswith("/")
                        and not parsed.path.startswith("//")
                    ):
                        next_url = parsed.path or url_for("main.home")
                        if parsed.query:
                            next_url += f"?{parsed.query}"
                    else:
                        next_url = url_for("main.home")
                else:
                    next_url = url_for("main.home")
            return redirect(url_for("auth.login", next=next_url))
        return f(*args, **kwargs)
    return wrapper


def admin_required(f):
    @wraps(f)
    @login_required
    def wrapper(*args, **kwargs):
        if get_current_user().role != "admin":
            abort(403)
        return f(*args, **kwargs)
    return wrapper