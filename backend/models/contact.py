from sqlalchemy import Column, Integer, String
from config import db

class Contact(db.Model):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True)
    
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    telephone = Column(String(120), unique=True, nullable=False)

    profile_picture = Column(String(255), nullable=True)


    def to_dict(self):
        return {
            "id":self.id,
            "name":self.name,
            "email":self.email,
            "telephone":self.telephone,
            "profile_picture":self.profile_picture
        }
