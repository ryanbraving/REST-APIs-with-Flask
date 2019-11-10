from werkzeug.security import safe_str_cmp
from models.user import UserModel

# users = [
#     User(1, 'bob', 'test')
# ]
# users = [
#     {
#         'id': 1,
#         'username': 'bob',
#         'password': 'test',
#     }
# ]

# username_mapping = {u.username: u for u in users}

# username_mapping = {
#     'bob': {
#         'id': 1,
#         'username': 'bob',
#         'password': 'test',
#     }
# }

# userid_mapping = {u.id: u for u in users}
# userid_mapping = {
#     1: {
#         'id': 1,
#         'username': 'bob',
#         'password': 'test',
#     }
# }


def authenticate(username, password):
    # user = username_mapping.get(username, None)
    user = UserModel.find_by_username(username)
    # if user and user.password == password:
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    # return userid_mapping.get(user_id, None)
    return UserModel.find_by_id(user_id)
