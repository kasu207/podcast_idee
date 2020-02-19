from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self): 
        #The __repr__ method tells Python how to print objects of this class, 
        #which is going to be useful for debugging.
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.passwor_hash, password)

#https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database

@login.user_loader
def load_user(id):
    return user.query.get(int(id))