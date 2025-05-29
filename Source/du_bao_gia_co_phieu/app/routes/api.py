from flask import Blueprint, request, jsonify
from utils.xu_ly_du_lieu import lay_danh_sach_ma

api_bp = Blueprint("api", __name__)

@api_bp.route("/lay-ma-co-phieu")
def lay_ma():
    san = request.args.get("san")
    danh_sach = lay_danh_sach_ma(san)
    return jsonify(danh_sach)
