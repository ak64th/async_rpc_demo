from spyne.server.wsgi import WsgiApplication
from .app import application as spyne_app

wsgi_application = WsgiApplication(spyne_app)

if __name__ == '__main__':
    from waitress import serve

    serve(wsgi_application, host='0.0.0.0', port=8000)
