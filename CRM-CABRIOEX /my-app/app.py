from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = '97110c78ae51a45af397b6534caef90ebb9b1dcb3380f008f90b23a5d1616bf1bc29098105da20fe'

    with app.app_context():
        # Importando los Blueprints
        from routers.router_login import login_bp
        from routers.router_home import home_bp
        from routers.router_page_not_found import page_not_found

        # Registrando los Blueprints en la aplicación
        app.register_blueprint(login_bp)
        app.register_blueprint(home_bp)
        app.register_error_handler(404, page_not_found)

    return app
