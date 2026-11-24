"""HTTP routes for Infra Monitor."""

from functools import wraps

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from app.auth_utils import verify_password

bp = Blueprint("main", __name__)


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("user"):
            return redirect(url_for("main.login"))
        return view(*args, **kwargs)

    return wrapped


@bp.get("/")
@login_required
def index():
    return render_template(
        "index.html",
        username=session.get("user"),
        metrics={
            "cpu": "—",
            "memory": "—",
            "network": "—",
            "ports": "—",
        },
    )


@bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user"):
        return redirect(url_for("main.index"))

    error = None
    username_value = "admin"

    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""
        username_value = username or "admin"

        expected_user = current_app.config["ADMIN_USERNAME"]
        password_hash = current_app.config["ADMIN_PASSWORD_HASH"]

        # Generic failure message — do not reveal which field failed.
        if username == expected_user and verify_password(password_hash, password):
            session.clear()
            session["user"] = username
            flash("Signed in.", "ok")
            return redirect(url_for("main.index"))

        error = "Invalid credentials"

    return render_template("login.html", error=error, username_value=username_value)


@bp.post("/logout")
@login_required
def logout():
    session.clear()
    flash("Signed out.", "ok")
    return redirect(url_for("main.login"))
