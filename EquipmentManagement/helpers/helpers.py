from functools import wraps
from flask import redirect, session
from datetime import datetime, time

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
        return None  # Nếu ngoài khung giờ, không cho mượn