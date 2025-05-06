import functools

from flask import (
    Blueprint, g, jsonify, request, session
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db
from flaskr.constants import (
    USER_REGISTERED_SUCCESSFULLY, USER_ALREADY_REGISTERED,
    USERNAME_REQUIRED, PASSWORD_REQUIRED,
    USERNAME_NOT_FOUND, INCORRECT_PASSWORD,
    USER_LOGGED_IN_SUCCESSFULLY
)


bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['POST'])
def register():
  username, password = request.form['username'], request.form['password']
  db = get_db()
  error = None
  
  if not username:
    error = USERNAME_REQUIRED
  
  elif not password:
    error = PASSWORD_REQUIRED
    
  if error is None:
    try:
      db.execute(
        "INSERT INTO users (username, password) values (?, ?)",
        (username, generate_password_hash(password))
      )
      db.commit()
    except db.IntegrityError:
      error = USER_ALREADY_REGISTERED.format(username=username)
      return jsonify({"error": error}), 400
    else:
      return jsonify({"message": USER_REGISTERED_SUCCESSFULLY}), 201
    
  return jsonify({"error": error}), 400
  
  

@bp.route('/login', methods=['POST'])
def login():
  username, password = request.form['username'], request.form['password']
  db = get_db()
  error = None
  user = db.execute(
    'SELECT * FROM users WHERE username = ?', (username,)
  ).fetchone()
  
  if user is None:
    error = USERNAME_NOT_FOUND
  elif not check_password_hash(user['password'], password):
    error = INCORRECT_PASSWORD
    
  if error is None:
    session.clear()
    session['user_id'] = user['user_id']
    
    
    # return response with 200 OK status
    return jsonify({"message": USER_LOGGED_IN_SUCCESSFULLY}), 200
  
  # return the error retrieved
  return jsonify({"error": error}), 400


@bp.before_app_request
def load_logged_in_user():
  user_id = session.get('user_id')
  
  if user_id is None:
    g.user = None
  else:
    g.user = get_db().execute(
      'SELECT * FROM users WHERE user_id = ?', (user_id, )
    ).fetchone()
    