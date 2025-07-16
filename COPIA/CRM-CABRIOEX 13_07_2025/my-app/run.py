# Declarando nombre de la aplicación e inicializando, crear la aplicación Flask
from app import create_app

app = create_app()

# Ejecutando el objeto Flask
if __name__ == '__main__':
    app.run(debug=True, port=5600)