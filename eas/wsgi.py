"""wsgi endpoint to run on a server"""
from eas import factories
app = factories.create_app()
