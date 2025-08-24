import os
from flask import Flask, send_from_directory, redirect, url_for
from flask_cors import CORS
from config import Config
from config import db
from flask_migrate import Migrate

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    os.makedirs(os.path.dirname(Config.DB_PATH), exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)

    CORS(app, supports_credentials=True)

    from router import contact_routes

    app.register_blueprint(contact_routes.contact_bp)

    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        return send_from_directory(os.path.join(app.root_path, 'uploads'), filename)
    
    @app.route('/')
    def index():
        return redirect(url_for('contacts.get_contacts'))
    
    return app

if __name__ == '__main__':
    app = create_app()

    app.run(debug=True)
    
        