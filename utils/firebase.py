import pyrebase

config = {
    "apiKey": "AIzaSyB0dprdh8FV_Guv0XO6dSsJWIFun4a2q2w",
    "authDomain": "clean-5777.firebaseapp.com",
    "databaseURL": "https://clean-5777-default-rtdb.firebaseio.com/",
    "storageBucket": "clean-5777.firebasestorage.app",
    "projectId": "clean-5777",
    "messagingSenderId": "939914991169",
    "appId": "1:939914991169:web:9bf59dc176fa3af01798c0",
    "measurementId": "G-GMWWRTVFBM"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()