from struct import pack


def encrypt(string: str) -> bytes:
    """Encrypt."""
    unencrypted = bytearray(string.encode())
    key = 171
    unencrypted_len = len(unencrypted)
    encrypted = bytearray(unencrypted_len)
    for idx, unencryptedbyte in enumerate(unencrypted):
        key = key ^ unencryptedbyte
        encrypted[idx] = key
    return pack(">I", unencrypted_len) + encrypted


def decrypt(string: bytes) -> str:
    """Decrypt."""
    key = 171
    result = bytearray(len(string))
    for idx, i in enumerate(string):
        a = key ^ i
        key = i
        result[idx] = a
    return result.decode()
