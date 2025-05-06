import pytest
from flask import g, session
from flaskr.db import get_db
from flaskr.constants import (
  USER_REGISTERED_SUCCESSFULLY, 
  USER_ALREADY_REGISTERED,
  USERNAME_REQUIRED, 
  PASSWORD_REQUIRED,
  USER_LOGGED_IN_SUCCESSFULLY,
  USERNAME_NOT_FOUND,
  INCORRECT_PASSWORD
)

def test_register(client, app):
  response = client.post(
    '/auth/register',
    data={ 'username': 'aristide', 'password': 'mypassword' }
  )
  
  assert response.status_code == 201
  assert response.get_json() == {"message": USER_REGISTERED_SUCCESSFULLY}
  
  with app.app_context():
    user =  get_db().execute(
      "SELECT * FROM users WHERE username = 'aristide'"
    ).fetchone()
    assert user is not None
    assert user['username'] == 'aristide'
    

@pytest.mark.parametrize(('username', 'password', 'message'), (
  ('', '', USERNAME_REQUIRED),
  ('newuser', '', PASSWORD_REQUIRED),
  ('test', 'test', USER_ALREADY_REGISTERED.format(username='test')),
))
def test_register_validate_input(client, username, password, message):
  # Test invalid registration inputs
  response = client.post(
    '/auth/register',
    data={ 'username': username, 'password': password }
  )
  assert response.status_code == 400
  assert response.get_json() == {"error": message}
  
  
def test_login(client, auth):
  # Test successfull login
  response = client.post(
    '/auth/login',
    data={ 'username': 'test', 'password': 'test'}
  )
  assert response.status_code == 200
  assert response.get_json() == { 'message': USER_LOGGED_IN_SUCCESSFULLY }
  
  # Verify is session not set
  with client:
    client.get('/')
    assert session['user_id'] == 1
    assert g.user['username'] == 'test'
    
@pytest.mark.parametrize(('username', 'password', 'message'), (
  ('', '', USERNAME_NOT_FOUND),
  ('wrong', 'test', USERNAME_NOT_FOUND),
  ('test', 'wrong', INCORRECT_PASSWORD),
))
def test_login_validate_input(client, username, password, message):
  # Test invalid inputs
  response = client.post(
    '/auth/login',
    data={ 'username': username, 'password': password }
  )
  
  assert response.status_code == 400
  assert response.get_json() == { 'error': message }
