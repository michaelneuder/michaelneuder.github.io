---
layout: post
title: Public-Key Cryptography
---

In this post we will discuss how public-key cryptography works and how it applies to cryptocurrencies. Broadly, cryptography is the study of sharing information privately over an insecure channel. In the context of modern computers, the goal is to exchange data over a network such that only the sender and recipient can decode it. Before 1976, the method of doing encrypting digital messages was using a shared private key (a pseudorandom string) to encode the data. This is problematic in many contexts, because it requires the sender and the receiver to agree on a private key before they can privately communicate. A solution to this problem was described by Diffie and Hellman in their [famous 1976 paper](https://ee.stanford.edu/~hellman/publications/24.pdf). They describe a system where two keys are created. The first, called the private-key, is kept secret to the individual, while the second, called the public key, is distributed over the network. Now if two individuals want to communicate, they can agree on a shared key to encrypt their data by each combining their private key with the others public key. We will explore exactly how this works, but first we need to cover a bit of number theory.

## Modular Arithmetic
The main result we will need to understand public-key cryptography is the definition of modular arithmetic. To begin, it is helpful to consider division. Let \\(A, B\\) be integers such that \\(A>B\\). Then we can define \\(A\\) in terms of \\(B\\), the quotient (how many copies of \\(B\\) fit in \\(A\\)), \\(q\\), and the remainder (how much is leftover), \\(r\\). More formally,


\\[
    A = B \cdot q + r.
\\]

As an example, consider the case where \\(A = 5\\) and \\(B=2\\), then \\(q=2\\) and \\(r=1\\) because two copies of \\(2\\) fit into \\(5\\) and there is \\(1\\) leftover. Now we can introduce the following notation,

\\[
    A_1 \equiv A_2 \; \textrm{mod}(B).
\\]

Intuitively, this means that \\(A_1 \; \& \; A_2\\) have the same *remainder* when divided by \\(B\\). Building off our example above where \\(B=5\\), consider \\(A_1=5 \; \& \; A_2 = 9\\), then we can assert the following

\\[
    5 \equiv 9 \; \textrm{mod}(2),
\\]

because \\(5\\) and \\(9\\) both have a remainder of \\(1\\) when divided by \\(2\\). Now we can see how this is useful in public-key cryptography.

## Key Distribution Algorithm 
Consider the case where Alice is trying to send Bob an encrypted message. Let \\(q\\) be a huge prime number that is known publicly. First, Alice will create her private key, denoted \\(A_0\\), and calculate her public key, denoted \\(A_1\\) with the following function,

\\[
    A_1 = 2^{A_0} \; \textrm{mod}(q).
\\]

Similarly, Bob will create his private key \\(B_0\\) and public key \\(B_1\\). Then they can each generate a shared private key,

\\[
    K = 2^{A_0\cdot B_0} \; \textrm{mod}(q).
\\]

Alice can calculate \\(K\\), by using Bob's public key in the following way,

\\[
    \begin{align}
        K &= B_1^{A_0} \; \textrm{mod}(q) \newline
        &= 2^{A_0\cdot B_0}\; \textrm{mod}(q).
    \end{align}
\\]

Similarly Bob can calculate \\(K\\) using Alice's public key and his private key. In this way they both agree on a shared key to use for the encryption without ever meeting outside of this insecure channel. Intuitively this works because they each have their own corresponding piece of the solution that they can use to quickly solve it. 

## Demo
Now that we have the theory developed, we can look at a toy example to see how this can work. The python3 code used in the demo can be found in full [here](https://github.com/michaelneuder/michaelneuder.github.io/blob/master/assets/code/publicKey.py). We will work through this file to understand what is going on. First, we define a global prime number that we will use `Q=23`. Now we define a class to that represents an individual on the network. The constructor simply takes a name for the person and chooses a random private key less than `Q` and stores both of these as class variables.

```python
def __init__(self, name):
    self.name = name
    self.privKey = np.random.randint(low=0, high=Q)
```

The next class function is a simple getter that returns the public key as a function of the private key as discussed in the previous section. This allows other users to access the public key without exposing the value of the private key.

```python
def getPubKey(self):
    return np.power(2, self.privKey) % Q
```

Now we get to the encryption function, which is parameterized with a message to encrypt and the public key of the recipient of the message. The first step is to create a shared key, which corresponds to finding the value of \\(K\\) as described above. Once we have the decimal representation we convert it a 32-bit binary string. To do the actual encryption given this shared key we will use the [cryptography python library](https://cryptography.io/en/latest/), and specifically the Fernet symmetric key functionality. Once we create a Fernet key with our shared key, then we can simply return the encrypted message. 

```python
def encrypt(self, message, recipientPubKey):
    sharedKeyDecimal = np.power(recipientPubKey, self.privKey) % Q
    sharedKeyBinary = bytes(
        '{:032b}'.format(sharedKeyDecimal), encoding='utf8')
    fernetKey = Fernet(base64.urlsafe_b64encode(sharedKeyBinary))
    return fernetKey.encrypt(message)
```

The decryption function is quite similar to the previous. In the same way, we create a shared key, convert it to binary, and create a Fernet key using it. But now we return the decrypt function on the encrypted message that was passed in.
```python
def decrypt(self, encryptedMessage, recipientPubKey):
    sharedKeyDecimal = np.power(recipientPubKey, self.privKey) % Q
    sharedKeyBinary = bytes(
        '{:032b}'.format(sharedKeyDecimal), encoding='utf8')
    fernetKey = Fernet(base64.urlsafe_b64encode(sharedKeyBinary))
    return fernetKey.decrypt(encryptedMessage)
```

Now we can test our class out. First in the main function, we instantiate our two people, Alice and Bob.
```python
# Construction.
alice = Person("Alice")
bob = Person("Bob")
```

Next we create an encrypted message from Alice to Bob. Notice how Alice never knows Bob's private key, she just calls the getter for his public key.
```python
# Encryption
encryptedMessage = alice.encrypt(b"Hi Bob, my credit card number is 1111 1111 1111 1111.", bob.getPubKey())
print(encryptedMessage)
```

The output from this print statement is seen below.
```
gAAAAABedqEurgAjBqyHIYN-qKOGCdP8k3vpU0HQsv-jifSHMMpQK8wenuW1NHWJlLudqyTNZrnxMNkIQBE2MwUNQJsiXjbj2Wq1MX36o8C36HZ1VSsAYuYKLE4w5AA8Raa8nuKT1b1Vyyk3Xd74PlbuNXApKL3Pag==
```

Now Bob can decrypt using only his private key and Alice's public key.
```python
# Decryption
decryptedMessage = bob.decrypt(encryptedMessage, alice.getPubKey())
print(decryptedMessage)
```
Finally, we can see the output from this print statement is indeed Alice's hidden message.
```
Hi Bob, my credit card number is 1111 1111 1111 1111.
```

Cool stuff! So this is a simple example of how public key encryption works. This is the foundation of modern cryptography and enables most of the encryption that happens on the internet. 

Thanks for reading! I hope you enjoyed, and please do reach out with comments/questions/corrections.

*Mike*