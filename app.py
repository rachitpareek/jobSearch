import os
from application import app, db
from application.models import User, Post


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

    
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}
