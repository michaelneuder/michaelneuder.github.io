---
layout: post
title: Public-Key Cryptography
---

In this post we will discuss how public-key cryptography works and how it applies to cryptocurrencies. Broadly, cryptography is the study of sharing information privately over an insecure channel. In the context of modern computers, the goal is to exchange data over a network such that only the sender and recipient can decode it. Before 1976, the method of doing encrypting digital messages was using a shared private key (a pseudorandom string) to encode the data. This is problematic in many contexts, because it requires the sender and the receiver to agree on a private key before they can privately communicate. A solution to this problem was described by Diffie and Hellman in their [famous 1976 paper](https://ee.stanford.edu/~hellman/publications/24.pdf). They describe a system where two keys are created. The first, called the private-key, is kept secret to the individual, while the second, called the public key, is distributed over the network. Now if two individuals want to communicate, they can agree on a shared key to encrypt their data by each combining their private key with the others public key. We will explore exactly how this works, but first we need to cover a bit of number theory.

## Modular Arithmetic

\\[ a^2 = b^2 + c^2 \\]