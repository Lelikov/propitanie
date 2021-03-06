import base64
import hashlib


def get_raw_signature(params):
    chunks = []

    for key in sorted(params.keys()):
        if key == 'signature':
            continue

        value = params[key]

        if isinstance(value, str):
            value = value.encode('utf8')
        else:
            value = str(value).encode('utf-8')

        if not value:
            continue

        value_encoded = base64.b64encode(value)
        chunks.append('%s=%s' % (key, value_encoded.decode()))

    raw_signature = '&'.join(chunks)
    return raw_signature


'''Двойное шифрование sha1 на основе секретного ключа'''


def double_sha1(secret_key, data):
    sha1_hex = lambda s: hashlib.sha1(s.encode('utf-8')).hexdigest()
    digest = sha1_hex(secret_key + sha1_hex(secret_key + data))
    return digest


'''Вычисляем подпись (signature). Подпись считается на основе склеенной строки из отсортированного массива параметров, исключая из расчета пустые поля и элемент "signature" '''


def get_signature(secret_key: str, params: dict) -> str:
    return double_sha1(secret_key, get_raw_signature(params))
