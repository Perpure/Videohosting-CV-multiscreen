from flask import redirect, render_template, session, url_for, make_response, request, send_file
from web import app
from web.forms import UploadVideoForm
from web.models import Video
from web.forms import RegForm, LogForm, UploadVideoForm
from web.models import User, Video
from web import ALLOWED_EXTENSIONS
from .helper import read_image
from werkzeug.utils import secure_filename
import os

def cur_user():
    if 'Login' in session:
        return User.query.get(session['Login'])
    else:
        return None


def is_auth():
    return 'Login' in session


@app.route('/images/<int:pid>.jpg')
def get_image(pid):
    image_binary = read_image(pid)
    response = make_response(image_binary)
    response.headers.set('Content-Type', 'image/jpeg')
    response.headers.set(
        'Content-Disposition', 'attachment', filename='%s.jpg' % pid)
    return response

@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template('main.html', user=cur_user())





@app.route('/video', methods=['GET', 'POST'])
def video():

    video=Video.query.id()

    return render_template('video.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/calibrate', methods=['GET', 'POST'])
def multicheck():
    return render_template('color.html', color="#FF0000")

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadVideoForm(csrf_enabled=False)
    if form.validate_on_submit():
        if 'video' not in request.files:
            return redirect(request.url)

        file = request.files['video']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['VIDEO_SAVE_PATH'], filename)
            
            file.save(path)
            video = Video(form.title.data, path)
            video.save()

            return redirect(request.url)

    return render_template('upload_video.html', form=form, user=is_auth())

@app.route('/rezult1', methods=['GET', 'POST'])
def rezult1():
    return render_template('rezult.html', pid=1, top=0, left=0, right=0, bottom=0)
@app.route('/rezult2', methods=['GET', 'POST'])
def rezult2():
    return render_template('rezult.html', pid=1, top=0, left=-400, right=0, bottom=0)

@app.route('/reg', methods=['GET', 'POST'])
def reg():
    form = RegForm()
    user = None

    if form.validate_on_submit():
        user = User(form.login_reg.data)
        user.save(form.password_reg.data)
        session["Login"] = user.login
        return redirect(url_for("main"))

    return render_template('reg.html', form=form, user=user)


@app.route('/auth', methods=['GET', 'POST'])
def log():
    form = LogForm()
    user = None

    if form.submit_log.data and form.validate_on_submit():
        user = User.get(form.login_log.data)
        session["Login"] = user.login
        return redirect(url_for("main"))

    return render_template('auth.html', form=form, user=is_auth())


@app.route('/cabinet', methods=['GET', 'POST'])
def cabinet():
    return render_template('Cabinet.html', user=is_auth())

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if 'Login' in session:
        session.pop('Login')
    return redirect('/')

@app.route('/play', methods=['GET'])
def video_play():
    return send_file('/home/mps53/Projects/HoE/video.mp4')
    
@app.route('/abcd', methods=['GET'])
def abcd():
    return render_template("video_play.html")
