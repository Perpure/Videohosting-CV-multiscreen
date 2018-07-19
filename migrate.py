# coding=utf-8
"""Файл миграции приложения"""
from web import db
from web.models import *

db.drop_all()
db.create_all()
user = User("TestUser")
user.save("testpassword")
matrix_1 = Calibrate_matrix(matrix='100000000')
db.session.add(matrix_1)
matrix_2 = Calibrate_matrix(matrix='110000000')
db.session.add(matrix_2)
matrix_3 = Calibrate_matrix(matrix='111000000')
db.session.add(matrix_3)
matrix_4 = Calibrate_matrix(matrix='111100000')
db.session.add(matrix_4)
matrix_5 = Calibrate_matrix(matrix='111110000')
db.session.add(matrix_5)
matrix_6 = Calibrate_matrix(matrix='111111000')
db.session.add(matrix_6)
user = User("tsarkov")
user.save("tsarkov1")
user = User("konnov")
user.save("konnov12")
user = User("mezentsev")
user.save("mezentsev")
user = User("vorobev")
user.save("vorobev1")
user = User("alekseev")
user.save("alekseev")
user = User("semenov")
user.save("semenov1")
user = User("shihanov")
user.save("shihanov")
user = User("dyachek")
user.save("dyachek1")
user = User("kucherov")
user.save("kucherov")
user = User("karimov")
user.save("karimov1")
user = User("valegov")
user.save("valegov1")
user = User("syomochkin")
user.save("syomochkin")
db.session.commit()
