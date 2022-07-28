import os

class Config(object):
    # define SECRET KEY "secret_string" can be a real secret
    # to avoid hackers attacking code or cookies
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'\x87<\xe0Pk\xebY_\xf1\x03 pZ\xf5\x1c\x96'
    
    #MONGODB_SETTINGS = { 'db' : 'UTA_Enrollment' }

    
    