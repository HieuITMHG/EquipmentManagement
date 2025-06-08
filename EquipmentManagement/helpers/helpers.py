from functools import wraps
from flask import redirect, session, flash
from datetime import datetime, time
from services.account_service import AccountService

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("account_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def get_expect_returning_time():
    """ Xác định expect_returning_time dựa trên giờ mượn """
    now = datetime.now().time()  # Lấy giờ hiện tại

    if time(6, 0) <= now <= time(10, 25):
        return datetime.combine(datetime.today(), time(10, 25))
    elif time(12, 25) <= now <= time(16, 0):
        return datetime.combine(datetime.today(), time(16, 0))
    elif time(17, 0) <= now <= time(20, 0):
        return datetime.combine(datetime.today(), time(20, 0))
    else:
        return datetime.combine(datetime.today(), time(20, 0))

def role_required(*roles):
    """
    Decorator to check if the current user has the required role(s)
    Usage: @role_required(RoleType.ADMIN.value, RoleType.EMPLOYEE.value)
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not session.get("account_id"):
                return redirect("/login")
                
            current_account = AccountService.get_account_by_person_id(session.get("account_id"))
            if not current_account:
                session.clear()
                return redirect("/login")
                
            if current_account["vai_tro_id"] not in roles:
                flash("you do not have access to this side!", "error")
                return redirect("/login")
                
            return f(*args, **kwargs)
        return decorated_function
    return decorator