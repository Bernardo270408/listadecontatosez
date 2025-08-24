from models.contact import Contact
from config import db

class ContactDAO:
    def get_all():
        return Contact.query.all()

    def get_by_id(contact_id):
        return Contact.query.get(contact_id)

    def get_by_email(email):
        return Contact.query.filter_by(email=email).first()
    
    def get_by_telephone(telephone):
        return Contact.query.filter_by(telephone=telephone).first()
    
    def get_by_name(name):
        return Contact.query.filter(Contact.name.ilike(f'%{name}%')).all()

    def create(data):
        contact = Contact(
            name=data.get('name'),
            email=data.get('email'),
            telephone=data.get('telephone'),
            profile_picture=data.get('profile_picture')
        )
        db.session.add(contact)
        db.session.commit()
        return contact

    def update(contact_id, data):
        contact = Contact.query.get(contact_id)
        if not contact:
            return None
        contact.update_from_dict(data)
        db.session.commit()
        return contact

    def delete(contact_id):
        contact = Contact.query.get(contact_id)
        if not contact:
            return False
        db.session.delete(contact)
        db.session.commit()
        return True
    