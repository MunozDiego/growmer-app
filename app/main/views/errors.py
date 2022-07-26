from flask import render_template
from app.main import main

@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('505.html'), 500
