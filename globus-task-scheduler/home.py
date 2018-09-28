"""Blueprint for home
"""
from flask import Blueprint, render_template

from .util.transfer import Transfer

bp = Blueprint('home', __name__, url_prefix='/')


@bp.route('/')
def home():
    t = Transfer()
    endpoints = [{'name': e['display_name'], 'id': e['id']} for e in t.endpoints]
    return render_template('index.html', endpoints=endpoints)
