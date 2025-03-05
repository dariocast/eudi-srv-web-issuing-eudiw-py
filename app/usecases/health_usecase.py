from flask import Blueprint, jsonify

health_usecase = Blueprint("health_usecase", __name__, url_prefix="/health")

@health_usecase.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"}), 200
