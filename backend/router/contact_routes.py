import os
import uuid
from flask import Blueprint, request, jsonify, current_app
from DAO.contact_dao import ContactDAO


contact_bp = Blueprint('contacts', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """Verifica se o arquivo tem extensão permitida."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# get contacts
@contact_bp.route('/contacts', methods=['GET'])
def get_contacts():
    contacts = ContactDAO.get_all()
    return jsonify([c.to_dict() for c in contacts]), 200

# get contact by id
@contact_bp.route('/contacts/<int:contact_id>', methods=['GET'])
def get_contact(contact_id):
    contact = ContactDAO.get_by_id(contact_id) 
    if not contact:
        return jsonify({'error': 'Contato não encontrado'}), 404
    
    return jsonify(contact.to_dict()), 200

# create contact
@contact_bp.route('/contacts', methods=['POST'])
def create_contact():
    data = request.form.to_dict()
    file = request.files.get('profile_picture')

    if not data.get('name') or not data.get('email') or not data.get('telephone'):
        return jsonify({'error': 'Dados obrigatórios não fornecidos'}), 400

    if file:
        if not allowed_file(file.filename):
            return jsonify({'error': 'File extension not allowed'}), 400

        ext = file.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{ext}"
        upload_folder = os.path.join(current_app.root_path, 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, unique_filename)

        try:
            file.save(filepath)
        except Exception:
            return jsonify({'error': 'Failed to save file'}), 500

        data['profile_picture'] = f'uploads/{unique_filename}'
    else:
        data['profile_picture'] = None

    contact = ContactDAO.create(data)
    return jsonify(contact.to_dict()), 201

# update contact
@contact_bp.route('/contacts/<int:contact_id>', methods=['PUT'])
def update_contact(contact_id):
    data = request.form.to_dict()
    file = request.files.get('profile_picture')

    contact = ContactDAO.get_by_id(contact_id)
    if not contact:
        return jsonify({'error': 'Contato não encontrado'}), 404

    if file:
        if not allowed_file(file.filename):
            return jsonify({'error': 'File extension not allowed'}), 400

        ext = file.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{ext}"
        upload_folder = os.path.join(current_app.root_path, 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, unique_filename)

        try:
            file.save(filepath)
        except Exception:
            return jsonify({'error': 'Failed to save file'}), 500

        # Remove imagem anterior, se existir
        if contact.profile_picture:
            old_path = os.path.join(current_app.root_path, contact.profile_picture.split('?')[0])
            try:
                if os.path.exists(old_path):
                    os.remove(old_path)
            except Exception:
                pass

        data['profile_picture'] = f'uploads/{unique_filename}'

    updated_contact = ContactDAO.update(contact_id, data)
    return jsonify(updated_contact.to_dict()), 200

# delete contact
@contact_bp.route('/contacts/<int:contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    success = ContactDAO.delete(contact_id)
    if not success:
        return jsonify({'error': 'Contato não encontrado'}), 404
    
    return jsonify({'message': 'Contato deletado com sucesso'}), 200