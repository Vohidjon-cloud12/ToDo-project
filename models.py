
from enum import Enum
from typing import Optional
#
# class UserRole(Enum):
#     ADMIN = 'ADMIN'
#     USER = 'USER'
#     SUPERADMIN = 'SUPERADMIN'
#
# class UserStatus(Enum):
#     ACTIVE = 'ACTIVE'
#     INACTIVE = 'INACTIVE'
#     BLOCKED = 'BLOCKED'
#
# class TodoType(Enum):
#     OPTIONAL = 'optional'
#     PERSONAL = 'personal'
#     SHOPPING = 'shopping'
#
# class User:
#     def __init__(self,
#                  username: str,
#                  password: str,
#                  user_id: Optional[int] = None,
#                  role: Optional[UserRole] = None,
#                  status: Optional[UserStatus] = None,
#                  login_try_count: Optional[int] = None):
#         self.username = username
#         self.password = password
#         self.id = user_id
#         self.role = role.value if role else UserRole.USER.value
#         self.status = status.value if status else UserStatus.INACTIVE.value
#         self.login_try_count = login_try_count or 0
#
#     def __str__(self):
#         return f'{self.role} => {self.username}'
#
# class Todo:
#     def __init__(self,
#                  title: str,
#                  user_id: int,
#                  todo_type: Optional[TodoType] = None):
#         self.title = title
#         self.user_id = user_id
#         self.todo_type = todo_type.value if todo_type else TodoType.OPTIONAL.value
#
from enum import Enum
from typing import Optional

class UserRole(Enum):
    ADMIN = 'ADMIN'
    USER = 'USER'
    SUPERADMIN = 'SUPERADMIN'

class UserStatus(Enum):
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'
    BLOCKED = 'BLOCKED'

class TodoType(Enum):
    OPTIONAL = 'optional'
    PERSONAL = 'personal'
    SHOPPING = 'shopping'

class User:
    def init(self, username: str, password: str, user_id: Optional[int] = None,
                 role: Optional[UserRole] = None, status: Optional[UserStatus] = None,
                 login_try_count: Optional[int] = None):
        self.username = username
        self.password = password
        self.id = user_id
        self.role = role.value if role else UserRole.USER.value
        self.status = status.value if status else UserStatus.INACTIVE.value
        self.login_try_count = login_try_count if login_try_count is not None else 0


class Todo:
    def init(self,
                 title: str,
                 user_id: int,
                 todo_type: Optional[TodoType] = None):
        self.title = title
        self.user_id = user_id
        self.todo_type = todo_type.value if todo_type else TodoType.OPTIONAL.value
