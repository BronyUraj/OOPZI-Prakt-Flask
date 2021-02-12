from flask import render_template, request
from app import app, db
from app.models import Records
import requests



@app.route("/")
def index():
    return "Hi!"

@app.route("/trash/<id>")
def trash(id):
    return str(Records.query.filter_by(id=id).paginate().items[0])

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
