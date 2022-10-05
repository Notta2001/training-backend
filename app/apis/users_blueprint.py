import uuid

from sanic import Blueprint
from sanic.response import json

from app.constants.cache_constants import CacheConstants
from app.databases.redis_cached import get_cache, set_cache
from app.databases.mongodb import MongoDB
from app.hooks.error import ApiBadRequest
from app.models.user import login_user_json_schema, register_user_json_schema
from app.decorators.json_validator import validate_with_jsonschema
from app.hooks.error import ApiInternalError, ApiBadRequest
from app.utils.jwt_utils import generate_jwt
from app.models.user import User

users_bp = Blueprint('users_blueprint', url_prefix='/users')

_db = MongoDB()

@users_bp.route('/')
async def get_all_users(request):
  async with request.app.ctx.redis as r:
    users = await get_cache(r, CacheConstants.all_users)
    if users is None:
      users_obj = _db.get_users()
      users = [users.to_dict() for user in users_obj]
      await set_cache(r, CacheConstants.all_users, users)

    users_obj = _db.get_users()
    users = [users.to_dict() for user in users_obj]
    number_of_users = len(users)
    return json({
        'n_users': number_of_users,
        'users': users
    })

@users_bp.route('/login', methods={'POST'})
@validate_with_jsonschema(login_user_json_schema)
async def login(request):
  body = request.json
  username = body.get('username', '')
  password = body.get('password', '')

  user_obj = _db.get_user_by_username(username)
  if not user_obj:
    raise ApiBadRequest('User: Not found!')
  
  if user_obj.check_password(password):
    jwt = generate_jwt(username)
    return json({
      'username': user_obj.username,
      'jwt': jwt
    })
  else:
    raise ApiBadRequest('User: Password is incorrect!')

@users_bp.route('/register', methods={'POST'})
@validate_with_jsonschema(register_user_json_schema)
async def register(request):
  body = request.json

  _id = str(uuid.uuid4())
  username = body.get('username')
  password = body.get('password')

  user = User(_id, username, password)

  user_obj = _db.get_user_by_username(username)
  if user_obj:
    raise ApiBadRequest('User: Already exists!')

  inserted = _db.create_user(user)
  if not inserted:
    raise ApiInternalError('User: Creat fail!')
  
  return json({
    'status': 'success',
    'user': user.to_dict()
  })

