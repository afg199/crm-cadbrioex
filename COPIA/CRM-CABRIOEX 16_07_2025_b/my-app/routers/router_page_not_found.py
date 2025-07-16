from flask import Blueprint, request, session, redirect, url_for

page_not_found_bp = Blueprint('page_not_found_bp', __name__)

def page_not_found(error):
    if 'conectado' in session and request.method == 'GET':
        return redirect(url_for('login_bp.inicio'))
    else:
        return redirect(url_for('login_bp.inicio'))
