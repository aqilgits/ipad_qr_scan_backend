from config import db

class Visitor(db.Model):
    __tablename__='visitor'
    ic = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    image = db.Column(db.String(120))

    def __init__(self, ic, name, email, image):
       self.ic = ic
       self.name = name
       self.email = email
       self.image = image

    def __repr__(self):
       return f"{self.ic}"
