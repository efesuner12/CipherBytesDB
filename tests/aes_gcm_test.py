from tkinter import StringVar

import unittest
import os

import app.operation.cryptography.aes as aes_encrypter

## Test AES GCM encryption and decryption
#
class AES_Test(unittest.TestCase):

    # Decryption function re-implemented without the EKMS
    def decrypt(self, ciphertext, key):
        try:
            byte_ciphertext = bytes.fromhex(ciphertext) if type(ciphertext) is str else ciphertext

            aad = byte_ciphertext[0:76]
            nonce = aad[0:12]
            metadata = aad[12:76].hex()
            tag = byte_ciphertext[76:92]

            dec_key = key

            decryptor = Cipher(algorithms.AES(dec_key), modes.GCM(nonce, tag), backend=default_backend()).decryptor()

            decryptor.authenticate_additional_data(aad)

            plaintext = decryptor.update(byte_ciphertext[92:])
            plaintext += decryptor.finalize()
            
            return plaintext.decode("utf-8")
        except Exception:
            error_msg.set("Operation has failed unexpectedly.\nPlease try again later")
            return None

    # Valid encryption test
    def encryption_test(self):
        nonce = aes_encrypter.generate_nonce()
        self.key = os.urandom(32)

        self.ciphertext = aes_encrypter.encrypt("test data", "test_metadata", self.key, nonce, "")
        self.assertIsNotNone(self.ciphertext)

    # Valid decryption test
    def decryption_test(self):
        plaintext = self.decrypt(self.ciphertext, self.key)
        self.assertEqual("test", plaintext)
