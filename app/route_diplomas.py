from flask import Blueprint, jsonify, render_template, request, session
from flask_cors import CORS
from uuid import uuid4
from datetime import datetime, timedelta
import json
import requests
import base64
import io
from urllib.parse import urlparse
import segno
from .app_config.config_service import ConfService as cfgservice
from app.data_management import oid4vp_requests


rtu_bp = Blueprint("rtu_diplomas", __name__, url_prefix="/rtu_diplomas")
CORS(rtu_bp)

@rtu_bp.route("/present", methods=["GET"])
def present_rtu_qr():
    session_id = str(uuid4())
    session["session_id"] = session_id

    input_descriptors = rtu_diplomas_input_descriptors

    nonce = str(uuid4())
    payload = json.dumps({
        "type": "vp_token",
        "nonce": nonce,
        "presentation_definition": {
            "id": "cbeb8f12-a9f0-47a0-a11e-7e22ecc5300f",
            "input_descriptors": input_descriptors
        }
    })

    url = cfgservice.dynamic_presentation_url.rstrip("/")
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, data=payload)

    if response.status_code != 200:
        return jsonify({"error": "Failed to initiate presentation"}), 500

    pres = response.json()
    oid4vp_requests[session_id] = {"response": pres, "expires": datetime.now() + timedelta(minutes=cfgservice.deffered_expiry)}

    qr_uri = f"eudi-openid4vp://{urlparse(url).netloc}?client_id={pres['client_id']}&request_uri={pres['request_uri']}"
    qrcode = segno.make(qr_uri)
    out = io.BytesIO()
    qrcode.save(out, kind='png', scale=3)
    qr_base64 = "data:image/png;base64," + base64.b64encode(out.getvalue()).decode("utf-8")

    return render_template("diplomas/rtu_login_qr_code.html", url_data=qr_uri, qrcode=qr_base64, transaction_id=pres["transaction_id"], redirect_url=cfgservice.service_url)


@rtu_bp.route("/verify", methods=["GET"])
def rtu_verification_result():
    url = cfgservice.dynamic_presentation_url
    if "response_code" in request.args and "session_id" in request.args:
        cfgservice.app_logger.info(", Session ID: " + session["session_id"] + ", " + "oid4vp flow: same_device")

        response_code = request.args.get("response_code")
        transaction_id = oid4vp_requests[request.args.get("session_id")]["response"]["transaction_id"]
        url = (
                url
                + transaction_id
                + "?nonce=hiCV7lZi5qAeCy7NFzUWSR4iCfSmRb99HfIvCkPaCLc="
                + "&response_code=" + response_code
        )

    elif "transaction_id" in request.args:
        cfgservice.app_logger.info(", Session ID: " + session["session_id"] + ", " + "oid4vp flow: cross_device")
        transaction_id = request.args.get("transaction_id")

        url = (
                url
                + transaction_id
                + "?nonce=hiCV7lZi5qAeCy7NFzUWSR4iCfSmRb99HfIvCkPaCLc="
        )

    headers = {
        "Content-Type": "application/json",
    }

    response = requests.request("GET", url, headers=headers)
    if response.status_code != 200:
        error_msg = str(response.status_code)
        return jsonify({"error": error_msg}), 400

    from app.formatter_func import cbor2elems
    mdoc = cbor2elems(response.json()["vp_token"][0] + "==")

    extracted = {}
    for doctype in mdoc:
        for attr, value in mdoc[doctype]:
            extracted[attr] = value

    return render_template("diplomas/rtu_diploma_verification_result.html", data=extracted)


@rtu_bp.route("/checkAuth", methods=["GET"])
def check_rtu_auth():
    transaction_id = request.args.get("transaction_id")
    if not transaction_id:
        return jsonify({"error": "Missing transaction_id"}), 400

    url = f"{cfgservice.dynamic_presentation_url}{transaction_id}?nonce=hiCV7lZi5qAeCy7NFzUWSR4iCfSmRb99HfIvCkPaCLc="
    headers = {"Content-Type": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        error_msg = str(response.status_code)
        return jsonify({"error": error_msg}), 500
    else:
        data = {"message": "Sucess"}
        return jsonify({"message": data}), 200


rtu_diplomas_input_descriptors = [
        {
            "id": "eu.europa.ec.eudi.rtu_diploma_mdoc",
            "name": "RTU.TITLE",
            "purpose": "",
            "format": {
                "mso_mdoc": {
                    "alg": ["ES256", "ES384", "ES512"]
                }
            },
            "constraints": {
                "fields": [
                    {"path": ["$['eu.europa.ec.eudi.rtu_diploma_mdoc']['awardingBody_countryCode']"], "intent_to_retain": False},
                    {"path": ["$['eu.europa.ec.eudi.rtu_diploma_mdoc']['awardingBody_legalName']"], "intent_to_retain": False},
                    {"path": ["$['eu.europa.ec.eudi.rtu_diploma_mdoc']['awardingBody_registration']"], "intent_to_retain": False},
                    {"path": ["$['eu.europa.ec.eudi.rtu_diploma_mdoc']['awardingDate']"], "intent_to_retain": False},
                    {"path": ["$['eu.europa.ec.eudi.rtu_diploma_mdoc']['citizenshipCountryCode']"], "intent_to_retain": False},
                    {"path": ["$['eu.europa.ec.eudi.rtu_diploma_mdoc']['creditPoint']"], "intent_to_retain": False},
                    {"path": ["$['eu.europa.ec.eudi.rtu_diploma_mdoc']['creditValue']"], "intent_to_retain": False},
                    {"path": ["$['eu.europa.ec.eudi.rtu_diploma_mdoc']['eqfLevel']"], "intent_to_retain": False},
                    {"path": ["$['eu.europa.ec.eudi.rtu_diploma_mdoc']['familyName']"], "intent_to_retain": False},
                    {"path": ["$['eu.europa.ec.eudi.rtu_diploma_mdoc']['givenName']"], "intent_to_retain": False},
                    {"path": ["$['eu.europa.ec.eudi.rtu_diploma_mdoc']['issuanceDate']"], "intent_to_retain": False},
                    {"path": ["$['eu.europa.ec.eudi.rtu_diploma_mdoc']['issued']"], "intent_to_retain": False},
                    {"path": ["$['eu.europa.ec.eudi.rtu_diploma_mdoc']['maximumDuration']"], "intent_to_retain": False},
                    {"path": ["$['eu.europa.ec.eudi.rtu_diploma_mdoc']['nationalID']"], "intent_to_retain": False},
                    {"path": ["$['eu.europa.ec.eudi.rtu_diploma_mdoc']['nqfLevel']"], "intent_to_retain": False},
                    {"path": ["$['eu.europa.ec.eudi.rtu_diploma_mdoc']['thematicArea']"], "intent_to_retain": False},
                    {"path": ["$['eu.europa.ec.eudi.rtu_diploma_mdoc']['title']"], "intent_to_retain": False},
                    {"path": ["$['eu.europa.ec.eudi.rtu_diploma_mdoc']['type']"], "intent_to_retain": False},
                    {"path": ["$['eu.europa.ec.eudi.rtu_diploma_mdoc']['validFrom']"], "intent_to_retain": False}
                ]
            }
        }
    ]

pid_diplomas_input_descriptors = [
    {
       "id":"eu.europa.ec.eudi.pid.1",
       "format":{
          "mso_mdoc":{
             "alg":[
                "ES256",
                "ES384",
                "ES512",
                "EdDSA"
             ]
          }
       },
       "constraints":{
          "limit_disclosure":"required",
          "fields":[
             {
                "path":[
                   "$['eu.europa.ec.eudi.pid.1']['family_name']"
                ],
                "intent_to_retain":False
             }
          ]
       }
    }
]