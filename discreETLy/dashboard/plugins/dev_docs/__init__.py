from flask import Blueprint
from flask import render_template

base_path = '/dev_docs'
tab_name = 'Dev docs'
plugin = Blueprint('dev_docs', __name__, template_folder='templates')

@plugin.route('/')
def index():
    return render_template('dev_docs/index.html')