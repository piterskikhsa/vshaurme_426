from flask import render_template, flash, redirect, url_for, current_app, request, Blueprint
from flask_login import login_required, current_user, fresh_login_required, logout_user
from flask.json import jsonify

from vshaurme.extensions import oauth


vkoauth_bp = Blueprint('vk', __name__)


def vk_compliance_fix(session):
    def _token_response(resp):
        token = resp.json()
        token['token_type'] = 'Bearer'
        resp.json = lambda: token
        return resp

    session.register_compliance_hook('access_token_response', _token_response)


vk = oauth.register(
    name='vk',
    api_base_url='https://api.vk.com/method/',
    access_token_url='https://oauth.vk.com/access_token',
    authorize_url='https://oauth.vk.com/authorize',
    client_kwargs={
            'token_placement': 'uri',
            'token_endpoint_auth_method': 'client_secret_post',
            'scope': ["photos", "groups", "wall", "email"]
        },
    compliance_fix=vk_compliance_fix
)

@vkoauth_bp.route('/login')
def login():
    redirect_uri = url_for('.authorize', _external=True)
    return vk.authorize_redirect(redirect_uri)

@vkoauth_bp.route('/authorize')
def authorize():
    token = vk.authorize_access_token()
    # we can save the token into database
    return jsonify(token)
