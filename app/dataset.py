# https://apidata.mos.ru/v1/datasets/2542/rows/?api_key=6797106fd85191ea7335559677948c72&$top=2&$skip=9
# https://apidata.mos.ru/v1/datasets/2542/count/?api_key=6797106fd85191ea7335559677948c72
import requests
from app import app, db
from app.models import Records


def get_new_data():
    # count = int(requests.get("https://apidata.mos.ru/v1/datasets/2542/count/", params={"api_key": app.config["API_KEY"]}).text)
    jsondata = requests.get(
        "https://apidata.mos.ru/v1/datasets/2542/rows/",
        params={"api_key": app.config["API_KEY"], "$top": 5, "$skip": 2},
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
        coordinates = cell["geoData"]["coordinates"]
        print(
            f"Имя мусорки: {YardName}; Район: {District}; Округ: {AdmArea}; Адрес: {Address}; Площадь свалки: {YardArea}; Тип свалки: {YardType}; Координаты: {coordinates[0]}-{coordinates[1]}"
        )
