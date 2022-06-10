from os import environ
from app.config import create_app
app = create_app()


if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5000'))
    except ValueError:
        PORT = 5000
    if PORT == '':
        PORT = 5000
    
    debug = True if HOST == 'localhost' else False
    
    app.run(HOST, PORT, debug=debug)
