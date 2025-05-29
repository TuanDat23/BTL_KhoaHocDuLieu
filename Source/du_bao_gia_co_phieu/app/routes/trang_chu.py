from flask import Blueprint, render_template

trang_chu_bp = Blueprint('trang_chu', __name__)

@trang_chu_bp.route('/')
def trang_chu():
    return render_template('trang_chu.html')
