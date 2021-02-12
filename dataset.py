# https://apidata.mos.ru/v1/datasets/2542/rows/?api_key=6797106fd85191ea7335559677948c72&$top=2&$skip=9
# https://apidata.mos.ru/v1/datasets/2542/count/?api_key=6797106fd85191ea7335559677948c72
import requests
from app import app, db
from app.models import Records


def get_new_data(start_point):
    count = int(
        requests.get(
            "https://apidata.mos.ru/v1/datasets/2542/count/",
            params={"api_key": app.config["API_KEY"]},
        ).text
    )
    print(count)
    for num in range(start_point, count, 1000):
        jsondata = requests.get(
            "https://apidata.mos.ru/v1/datasets/2542/rows/",
            params={"api_key": app.config["API_KEY"], "$top": 1000, "$skip": num},
        ).json()
        for record in jsondata:
            print(record)
            cell = record["Cells"]
            YardName = cell["YardName"]
            YardLocation = cell["YardLocation"][0]
            District = YardLocation["District"]
            AdmArea = YardLocation["AdmArea"]
            Address = YardLocation["Address"]
            YardArea = cell["YardArea"]
            YardType = cell["YardType"]
            Coordinates = "".join([str(cord) for cord in cell["geoData"]["coordinates"]])
            Record = Records(YardName=YardName, District=District, AdmArea=AdmArea, Address=Address, YardArea=YardArea, YardType=YardType, Coordinates=Coordinates)
            db.session.add(Record)
        db.session.commit()
