import os
import random

import imageio
import numpy as np
from scipy import ndimage

from PIL import Image
from faker import Faker
from flask import current_app
from sqlalchemy.exc import IntegrityError

from vshaurme.extensions import db
from vshaurme.models import User, Photo, Tag, Comment, Notification

fake = Faker()


def fake_admin():
    admin = User(name='Grey Li',
                 username='greyli',
                 email='admin@helloflask.com',
                 bio=fake.sentence(),
                 website='http://greyli.com',
                 confirmed=True)
    admin.set_password('helloflask')
    notification = Notification(message='Hello, welcome to Vshaurme.', receiver=admin)
    db.session.add(notification)
    db.session.add(admin)
    db.session.commit()


def fake_user(count=10):
    for user_number in range(count):
        user = User(name=fake.name(),
                    confirmed=True,
                    username=fake.profile()['username'],
                    bio=fake.sentence(),
                    location=fake.city(),
                    website=fake.url(),
                    email=fake.ascii_email())
        user.set_password('123456')
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_follow(count=30):
    for _ in range(count):
        user = User.query.get(random.randint(1, User.query.count()))
        user.follow(User.query.get(random.randint(1, User.query.count())))
    db.session.commit()


def fake_tag(count=20):
    for tag_number in range(count):
        tag = Tag(name=fake.slug())
        db.session.add(tag)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_photo(count=30):
    # photos
    upload_path = current_app.config['VSHAURME_UPLOAD_PATH']
    for photo_number in range(count):
        filename = 'random_%d.jpg' % photo_number
        # TODO: generate image
        n, l = 10, 256
        im = np.zeros((l, l))
        points = l * np.random.random((2, n ** 2))
        im[(points[0]).astype(np.int), (points[1]).astype(np.int)] = 1
        im = ndimage.gaussian_filter(im, sigma=l / n)
        mask = (im > im.mean()).astype(np.float)
        mask += 0.1 * im
        img = mask + 0.2 * np.random.randn(*mask.shape)
        imageio.imsave(os.path.join(upload_path,filename), img)
        photo = Photo(
            description=fake.text(),
            filename=filename,
            filename_m=filename,
            filename_s=filename,
            author=User.query.get(random.randint(1, User.query.count())),
            timestamp=fake.date_time_this_year()
        )

        # tags
        for j in range(random.randint(1, 5)):
            tag = Tag.query.get(random.randint(1, Tag.query.count()))
            if tag not in photo.tags:
                photo.tags.append(tag)

        db.session.add(photo)
    db.session.commit()


def fake_collect(count=50):
    for i in range(count):
        user = User.query.get(random.randint(1, User.query.count()))
        user.collect(Photo.query.get(random.randint(1, Photo.query.count())))
    db.session.commit()


def fake_comment(count=100):
    for i in range(count):
        comment = Comment(
            author=User.query.get(random.randint(1, User.query.count())),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            photo=Photo.query.get(random.randint(1, Photo.query.count()))
        )
        db.session.add(comment)
    db.session.commit()
