from app import app, db
from app.models import User
from app.api.errors import bad_request, error_response
from flask import jsonify, url_for, request, g, abort
# from app.api.auth import token_auth


@app.route('/api/users/<int:id>', methods=['GET'])
def get_user(id):
    if g.user.id != id:
        abort(403)
    return jsonify(User.query.get_or_404(id).to_dict())