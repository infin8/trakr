USERNAME="trakr"
PASSWORD="trakr"

import bottle

def login():
    username = bottle.request.forms.get('username')
    password = bottle.request.forms.get('password')
    
    if username == USERNAME and password == PASSWORD:
        bottle.response.set_cookie('auth', str(hash(username+password)))
        return True
    
    return False

def check():
    key = bottle.request.get_cookie('auth')
    if key == str(hash(USERNAME+PASSWORD)):
        return key
    
def authenticated(f, *args, **kwargs):
    def decorator(*args, **kwargs):
        key = check()
        if key:
            return f(*args, user=key, **kwargs)
            
        bottle.redirect('/login')
        
    return decorator

login_form = """
<form method="POST">
    <input type="text" name="username" />
    <input type="password" name="password" />
    <input type="submit" name="submit" value="login" />
</form>
"""
