import hashlib 

class User:
  def __init__(self, _id='', username='', password=''):
    self._id = _id
    self.username = username
    hash_password = (hashlib.sha256(password.encode())).hexdigest()
    self.hash_password = hash_password

  def to_dict(self):
    return {
      '_id': self._id,
      'username': self.username,
      'hash_password': self.hash_password
    }

  def from_dict(self, dict: dict):
    self._id = dict.get('_id', self._id)
    self.username = dict.get('username', '')
    self.hash_password = dict.get('hash_password', '')
    return self

  def check_password(self, password: str):
    check_password = (hashlib.sha256(password.encode())).hexdigest()
    if self.hash_password == check_password:
      return True
    else:
      return False

login_user_json_schema = {
  'type': 'object',
  'properties': {
    'username': {'type': 'string'},
    'password': {'type': 'string'}
  },
  'required': ['username', 'password']
}

register_user_json_schema = {
  'type': 'object',
  'properties': {
    'username': {'type': 'string'},
    'password': {'type': 'string'}
  },
  'required': ['username', 'password']
}