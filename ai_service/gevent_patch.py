from gevent import monkey

# Apply gevent monkey patching globally before any other imports.
# This patches standard library modules like socket, ssl, threading, etc.
monkey.patch_all()
