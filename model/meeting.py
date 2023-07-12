from config import db

class Meeting(db.Model):
    __tablename__='meeting'
    email = db.Column(db.String, primary_key=True)
    time = db.Column(db.String)
    venue = db.Column(db.String(120))
    host = db.Column(db.String)

    def __init__(self, email, time, venue, host):
       self.email = email
       self.time = time
       self.venue = venue
       self.host = host

    def __repr__(self):
       return f"{self.email}"