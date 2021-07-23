import sys

from dashboard.app import create_app

sys.path.insert(0,"/app/")

application = create_app()


def wsgi(*args, **kwargs):
    return application


if __name__ == '__main__':
    application.run(host="0.0.0.0", port="8000")
