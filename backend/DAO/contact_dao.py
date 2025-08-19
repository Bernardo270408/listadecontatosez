from models.contact import Contact
from config import db

class ContactDAO:
    def get_all():
        return Contact.query.all()

    def get_by_id(contact_id):
        return Contact.query.get(contact_id)

    def get_by_email(email):
        return Contact.query.filter_by(email=email).first()

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
        contact.name = data.get('name', contact.name)
        contact.email = data.get('email', contact.email)
        contact.telephone = data.get('telephone', contact.telephone)
        contact.profile_picture = data.get('profile_picture', contact.profile_picture)
        db.session.commit()
        return contact

    def delete(contact_id):
        contact = Contact.query.get(contact_id)
        if not contact:
            return False
        db.session.delete(contact)
        db.session.commit()
        return True
    