from flask import url_for

from vshaurme.extensions import db
from vshaurme.models import Notification
from flask_babel import _


def commit_notification(notification):
    try:
        db.session.add(notification)
        db.session.commit()
    except:
        db.session.rollback()
        raise
    finally:
        db.session.close()


def push_follow_notification(follower, receiver):
    message = _(
        'User <a href="%(url_username)s">%(follower_username)s</a> followed you.',
        url_username=url_for('user.index', username=follower.username),
        follower_username=follower.username
    )
    notification = Notification(message=message, receiver=receiver)
    commit_notification(notification)


def push_comment_notification(photo_id, receiver, page=1):
    message = _(
        '<a href="%(url_main_show_photo)s#comments">This photo</a> has new comment/reply.',
        url_main_show_photo=url_for('main.show_photo', photo_id=photo_id, page=page)
    )
    notification = Notification(message=message, receiver=receiver)
    commit_notification(notification)


def push_collect_notification(collector, photo_id, receiver):
    message = _(
        'User <a href="%(url_username)s">%(collector_username)s</a> collected your <a href="%(url_main_show_photo)s">photo</a>',
        url_username=url_for('user.index', username=collector.username),
        collector_username=collector.username,
        url_main_show_photo=url_for('main.show_photo', photo_id=photo_id)
    )
    notification = Notification(message=message, receiver=receiver)
    commit_notification(notification)
