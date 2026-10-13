from flask import Blueprint, redirect, url_for
from ..decorators import get_current_user, login_required
from ..extensions import db
from ..models import Notification


bp = Blueprint("notifications", __name__, url_prefix="/notifications")


@bp.route("/<int:notification_id>/read", methods=["POST"])
@login_required
def mark_read(notification_id):
    user = get_current_user()
    notification = Notification.query.filter_by(
        id=notification_id, user_id=user.id
    ).first_or_404()
    notification.is_read = True
    db.session.commit()
    return redirect(notification.target)


@bp.route("/read-all", methods=["POST"])
@login_required
def mark_all_read():
    user = get_current_user()
    Notification.query.filter_by(user_id=user.id, is_read=False).update(
        {Notification.is_read: True}, synchronize_session=False
    )
    db.session.commit()
    return redirect(url_for("main.home"))
