from app import app, db


class Records(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    YardName = db.Column(db.String(128), index=True, unique=True)
    YardArea = db.Column(db.Float)
    YardType = db.Column(db.String(64), index=True)
    Coordinates = db.Column(db.String(32))

    def __repr__(self):
        return (f"Имя мусорки: {self.YardName} Район мусорки: {self.AdmArea} Округ мусорки: {self.District} Адрес мусорки: {self.Address} Площадь мусорки: {self.YardArea} м^2 Тип мусорки: {self.YardType} Координаты мусорки: {self.Coordinates}")
