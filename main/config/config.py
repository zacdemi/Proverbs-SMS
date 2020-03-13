import os

SECRET_KEY = os.environ.get('SECRET_KEY')
WTF_CSRF_SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = True

MONGO_PW = os.environ.get('MONGO_PW')
MONGO_URI = f"mongodb+srv://zacdemi:{MONGO_PW}@cluster0-qrc2l.mongodb.net/get_proverbs?retryWrites=true&w=majority"
