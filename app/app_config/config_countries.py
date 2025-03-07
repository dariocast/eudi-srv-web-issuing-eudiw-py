# coding: latin-1
###############################################################################
# Copyright (c) 2023 European Commission
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
###############################################################################
"""
The PID Issuer Web service is a component of the PID Provider backend. 
Its main goal is to issue the PID in cbor/mdoc (ISO 18013-5 mdoc) and SD-JWT format.

This config_countries.py contains configuration data related to the countries supported by the PID Issuer. 

NOTE: You should only change it if you understand what you're doing.
"""

from .config_service import ConfService as cfgserv


class ConfCountries:
    urlReturnEE = "https://pprpid.provider.eudiw.projj.eu/tara/redirect"

    formCountry = "FC"
    unisaCountry = "IT"
    # supported countries
    supported_countries = {
        unisaCountry: {
            "name": "University of Salerno",
            "pid_mdoc_privkey": "api_docs/test_tokens/DS-token/PID-DS-0002/PID-DS-0002.pid-ds-0002.key.pem",
            "pid_mdoc_privkey_passwd": b'pid-ds-0002',  # None or bytes
            "pid_mdoc_cert": "api_docs/test_tokens/DS-token/PID-DS-0002/PID-DS-0002.cert.der",
            "un_distinguishing_sign": "IT",
            "supported_credentials": [
                "it.unisa.credentials.elm_mdoc"
            ],
            "dynamic_R2": cfgserv.service_url + "dynamic/form_R2",
        },
        formCountry: {
            "name": "FormEU",
            "pid_url": cfgserv.service_url + "pid/form",
            "pid_mdoc_privkey": "api_docs/test_tokens/DS-token/PID-DS-0002/PID-DS-0002.pid-ds-0002.key.pem",
            # "pid_mdoc_privkey": "/etc/eudiw/pid-issuer/privkey/hackathon-DS-0001_UT.pem",
            # "pid_mdoc_privkey": 'app\certs\PID-DS-0001_UT.pem',
            "pid_mdoc_privkey_passwd": b'pid-ds-0002',  # None or bytes
            "pid_mdoc_cert": "api_docs/test_tokens/DS-token/PID-DS-0002/PID-DS-0002.cert.der",
            # "pid_mdoc_cert": "/etc/eudiw/pid-issuer/cert/hackathon-DS-0001_UT_cert.der",
            "un_distinguishing_sign": "FC",
            "supported_credentials": [
                "eu.europa.ec.eudi.pid_mdoc",
                "eu.europa.ec.eudi.pid_jwt_vc_json",
                "eu.europa.ec.eudi.mdl_mdoc",
                "eu.europa.ec.eudi.over18_mdoc",
                "eu.europa.ec.eudi.loyalty_mdoc",
                "eu.europa.ec.eudi.pseudonym_over18_mdoc",
                "eu.europa.ec.eudi.pseudonym_over18_mdoc_deferred_endpoint",
                "eu.europa.ec.eudi.photoid",
                "eu.europa.ec.eudi.por_mdoc",
                "eu.europa.ec.eudi.iban_mdoc",
                "eu.europa.ec.eudi.hiid_mdoc",
                "eu.europa.ec.eudi.tax_mdoc",
                "eu.europa.ec.eudi.msisdn_mdoc"
            ],
            "dynamic_R2": cfgserv.service_url + "dynamic/form_R2",
        },
    }
