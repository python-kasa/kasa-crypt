import json
import struct

from kasa_crypt import decrypt, encrypt

# from
# https://github.com/python-kasa/python-kasa/blob/master/kasa/tests/test_protocol.py

PLAIN_TEXT_STRING = (
    "\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n"
    "\x0b"
    "\x0c"
    "\r"
    "\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c"
    "\x1d"
    "\x1e"
    "\x1f "
    "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f\x80\x81\x82\x83\x84\x85"
    "\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0"
    "¡¢£¤¥¦§¨©ª«¬"
)
ENCRYPTED_BYTE_WITH_NULLS = (
    b"\x00\x00\x00\xad\xab\xaa\xa8\xab\xaf\xaa\xac\xab\xa3\xaa\xa0\xab"
    b"\xa7\xaa\xa4\xab\xbb\xaa\xb8\xab\xbf\xaa\xbc\xab\xb3\xaa\xb0\xab"
    b"\xb7\xaa\xb4\xab\x8b\xaa\x88\xab\x8f\xaa\x8c\xab\x83\xaa\x80\xab"
    b"\x87\xaa\x84\xab\x9b\xaa\x98\xab\x9f\xaa\x9c\xab\x93\xaa\x90\xab"
    b"\x97\xaa\x94\xab\xeb\xaa\xe8\xab\xef\xaa\xec\xab\xe3\xaa\xe0\xab"
    b"\xe7\xaa\xe4\xab\xfb\xaa\xf8\xab\xff\xaa\xfc\xab\xf3\xaa\xf0\xab"
    b"\xf7\xaa\xf4\xab\xcb\xaa\xc8\xab\xcf\xaa\xcc\xab\xc3\xaa\xc0\xab"
    b"\xc7\xaa\xc4\xab\xdb\xaa\xd8\xab\xdf\xaa\xdc\xab\xd3\xaa\xd0\xab"
    b"\xd7\xaa\xd4\xabi\xe9+\xaah\xea(\xabi\xed/\xaah\xee,\xabi\xe1#\xaah\xe2 \xab"
    b"i\xe5'\xaah\xe6$\xabi\xf9;\xaah\xfa8\xabi\xfd?\xaah\xfe<\xabi\xf13\xaa"
    b"h\xf20\xabi\xf57\xaah\xf64\xabi\xc9\x0b\xaah\xca\x08\xabi\xcd\x0f\xaa"
    b"h\xce\x0c\xabi\xc1\x03\xaah\xc2\x00\xabi\xc5"
)


def test_encrypt_json():
    d = json.dumps({"foo": 1, "bar": 2})
    encoded = d.encode("utf-8")
    encrypted = encrypt(d)
    # encrypt adds a 4 byte header
    assert struct.unpack(">I", encrypted[:4])[0] == len(encoded)
    encrypted = encrypted[4:]
    assert d == decrypt(encrypted)


def test_encrypt_utf8_json():
    d = json.dumps({"漢字": 1, "bar": 2})
    encoded = d.encode("utf-8")
    encrypted = encrypt(d)
    # encrypt adds a 4 byte header
    assert struct.unpack(">I", encrypted[:4])[0] == len(encoded)
    encrypted = encrypted[4:]
    assert d == decrypt(encrypted)


def test_encrypt_utf8():
    d = "漢字"
    encoded = d.encode("utf-8")
    encrypted = encrypt(d)
    # encrypt adds a 4 byte header
    assert struct.unpack(">I", encrypted[:4])[0] == len(encoded)
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


def test_decrypt_real_device():
    input = (
        b"\xd0\xf2\x81\xf8\x8b\xff\x9a\xf7\xd5\xef\x94\xb6\xd1\xb4\xc0\x9f"
        b"\xec\x95\xe6\x8f\xe1\x87\xe8\xca\xf0\x8b\xa9\xda\xad\xf2\x84\xe1"
        b"\x93\xb1\x8b\xa9\x98\xb6\x86\xa8\x9a\xba\xf8\x8d\xe4\x88\xec\xcc"
        b"\xfe\xcf\xff\xce\xfe\xcb\xeb\xb9\xdc\xb0\x9e\xaf\x99\xac\x95\xa6"
        b"\x9e\xbc\x90\xb2\xda\xad\xf2\x84\xe1\x93\xb1\x8b\xa9\x98\xb6\x86"
        b"\xa4\x88\xaa\xc7\xa8\xcc\xa9\xc5\xe7\xdd\xff\xba\xea\xde\xee\xc6"
        b"\x93\xc0\xe9\xcb\xe7\xc5\xa1\xc4\xb2\xdb\xb8\xdd\x94\xf0\xd2\xe8"
        b"\xca\xf2\xc2\xf2\xc4\xf6\xc5\xf4\xb1\x80\xb4\x8d\xb4\xf6\xb7\xf4"
        b"\xc0\x84\xb0\xf2\xb1\x86\xc3\x85\xc6\x82\xb6\xf4\xc4\xf3\xc6\xf7"
        b"\xcf\xfe\xbb\x8d\xbe\x87\xb4\xf2\xc0\xe2\xce\xec\x83\xe6\x8b\xc2"
        b"\xa6\x84\xbe\x9c\xae\xe8\xd1\xe3\xd2\xe7\xa1\x90\xd4\x97\xd5\x93"
        b"\xa4\xe0\xa3\x92\xa5\xe3\xdb\xeb\xae\x9c\xde\xee\xad\xec\xaf\xeb"
        b"\xdf\xe8\xae\xed\xcf\xe3\xc1\xa9\xde\x97\xf3\xd1\xeb\xc9\x8b\xb8"
        b"\xfa\xcd\x8f\xbf\x8a\xc8\xff\xca\xf2\xb1\x82\xc7\x83\xc2\xfa\xbc"
        b"\x85\xc6\xf0\xc9\x8f\xca\x89\xcd\x8f\xce\xfc\xcd\xfc\xcd\xef\xc3"
        b"\xe1\x93\xe0\x93\xfa\xd8\xe2\xcf\xfb\xcb\xe7\xc5\xa9\xc8\xbc\xd5"
        b"\xa1\xd4\xb0\xd5\x8a\xe3\xc1\xfb\xc9\xf0\xc7\xff\xca\xf8\xd4\xf6"
        b"\x9a\xf5\x9b\xfc\x95\xe1\x94\xf0\x95\xca\xa3\x81\xbb\x96\xaf\x9a"
        b"\xae\x9e\xa9\x9a\xb6\x94\xf5\x99\xf0\x91\xe2\xc0\xfa\xd8\x8c\xdc"
        b"\xf1\xbd\xf4\xba\xf1\xae\xfd\x90\xf1\x83\xf7\xd7\x87\xeb\x9e\xf9"
        b"\xa6\x96\xa6\x92\xd4\xf6\xda\xf8\x8b\xff\x9e\xea\x9f\xec\xce\xf4"
        b"\xd6\xb8\xdd\xaa\x88\xa4\x86\xeb\x82\xe1\xbe\xca\xb3\xc3\xa6\x84"
        b"\xbe\x9c\xd5\x9a\xce\xe0\xb3\xfe\xbf\xed\xb9\xe9\xa5\xf0\xb7\xe4"
        b"\xb3\xfa\xae\xed\xa5\x87\xab\x89\xef\x8a\xeb\x9f\xea\x98\xfd\xdf"
        b"\xe5\xc7\x93\xda\x97\xb5\x99\xbb\xd6\xb7\xd4\xf6\xcc\xee\xab\x93"
        b"\xa9\x9d\xa5\x9f\xdd\xe5\xdf\xee\xab\x91\xa1\x91\xab\x9f\xd9\xfb"
        b"\xd7\xf5\x80\xf0\x94\xf5\x81\xe8\x86\xe1\xc3\xf9\xc9\xe5\xc7\xab"
        b"\xce\xaa\xf5\x9a\xfc\x9a\xb8\x82\xb2\x9e\xbc\xdf\xb7\xde\xb2\xd6"
        b"\xa4\xc1\xaf\x8d\xb7\xec\x97\xb5\xdc\xb8\x9a\xa0\x82\xb2\x82\xa0"
        b"\x8c\xae\xdd\xa9\xc8\xbc\xd9\xfb\xc1\xf0\xdc\xfe\x9f\xf3\x9a\xfb"
        b"\x88\xaa\x90\xb2\xe8\x87\xea\x88\xe1\x84\xa6\x8a\xa8\xc7\xa9\xf6"
        b"\x82\xeb\x86\xe3\xc1\xfb\xcf\xf8\xc8\xe4\xc6\xa8\xcd\xb5\xc1\x9e"
        b"\xff\x9c\xe8\x81\xee\x80\xa2\x98\xe3\xc1\xb5\xcc\xbc\xd9\xfb\xc1"
        b"\xec\xdd\xa0\xdd\xf1\x8a\xa8\xc1\xa5\x87\xbd\x9f\xaf\x9e\xbc\x90"
        b"\xb2\xc1\xb5\xd4\xa0\xc5\xe7\xdd\xec\xc0\xe2\x83\xef\x86\xe7\x94"
        b"\xb6\x8c\xae\xe3\x82\xe5\x8c\xef\xcd\xe1\xc3\xac\xc2\x9d\xe9\x80"
        b"\xed\x88\xaa\x90\xa1\x96\xa2\x8e\xac\xc2\xa7\xdf\xab\xf4\x95\xf6"
        b"\x82\xeb\x84\xea\xc8\xf2\x89\xab\xdf\xa6\xd6\xb3\x91\xab\x86\xb7"
        b"\xca\xb7\xea\xc6\xe4\x87\xef\x86\xea\x8e\xd1\xbf\xca\xa7\x85\xbf"
        b"\x8d\xa1\x83\xed\x99\xfa\xa5\xd6\xa2\xc3\xb7\xd2\xf0\xca\xfa\xd6"
        b"\xf4\x91\xe3\x91\xce\xad\xc2\xa6\xc3\xe1\xdb\xeb\x96\xeb\x96"
    )
    decrypted = decrypt(input)
    assert (
        decrypted == '{"system":{"get_sysinfo":{"sw_ver":"1.0.2 Build 210105'
        ' Rel.165938","hw_ver":"1.0","model":"EP40(US)","deviceId":"8006231E1499BAC4D4BC7EFCD4B075181E6393F2","oemId":"2F9215F1DCBF7DC17F80E2B0CACD47FC","hwId":"B3B7B05B758C3EDA8F9C69FECDBA2111","rssi":-40,"latitude_i":297852,"longitude_i":-954073,"alias":"TP-LINK_Smart'
        ' Plug_004F","status":"new","mic_type":"IOT.SMARTPLUGSWITCH","feature":"TIM","mac":"E8:48:B8:1E:00:4F","updating":0,"led_off":0,"children":[{"id":"00","state":1,"alias":"Zombie","on_time":470,"next_action":{"type":-1}},{"id":"01","state":1,"alias":"Magic","on_time":174,"next_action":{"type":-1}}],"child_num":2,"ntc_state":0,"err_code":0}}}'
    )


def test_roundtrip_with_nulls():
    assert decrypt(ENCRYPTED_BYTE_WITH_NULLS[4:]) == PLAIN_TEXT_STRING


def test_encrypt_with_nulls():
    string_with_nulls = b"this\x00has\x00nulls".decode()
    assert (
        encrypt(string_with_nulls)
        == b"\x00\x00\x00\x0e\xdf\xb7\xde\xad\xad\xc5\xa4\xd7\xd7\xb9\xcc\xa0\xcc\xbf"
    )
    assert decrypt(encrypt(string_with_nulls)[4:]) == string_with_nulls


def test_encrypt_round_decreasing_size():
    for i in range(0, 128):
        payload = bytes([i] * i).decode()
        assert decrypt(encrypt(payload)[4:]) == payload

    for i in range(127, 0, -1):
        payload = bytes([i] * i).decode()
        assert decrypt(encrypt(payload)[4:]) == payload
