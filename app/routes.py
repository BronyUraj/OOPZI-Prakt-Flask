from flask import render_template, request, url_for
from app import app, db, cache
from app.models import Records
import requests



@app.route("/")
@app.route("/trash")
@app.route("/trash/<page>")
@cache.cached()
def trash(page=1):
    trash = Records.query.paginate(int(page), app.config["RECORD_PER_PAGE"], False)
    next_url = url_for("trash", page=trash.next_num) if trash.has_next else None
    prev_url = url_for("trash", page=trash.prev_num) if trash.has_prev else None
    return render_template(
        "trash.html",
        title="Trash",
        trash=trash.items,
        next_url=next_url,
        prev_url=prev_url,
    )
