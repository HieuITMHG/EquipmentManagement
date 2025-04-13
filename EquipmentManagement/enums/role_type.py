from enum import Enum

class RoleType(Enum):
    STUDENT = 'Student'
    STAFF = 'Staff'
    MANAGER = 'Manager'

class RoleID(Enum):
    MANAGER = 1
    STUDENT = 2
    STAFF = 3
