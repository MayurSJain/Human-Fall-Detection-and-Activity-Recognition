# firebase_config.py
import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate('=your firebase credentials')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'yout firebasse url'
})
