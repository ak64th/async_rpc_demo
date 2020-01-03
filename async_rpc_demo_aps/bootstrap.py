if __name__ == '__main__':
    from waitress import serve

    from .db import metadata
    from .wsgi import wsgi_application
    from .scheduler import scheduler

    metadata.create_all()
    scheduler.start()
    serve(wsgi_application, host='0.0.0.0', port=8000)
