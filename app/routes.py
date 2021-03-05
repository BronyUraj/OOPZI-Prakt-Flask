from flask import render_template, request, url_for
from app import app, db
from app.models import Records
import requests


@app.route("/")
def index():
    return "Hi!"


@app.route("/trash")
def trash():
    page = request.args.get("page", 1, type=int)
    trash = Records.query.paginate(page, app.config["RECORD_PER_PAGE"], False)
    next_url = url_for("trash", page=trash.next_num) if trash.has_next else None
    prev_url = url_for("trash", page=trash.prev_num) if trash.has_prev else None
    return render_template(
        "trash.html",
        title="Trash",
        trash=trash.items,
        next_url=next_url,
        prev_url=prev_url,
    )


@app.route("/update")
def get_new_data():
    count = int(
        requests.get(
            "https://apidata.mos.ru/v1/datasets/2542/count/",
            params={"api_key": app.config["API_KEY"]},
        ).text
    )
    db_count = db.session.query(Records).count()
    if db_count != count:
        for num in range(db_count, count, 1000):
            jsondata = requests.get(
                "https://apidata.mos.ru/v1/datasets/2542/rows/",
                params={"api_key": app.config["API_KEY"], "$top": 1000, "$skip": num},
            ).json()
            for record in jsondata:
                cell = record["Cells"]
                YardName = cell["YardName"]
                YardLocation = cell["YardLocation"][0]
                District = YardLocation["District"]
                AdmArea = YardLocation["AdmArea"]
                Address = YardLocation["Address"]
                YardArea = cell["YardArea"]
                YardType = cell["YardType"]
                Coordinates = "".join(
                    [str(cord) for cord in cell["geoData"]["coordinates"]]
                )
                Record = Records(
                    YardName=YardName,
                    District=District,
                    AdmArea=AdmArea,
                    Address=Address,
                    YardArea=YardArea,
                    YardType=YardType,
                    Coordinates=Coordinates,
                )
            datasetsb.session.add(Record)
            db.session.commit()
        return "Updated!"
    return "DB is up-to-date"
