from app import app, db, crontab
from app.models import Records
import requests


@crontab.job(hour="3")
def update():
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
                YardArea = cell["YardArea"]
                YardType = cell["YardType"]
                Coordinates = str(cell["geoData"]["coordinates"][0]) + "-" + str(cell["geoData"]["coordinates"][1])
                Record = Records(
                    YardName=YardName,
                    YardArea=YardArea,
                    YardType=YardType,
                    Coordinates=Coordinates,
                )
                db.session.add(Record)
            db.session.commit()
        print("Updated!")
        return "Updated!"
    print("DB is up-to-date!")
    return "DB is up-to-date"