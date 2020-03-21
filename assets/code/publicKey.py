#!/usr/bin/env python3
import base64
from cryptography.fernet import Fernet
import numpy as np
np.random.seed(0)

# Prime number
Q = 23

class Person():
    def __init__(self, name):
        self.name = name
        self.privKey = np.random.randint(low=0, high=Q)

    def getPubKey(self):
        return np.power(2, self.privKey) % Q
    
    def encrypt(self, message, recipientPubKey):
        sharedKeyDecimal = np.power(recipientPubKey, self.privKey) % Q
        sharedKeyBinary = bytes('{:032b}'.format(sharedKeyDecimal), encoding='utf8')
        fernetKey = Fernet(base64.urlsafe_b64encode(sharedKeyBinary))
        return fernetKey.encrypt(message)
    
    def decrypt(self, encryptedMessage, recipientPubKey):
        sharedKeyDecimal = np.power(recipientPubKey, self.privKey) % Q
        sharedKeyBinary = bytes('{:032b}'.format(sharedKeyDecimal), encoding='utf8')
        fernetKey = Fernet(base64.urlsafe_b64encode(sharedKeyBinary))
        return fernetKey.decrypt(encryptedMessage)


if __name__ == "__main__":
    # Construction.
    alice = Person("Alice")
    bob = Person("Bob")
    
    # Encryption
    encryptedMessage = alice.encrypt(b"Hi Bob, my credit card number is 1111 1111 1111 1111.", bob.getPubKey())
    print(encryptedMessage)

    # Decryption
    decryptedMessage = bob.decrypt(encryptedMessage, alice.getPubKey())
    print(decryptedMessage)