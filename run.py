# coding=utf-8
"""Файл запуска приложения"""


from web import app

app.run(debug=True, host='0.0.0.0', port=8000)
