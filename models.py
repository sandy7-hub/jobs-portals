from flask_sqlalchemy import SQLAlchemy
import models

db = SQLAlchemy()

class User (db.Model) :
    
    
    id = db.Column( db.Integer, primary_key = True , autoincrement = True )
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    email_id = db.Column(db.String(100))


class Application (db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    company = db.Column(db.String(100))
    description = db.Column(db.String(500))
    salary = db.Column(db.Float)
    
class Post (db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    job_id = db.Column(db.Integer)
    your_name = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))
    email = db.Column(db.String(100))
    address = db.Column(db.String(200))
    location = db.Column(db.String(100))
    resume = db.Column(db.String(200)) 
    

    
