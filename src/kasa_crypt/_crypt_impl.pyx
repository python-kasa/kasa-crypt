import cython

from libc.stdlib cimport malloc
from libc.string cimport strlen


cdef extern from "crypt_wrapper.h":
    void _encrypt_into(const char * unencrypted, char * encrypted)
    void _decrypt_into(const char * encrypted, char * unencrypted)

cdef char* _decrypt(const char *encrypted):
    cdef Py_ssize_t n = strlen(encrypted)
    cdef char* unencrypted = <char *> malloc((n + 1) * sizeof(char))
    if not unencrypted:
        return NULL  # malloc failed
    _decrypt_into(encrypted, unencrypted)
    return unencrypted[:n]

cdef char* _encrypt(const char *unencrypted):
    cdef Py_ssize_t n = strlen(unencrypted)
    cdef char* encrypted = <char *> malloc((n + 1) * sizeof(char))
    if not encrypted:
        return NULL  # malloc failed
    _encrypt_into(unencrypted, encrypted)
    return encrypted[:n]

def encrypt(string: str) -> bytes:
    return _encrypt(string.encode('utf-8'))


def decrypt(string: bytes) -> str:
    return _decrypt(string).decode('utf-8')
