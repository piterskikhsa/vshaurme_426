import os
import hmac
import subprocess


from flask import Blueprint, request, abort, jsonify, json, current_app
from flask_login import login_required
from flask_babel import _
from flask_wtf import CSRFProtect

from vshaurme.decorators import admin_required, permission_required
from vshaurme.extensions import db
from vshaurme.forms.admin import EditProfileAdminForm
from vshaurme.models import Role, User, Tag, Photo, Comment
from vshaurme.utils import redirect_back

api_bp = Blueprint('api', __name__)
csrf = CSRFProtect(current_app)


@api_bp.route('/hook', methods=['POST'])
@csrf.exempt
def hook():
    key = os.environ['API_TOKEN']
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    command = os.path.join(basedir, 'deploy.sh')

    def sig_blob(body):
        return 'sha1={}'.format(hmac.new(key.encode(), body, digestmod='sha1')
                                .hexdigest())

    received_sig = request.headers.get('x-hub-signature')
    computed_sig = sig_blob(request.data)

    if received_sig != computed_sig:
        return abort(404)

    ref = json.loads(request.data).get('ref')
    if ref and 'master' not in ref:
        return abort(404)

    subprocess.call(command, stdout=subprocess.PIPE, shell=True)

    return jsonify({'success': True}), 200, {'ContentType': 'application/json'}
