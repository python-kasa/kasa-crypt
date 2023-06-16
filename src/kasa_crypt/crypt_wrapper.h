

#include <stdint.h>
#include <stdio.h>
#include <string.h>


void _encrypt_into(const char * unencrypted, char * encrypted) {
    uint8_t unencrypted_byte;
    uint8_t key = 171;
    for(unsigned i = 0; i <= strlen(unencrypted); i++) {
        unencrypted_byte = unencrypted[i];
        key = key ^ unencrypted_byte;
        encrypted[i] = key;
    }
}
void _decrypt_into(const char * encrypted, char * unencrypted) {
    uint8_t unencrypted_byte;
    uint8_t encrypted_byte;
    uint8_t key = 171;
    for(unsigned i = 0; i <= strlen(encrypted); i++) {
        encrypted_byte = encrypted[i];
        unencrypted_byte = key ^ encrypted_byte;
        key = encrypted_byte;
        unencrypted[i] = unencrypted_byte;
    }
}
