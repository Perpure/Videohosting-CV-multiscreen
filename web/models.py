﻿# coding=utf-8
import shutil
import hashlib
import os
import json
from datetime import datetime
from uuid import uuid4
from flask import url_for
from web import db, app, avatars, backgrounds


Views = db.Table('Views', db.Model.metadata,
                 db.Column('User_id', db.Integer, db.ForeignKey('User.id')),
                 db.Column('Video_id', db.String(32), db.ForeignKey('Video.id')))

Likes = db.Table('Likes', db.Model.metadata,
                 db.Column('User_id', db.Integer, db.ForeignKey('User.id')),
                 db.Column('Video_id', db.String(32), db.ForeignKey('Video.id')))

Dislikes = db.Table('Dislikes', db.Model.metadata,
                    db.Column('User_id', db.Integer, db.ForeignKey('User.id')),
                    db.Column('Video_id', db.String(32), db.ForeignKey('Video.id')))


class Comment(db.Model):
    __tablename__ = 'Comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text())
    video_id = db.Column(db.Text(), db.ForeignKey('Video.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

    def __init__(self, text, video_id, user_id):
        self.text = text
        self.user_id = user_id
        self.video_id = video_id

    def save(self):
        db.session.add(self)
        db.session.commit()


class Tag(db.Model):
    __tablename__ = 'Tag'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text())
    video_id = db.Column(db.Text(), db.ForeignKey('Video.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

    def __init__(self, text, video_id, user_id):
        self.text = text
        self.user_id = user_id
        self.video_id = video_id

    def save(self):
        db.session.add(self)
        db.session.commit()


class Video(db.Model):
    __tablename__ = 'Video'
    id = db.Column(db.String(32), primary_key=True)
    title = db.Column(db.String(140), nullable=False)
    path = db.Column(db.String(256), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    user_login = db.Column(db.String)

    longitude = db.Column(db.Float(), nullable=True)
    latitude = db.Column(db.Float(), nullable=True)

    likes = db.relationship('User', secondary=Likes, backref='likes', lazy='joined')
    dislikes = db.relationship('User', secondary=Dislikes, backref='dislikes', lazy='joined')

    comments = db.relationship('Comment', backref='video', lazy='joined')

    tags = db.relationship('Tag', backref='video', lazy='joined')

    viewers = db.relationship('User', secondary=Views, backref='views', lazy='joined')

    geotags = db.relationship("Geotag", backref="video", lazy="joined")

    def __init__(self, title):
        self.title = title

    def save(self, hash, user):
        self.date = datetime.now(tz=None)
        self.id = hashlib.md5((hash + self.date.isoformat()).encode("utf-8")).hexdigest()
        self.path = os.path.join(app.config['VIDEO_SAVE_PATH'], self.id)
        self.user_id = user.id
        self.user_login = user.login

        db.session.add(self)
        db.session.commit()

        return self.path

    def add_viewer(self, user):
        self.viewers.append(user)

        db.session.add(self)
        db.session.commit()

    def add_like(self, user):
        self.likes.append(user)
        db.session.add(self)
        db.session.commit()

    def add_dislike(self, user):
        self.dislikes.append(user)
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get(search=None, sort=None, video_id=None):
        if video_id:
            return Video.query.get(video_id)

        videos = Video.query.all()

        if sort:
            sort = sort.lower()
            if "date" in sort:
                videos.sort(key=lambda video: video.date, reverse=True)
            if "views" in sort:
                videos.sort(key=lambda video: len(video.viewers), reverse=True)

        if search:
            if '#' in search:
                temp = [(video, len([word for word in search.split('#')
                                     if word.lower() in video.get_tags()])) for video in videos]
            else:
                temp = [(video, len([word for word in search.lower().split()
                                     if word in video.title.lower()])) for video in videos]

            temp = [item for item in temp if item[1] > 0]
            temp.sort(key=lambda item: item[1], reverse=True)
            videos = [item[0] for item in temp]

        return videos

    def get_tags(self):
        tags = []
        for tag in self.tags:
            tags.append(tag.text.lower())
        return tags

    def add_geotag(self, coords):
        self.latitude = coords[0]
        self.longitude = coords[1]

        db.session.add(self)
        db.session.commit()

    def delete_video(self):
        shutil.rmtree(self.path)
        db.session.delete(self)
        db.session.commit()


class Geotag(db.Model):
    __tablename__ = "Geotag"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    video_id = db.Column(db.String(32), db.ForeignKey("Video.id"), nullable=False)

    def __init__(self, longitude, latitude):
        self.longitude = longitude
        self.latitude = latitude

    def save(self, video):
        self.date = datetime.now()
        self.video_id = video.id

        db.session.add(self)
        db.session.commit()


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    name = db.Column(db.String(32), nullable=False)
    channel_info = db.Column(db.String(64))
    avatar = db.Column(db.String(128))
    background = db.Column(db.String(128))
    action = db.Column(db.String(64))
    color = db.Column(db.String(64))
    top = db.Column(db.Integer)
    left = db.Column(db.Integer)
    res_k = db.Column(db.Integer)

    videos = db.relationship("Video",
                             backref="user",
                             lazy="joined")

    comments = db.relationship('Comment',
                               backref='user',
                               lazy='joined')
    tags = db.relationship('Tag',
                           backref='user',
                           lazy='joined')

    def __init__(self, login):
        self.login = login
        self.name = login
        self.channel_info = "Заполните информацию о канале"

    def save(self, password):
        self.password = hashlib.sha512(
            password.encode("utf-8")).hexdigest()
        db.session.add(self)
        db.session.commit()

    def check_pass(self, password):
        hash = hashlib.sha512(password.encode("utf-8")).hexdigest()
        return self.password == hash

    def change_name(self, name):
        self.name = name
        db.session.add(self)
        db.session.commit()

    def change_channel_info(self, info):
        self.channel_info = info
        db.session.add(self)
        db.session.commit()

    def update_action(self, action):
        self.action = action
        db.session.add(self)
        db.session.commit()

    def update_avatar(self, avatar):
        self.avatar = avatar
        db.session.add(self)
        db.session.commit()

    def update_background(self, background):
        self.background = background
        db.session.add(self)
        db.session.commit()

    def avatar_url(self):
        if self.avatar:
            avatar_json = json.loads(self.avatar)
            return url_for('_uploads.uploaded_file', setname=avatars.name, filename=avatar_json['url'])
        else:
            return '../static/avatar.jpg'

    def background_url(self):
        if self.background:
            background_json = json.loads(self.background)
            return url_for('_uploads.uploaded_file', setname=backgrounds.name, filename=background_json['url'])
        else:
            return '../static/background.jpg'

    @staticmethod
    def get(id=None, login=None):
        if login:
            return User.query.filter_by(login=login).first()
        if id:
            return User.query.get(id)
        return User.query.all()


class Room(db.Model):
    __tablename__ = 'Room'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime, nullable=False)
    video_id = db.Column(db.String(32))
    capitan_id = db.Column(db.String(), db.ForeignKey('AnonUser.id'))
    name = db.Column(db.String(64), nullable=False)
    devices_in_room = db.relationship('RoomDeviceColorConnector', backref='room', lazy=True)

    def __init__(self, name, capitan_id):
        self.name = name
        self.capitan_id = capitan_id
        self.date = datetime.now(tz=None)

    def save(self, vid):
        self.video_id = vid
        db.session.add(self)
        db.session.commit()

    def get_format_date(self):
        return self.date.strftime("%H:%M %d.%m.%Y")

    def get_devices(self):
        raw_users = RoomDeviceColorConnector.query.filter_by(room=self)
        return [rac.anon for rac in raw_users]

    @staticmethod
    def get(id=None, name=None):
        if name:
            return Room.query.filter_by(name=name).first()
        if id:
            return Room.query.get(id)
        return Room.query.all()


class Color(db.Model):
    __tablename__ = 'Color'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    color = db.Column(db.String(64), nullable=False)
    anons_rooms = db.relationship('RoomDeviceColorConnector', backref='color', lazy=True)

    @staticmethod
    def get(id=None):
        if id:
            return Color.query.get(id)
        return Color.query.all()


class RoomDeviceColorConnector(db.Model):
    __tablename__ = 'RoomDeviceColorConnector'
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('Room.id'))
    anon_id = db.Column(db.String(), db.ForeignKey('AnonUser.id'))
    color_id = db.Column(db.Integer, db.ForeignKey('Color.id'))


class AnonUser(db.Model):
    __tablename__ = 'AnonUser'
    id = db.Column(db.String(), primary_key=True)
    action = db.Column(db.String(64))
    time = db.Column(db.Integer)
    device_width = db.Column(db.Integer)
    device_height = db.Column(db.Integer)
    color = db.Column(db.String(64))
    top = db.Column(db.Integer)
    left = db.Column(db.Integer)
    res_k = db.Column(db.Integer)
    rooms_colors = db.relationship('RoomDeviceColorConnector', backref='anon', lazy=True)
    room_capitan = db.relationship("Room", backref='captain')

    def __init__(self):
        self.id = str(uuid4())
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get(id=None):
        if id:
            return AnonUser.query.get(id)
        return AnonUser.query.all()

    def update_resolution(self, width, height):
        if self.device_width == width and self.device_height == height:
            return()
        self.device_height = height
        self.device_width = width
        db.session.add(self)
        db.session.commit()
