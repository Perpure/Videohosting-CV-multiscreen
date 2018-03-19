from config import basedir
from flask import session
from web.models import User


def read_image(pid):
    path=basedir + '/images/%s.jpg' % pid
    with open(path, "rb") as im:
        f = im.read()
        b = bytearray(f)
        return b


def read_video(vid):
    path = basedir + '/video/%s/video.mp4' % vid
    with open(path, "rb") as im:
        f = im.read()
        b = bytearray(f)
        return b


def cur_user():
    if 'Login' in session:
        return User.query.filter_by(login=session['Login']).first()
    else:
        return None