import cython

from libc.stdlib cimport free, malloc
from libc.string cimport strlen


cdef extern from "crypt_wrapper.h":
    void _encrypt_into(const char * unencrypted, char * encrypted)
    void _decrypt_into(const char * encrypted, char * unencrypted)

cdef void _decrypt(const char *encrypted, char **unencrypted, Py_ssize_t *length):
    cdef Py_ssize_t n = strlen(encrypted)
    unencrypted[0] = <char *> malloc((n + 1) * sizeof(char))
    if not unencrypted[0]:
        return  # malloc failed
    _decrypt_into(encrypted, unencrypted[0] )
    length[0] = n

cdef void _encrypt(const char *unencrypted, char** encrypted, Py_ssize_t *length):
    cdef Py_ssize_t n = strlen(unencrypted)
    encrypted[0] = <char *> malloc((n + 1) * sizeof(char))
    if not encrypted[0]:
        return  # malloc failed
    _encrypt_into(unencrypted, encrypted[0])
    length[0] = n

def encrypt(string: str) -> bytes:
    cdef char* encrypted = NULL
    cdef Py_ssize_t length = 0
    _encrypt(string.encode('utf-8'), &encrypted, &length)
    try:
        return encrypted[:length]
    finally:
        free(encrypted)

def decrypt(string: bytes) -> str:
    cdef char* unencrypted = NULL
    cdef Py_ssize_t length = 0
    _decrypt(string, &unencrypted, &length)
    try:
        return unencrypted[:length].decode('utf-8')
    finally:
        free(unencrypted)
