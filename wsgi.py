from flask import Flask
from CTFd import create_app

app = create_app()

# Relevant documents:
# http://werkzeug.pocoo.org/docs/middlewares/
# http://flask.pocoo.org/docs/patterns/appdispatch/
from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware
app.config['DEBUG'] = True
# Load a dummy app at the root URL to give 404 errors.
# Serve app at APPLICATION_ROOT for localhost development.
application = DispatcherMiddleware(Flask('dummy_app'), {
    '/ctf': app,
})
run_simple('localhost', 4000, application, use_reloader=True)
