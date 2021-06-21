import base64
import hmac
import json
import time
import requests


def push_text(msg, webhook: str, secret: str):
    t = str(round(time.time() * 1000))
    secret_enc = secret.encode('utf-8')
    string_to_sign_enc = '{}\n{}'.format(t, secret).encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod="SHA256").digest()
    sign = base64.b64encode(hmac_code).decode("utf-8")

    url = "{}&timestamp={}&sign={}".format(webhook, t, sign)
    data = {
        "msgtype": "text",
        "text": {
            "content": "[cloud189app-action]"+msg
        }
    }
    data = json.dumps(data).encode("utf-8")
    headers = {"Content-Type": "application/json"}

    return requests.post(url, data=data, headers=headers).json()['errmsg']
