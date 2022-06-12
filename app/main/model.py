import firebase_admin
from firebase import Firebase
from firebase_admin import firestore
from datetime import datetime as dt, timedelta as td
import json
from app.config import FIREBASE_CREDENTIALS



#initialize firebase
auth = Firebase(FIREBASE_CREDENTIALS).auth()
db = Firebase(FIREBASE_CREDENTIALS).database()
fire_app = firebase_admin.initialize_app(options=FIREBASE_CREDENTIALS)
fire_client = firestore.client(fire_app)





class User:
    def __init__(self, data):
        self.json_data = data
        self.data = json.dumps(data)
        self.uid = data['uid']
        self.email = data.get('email') or ''
        self.display_name = data.get('displayName') or ''
        self.anonymous = data.get('isAnonymous') or True
        self.photo_url = data.get('photoURL') or ''
        self.tokens = data.get('stsTokenManager')
        self.refresh_token = data['stsTokenManager']['refreshToken']
        self.access_token = data['stsTokenManager']['accessToken']
        self.expiration_time = data['stsTokenManager']['expirationTime']
        self.update_db()
        self.read_profile()

    def update_db(self):
        data = {
            'uid': self.uid,
            'email': self.email,
            'displayName': self.display_name,
            'photoURL': self.photo_url            
        }
        fire_client.collection(u'users').document(self.uid).set(data, merge=True)


    def read_profile(self):
        users_ref = fire_client.collection(u'users').document(self.uid)
        doc = users_ref.get()
        data = doc.to_dict()
        self.first_name = data.get('firstName') or ''
        self.last_name = data.get('lastName') or ''
        self.contact_email = data.get('contactEmail') or ''
        self.phone = data.get('phone') or ''
    
    def save_profile(self):
        data = {
            'firstName': self.first_name,
            'lastName': self.last_name,
            'contactEmail': self.contact_email,
            'phone': self.phone            
        }
        fire_client.collection(u'users').document(self.uid).set(data, merge=True)

    def get_user(data):
        try:
            data = json.loads(data)
            user = User(data)
        except:
            user = None
        return user

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        try:
            if self.expiration_time > dt.timestamp(dt.now()) * 1000:
                return True
            else:
                new_tokens = dict(auth.refresh(self.refresh_token))
                self.access_token = new_tokens["idToken"]
                self.refresh_token = new_tokens["refreshToken"]
                self.expiration_time = dt.timestamp(dt.now() + td(minutes=60)) * 1000
                return True
        except:
            print('Error refreshing tokens')
            return False


    @property
    def is_anonymous(self):
        return self.anonymous

    def get_id(self):
        try:
            return self.data
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

