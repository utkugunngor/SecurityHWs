import requests
import time
import hmac
import hashlib
import requests
import json
import sys
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Cryptodome.Hash import SHA256,SHA1
from Cryptodome.Signature import pss
import base64
import jwt
import datetime

def register():
    message = "utkuGungorSecKey".encode("utf-8")
    key = RSA.importKey(open('gradecoin.pub').read())
    cipher = PKCS1_OAEP.new(key,hashAlgo=SHA256)
    ciphertext = cipher.encrypt(message)
    encrypted=base64.b64encode(ciphertext).decode('utf-8')

    iv = "initVectorTemp24".encode("utf-8")
    encrypted_iv=base64.b64encode(iv).decode('utf-8')

    url_reg="https://gradecoin.xyz/register"
    data = '{"student_id": "e223747","passwd": "8LAeHrsjnwXh59Q","public_key": "-----BEGIN PUBLIC KEY-----MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCsz333GMkQWSdD9g+e6lB3jgLxUb0xnq7NOZBui0+LIlmq4xz95jDmHu1OaEe9t3Q+wZ1KOV2gJBwgmesL3Jx5PajaSSoV7vjYrNHqICvhGjz1DlLfdOg1tAHPgiIsF+dcO8exF+/k7R4sUuDwBxPKaBtWsu4I/2tyyZ0urbLNMQIDAQAB-----END PUBLIC KEY-----"}'
    auth_request = '{"c": "u5xnMPlc2kj30DszHxO6ohQHgrCKGhqh9MEL49USiI9u1ZhlTRmCkAeoxrRvcNYfrFWo/vl1ZuqdHEvGhzZBLngwa/URU2qk46WGG/JUrcdak2XeuY2SlWC00zW/hZ19HPe1nPPWUg+y2jgvK1UtQKnlsNKK1+bHe+NTdZ6xsSRRLGzsAPuIeaGgjCA3FiVGk7HkA4GTXPhZZqlhVKBjZUsf5Fzk//0Icp4TBPIB64MaUto8ajDpvSThIhhM5zBwRbeYSX/1S056vCTeMrqJjDYQULRQrC/lcXfBXNEo1Eqmff9pBsE8LmsSXr/bPaZqMzou/Nttv7+Ct5tmqw0/KtFiBjQHLiHHjC56qDSmVfqF4mbmuRYMS9oLuLok1PSGC153n2W4hY0kj8I0hDgxQuSqIvEWxx7B8NV5b5RsiGih2lp68MggE/Ohj7ScUJHcHsIdXSTLT2wW5ayoi4z9wQ==","iv":"%s","key":"%s"}'% (encrypted_iv, encrypted)
    response = requests.post(url_reg,auth_request)
    print(response.text)

def transaction(dest):
    
    transaction = {
        "source":identifier,
        "target":dest,
        "amount":2,
        "timestamp":datetime.datetime.now().replace(microsecond=0).isoformat()
    }
    
    tr_hash = hashlib.md5(json.dumps(transaction, separators=(',', ':')).encode())

    payload = {
        "tha": tr_hash.hexdigest(),
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }

    encodedJWT = jwt.encode(payload, priKey, algorithm="RS256")
    header = {"Authorization": "Bearer " + encodedJWT}
    #print(encodedJWT)
    url_trans = "https://gradecoin.xyz/transaction"
    
    #Somehow I am getting "invalid signature, so I was not able to implement block mining part"
    t1 = requests.post(url_trans, headers = header, data=json.dumps(transaction))
    print(t1.text)

if __name__ == "__main__":
    
    #register()

    #x = requests.get('https://gradecoin.xyz/user')
    #print(x.text)

    priKey = "-----BEGIN RSA PRIVATE KEY-----\nMIICWwIBAAKBgQCsz333GMkQWSdD9g+e6lB3jgLxUb0xnq7NOZBui0+LIlmq4xz95jDmHu1OaEe9t3Q+wZ1KOV2gJBwgmesL3Jx5PajaSSoV7vjYrNHqICvhGjz1DlLfdOg1tAHPgiIsF+dcO8exF+/k7R4sUuDwBxPKaBtWsu4I/2tyyZ0urbLNMQIDAQABAoGAMws+6+PYUAnlfT+LMaeIiSfbWqiIN8XlYB0mumBP6IsG7WEUSTLbMr3j3osS1ckAfyD1ct0q+Ihx/nc4ZFKPrQtmjrG/0Z0ug2LPvyL5KCjKZkb/3APeAa9B4dYvxW0ZeTnrdEoGRohc34DS0X3F0222z8w1VmZehe6BL2sMmyECQQDnSHjaSqMc/JmB3LeIcCFvlFjRS0+faSldZgcQ46it6nPEob4o3+Vl20kEuTFK+4NtkKGv/huDnRAAlPNZuRwtAkEAv0dOQOXOANMp9vGuO3mwxssBoBsRW8BNyGyi6Ql2NFZhekljS8/MjXwSjBg3H3JEchaTbybNI+4scgbN9VBjlQJAS3jgxwsYEztytGfcFE/S+WBFY3bZ8sEUWIAUyjQgNTCOupm1Pg1iBEz8lOgB5+APUU+jE5UuUVKNiEMS7jJzuQJAWvoMUzu6LpRBGm47A5jOps65mDAnom8lz9Uz6wkQCranKGWtb8qHLSg9HhsKZM+RlH3+Y9idq6BFzXpFDY/NvQJAGN8ANK9I5vdtDYYzACWq0folJRiopi1G3NACDAr0f8dTFSlCGX8ItaQuHM/bJk4dop4ToAXfTEwFyW5vCX6w4g==\n-----END RSA PRIVATE KEY-----"
    identifier = "aeb39ffcde7fb7971f1c7a30ff7a86eccaa9ae2b9043cbb56f50412105023ac1"
    dest1 = "53acd2e0ce05d3965140a9a46e53a6fe7774109b79d3f88b5fe996ef8a23cfad"
    transaction(dest1)
    


