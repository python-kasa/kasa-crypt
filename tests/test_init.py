import json

from kasa_crypt import decrypt, encrypt

# from
# https://github.com/python-kasa/python-kasa/blob/master/kasa/tests/test_protocol.py


def test_encrypt():
    d = json.dumps({"foo": 1, "bar": 2})
    encrypted = encrypt(d)
    # encrypt adds a 4 byte header
    encrypted = encrypted[4:]
    assert d == decrypt(encrypted)


def test_encrypt_unicode():
    d = "{'snowman': '\u2603'}"

    e = bytes(
        [
            208,
            247,
            132,
            234,
            133,
            242,
            159,
            254,
            144,
            183,
            141,
            173,
            138,
            104,
            240,
            115,
            84,
            41,
        ]
    )

    encrypted = encrypt(d)
    # encrypt adds a 4 byte header
    encrypted = encrypted[4:]

    assert e == encrypted


def test_decrypt_unicode():
    e = bytes(
        [
            208,
            247,
            132,
            234,
            133,
            242,
            159,
            254,
            144,
            183,
            141,
            173,
            138,
            104,
            240,
            115,
            84,
            41,
        ]
    )

    d = "{'snowman': '\u2603'}"

    assert d == decrypt(e)


def test_roundtrip():
    d = json.dumps({"foo": 1, "bar": 2}) * 2048
    encrypted = encrypt(d)
    assert isinstance(encrypted, bytes)
    decrypted = decrypt(encrypted[4:])
    assert isinstance(decrypted, str)
    assert d == decrypted
