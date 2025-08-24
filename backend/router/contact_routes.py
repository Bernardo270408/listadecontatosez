import os
import uuid
from flask import Blueprint, request, render_template, redirect, url_for, flash, current_app
from DAO.contact_dao import ContactDAO


contact_bp = Blueprint('contacts', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Verifica se o arquivo tem extensão permitida.
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# get contacts (list)
@contact_bp.route('/contacts', methods=['GET'])
def get_contacts():
    contacts = ContactDAO.get_all()
    return render_template('list.html', contacts=contacts)

# search for contacts
@contact_bp.route('/contacts/search', methods=['GET'])
def search_contacts():
    query = request.args.get('q')
    
    if not query:
        return redirect(url_for('contacts.get_contacts'))

    by_name = ContactDAO.search_by_name(query)
    by_email = ContactDAO.search_by_email(query)
    by_telephone = ContactDAO.search_by_telephone(query)

    contacts = set(by_name + by_email + by_telephone)
    contacts = [c for c in contacts if c]

    return render_template('list.html', contacts=contacts)

# get contact by id (detail)
@contact_bp.route('/contacts/<int:contact_id>', methods=['GET'])
def get_contact(contact_id):
    contact = ContactDAO.get_by_id(contact_id)
    if not contact:
        flash('Contato não encontrado', 'danger')
        return redirect(url_for('contacts.get_contacts'))
    return render_template('detail.html', contact=contact)


# create contact (GET/POST)
@contact_bp.route('/contacts/create', methods=['GET', 'POST'])
def create_contact():
    if request.method == 'POST':
        data = request.form.to_dict()
        file = request.files.get('profile_picture')

        if not data.get('name') or not data.get('email') or not data.get('telephone'):
            flash('Dados obrigatórios não fornecidos', 'danger')
            return render_template('create.html')

        if file and file.filename:
            if not allowed_file(file.filename):
                flash('Extensão de arquivo não permitida', 'danger')
                return render_template('create.html')

            ext = file.filename.rsplit('.', 1)[1].lower()
            unique_filename = f"{uuid.uuid4().hex}.{ext}"
            upload_folder = os.path.join(current_app.root_path, 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            filepath = os.path.join(upload_folder, unique_filename)

            try:
                file.save(filepath)
            except Exception:
                flash('Falha ao salvar o arquivo', 'danger')
                return render_template('create.html')

            data['profile_picture'] = f'uploads/{unique_filename}'
        else:
            data['profile_picture'] = None

        contact = ContactDAO.create(data)
        flash('Contato criado com sucesso!', 'success')
        return redirect(url_for('contacts.get_contacts'))
    return render_template('create.html')


# update contact (GET/POST)
@contact_bp.route('/contacts/<int:contact_id>/edit', methods=['GET', 'POST'])
def update_contact(contact_id):
    contact = ContactDAO.get_by_id(contact_id)
    if not contact:
        flash('Contato não encontrado', 'danger')
        return redirect(url_for('contacts.get_contacts'))

    if request.method == 'POST':
        data = request.form.to_dict()
        file = request.files.get('profile_picture')

        if file and file.filename:
            if not allowed_file(file.filename):
                flash('Extensão de arquivo não permitida', 'danger')
                return render_template('edit.html', contact=contact)

            ext = file.filename.rsplit('.', 1)[1].lower()
            unique_filename = f"{uuid.uuid4().hex}.{ext}"
            upload_folder = os.path.join(current_app.root_path, 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            filepath = os.path.join(upload_folder, unique_filename)

            try:
                file.save(filepath)
            except Exception:
                flash('Falha ao salvar o arquivo', 'danger')
                return render_template('edit.html', contact=contact)

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
        flash('Contato atualizado com sucesso!', 'success')
        return redirect(url_for('contacts.get_contacts'))

    return render_template('edit.html', contact=contact)


# delete contact (POST)
@contact_bp.route('/contacts/<int:contact_id>/delete', methods=['POST'])
def delete_contact(contact_id):
    success = ContactDAO.delete(contact_id)
    if not success:
        flash('Contato não encontrado', 'danger')
    else:
        flash('Contato deletado com sucesso!', 'success')
    return redirect(url_for('contacts.get_contacts'))