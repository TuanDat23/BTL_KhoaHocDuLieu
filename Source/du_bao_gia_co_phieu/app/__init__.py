from flask import Flask

def tao_ung_dung():
    app = Flask(__name__)

    from app.routes.trang_chu import trang_chu_bp
    from app.routes.du_bao import du_bao_bp
    from app.routes.api import api_bp

    app.register_blueprint(trang_chu_bp)
    app.register_blueprint(du_bao_bp)
    app.register_blueprint(api_bp)

    return app