import os
import hmac
import subprocess

from flask import Blueprint, request, abort, jsonify, json, current_app

from vshaurme.decorators import admin_required, permission_required
from vshaurme.extensions import csrf
from vshaurme.forms.admin import EditProfileAdminForm
from vshaurme.models import Role, User, Tag, Photo, Comment
from vshaurme.utils import redirect_back


api_bp = Blueprint('api', __name__)


@api_bp.route('/hook', methods=['POST'])
@csrf.exempt
def hook():
    key = os.getenv('API_TOKEN')
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    command = os.path.join(basedir, 'deploy.sh')

    signature = request.headers.get('X-Hub-Signature')
    sha, signature = signature.split('=')

    secret = str.encode(key)

    hashhex = hmac.new(secret, request.data, digestmod='sha1').hexdigest()
    if hmac.compare_digest(hashhex, signature):
        subprocess.call(command, stdout=subprocess.PIPE, shell=True)
        return jsonify({'success': True}), 200
    return jsonify({'error': True}), 400
