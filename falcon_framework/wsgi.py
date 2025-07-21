"""
WSGI entry point for the Falcon Framework application.

This module imports the `app` object from the `controller` module,
which serves as the WSGI application callable for deployment.

Attributes:
    app: The WSGI application instance defined in the controller module.
"""
from controller import app
