from enum import Enum

class RoleType(Enum):
    STUDENT = 'Student'
    STAFF = 'Staff'
    MANAGER = 'Manager'

class RoleID(Enum):
    STUDENT = 3
    STAFF = 2
    MANAGER = 1
