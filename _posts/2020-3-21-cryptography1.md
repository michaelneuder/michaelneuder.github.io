---
layout: post
title: Public-Key Cryptography
---

In this post we will discuss how public-key cryptography works and how it applies to cryptocurrencies. Broadly, cryptography is the study of sharing information privately over an insecure channel. In the context of modern computers, the goal is to exchange data over a network such that only the sender and recipient can decode it. Before 1976, the method of doing encrypting digital messages was using a shared private key (a pseudorandom string) to encode the data. This is problematic in many contexts, because it requires the sender and the receiver to agree on a private key before they can privately communicate. A solution to this problem was described by Diffie and Hellman in their [famous 1976 paper](https://ee.stanford.edu/~hellman/publications/24.pdf). They describe a system where two keys are created. The first, called the private-key, is kept secret to the individual, while the second, called the public key, is distributed over the network. Now if two individuals want to communicate, they can agree on a shared key to encrypt their data by each combining their private key with the others public key. We will explore exactly how this works, but first we need to cover a bit of number theory.

## Modular Arithmetic
The main result we will need to understand public-key cryptography is the definition of modular arithmetic. To begin, it is helpful to consider division. Let $A, B$ be integers such that $A>B$. Then we can define $A$ in terms of $B$, the quotient (how many copies of $B$ fit in $A$), $q$, and the remainder \(how much is leftover\), $r$. More formally,

$$
\begin{equation}
    A &= B \cdot q + r.
\begin{equation}
$$

As an example, consider the case where $A = 5$ and $B=2$, then $q=2$ and $r=1$ because two copies of $2$ fit into $5$ and there is $1$ 
leftover. Now we can introduce the following notation,

\begin{align*}
    A_1 \equiv A_2 \; \textrm{mod}(B).
\end{align*}

Intuitively, this means that $A_1 \; \& \; A_2$ have the same *remainder* when divided by $B$. Building off our example above where $B=5$, consider $A_1=5 \; \& \; A_2 = 9$, then we can assert the following

\begin{align*}
    5 \equiv 9 \; \textrm{mod}(2),
\begin{align*}

because $5$ and $9$ both have a remainder of $1$ when divided by $2$. Now we can see how this is useful in public-key cryptography.

## Key Distribution Algorithm 
Consider the case where Alice is trying to send Bob an encrypted message. Let $q$ be a huge prime number that is known publicly. First, Alice will create her private key, denoted $A_0$, and calculate her public key, denoted $A_1$ with the following function,

\begin{align*}
    A_1 = 2^{A_0} \; \textrm{mod}(q).
\begin{align*}

Similarly, Bob will create his private key $B_0$ and public key as,

\begin{align*}
    B_1 = 2^{B_0} \; \textrm{mod}(q).
\begin{align*}

Then they can each generate a shared private key,

\begin{align*}
    K = 2^{A_0\cdot B_0} \; \textrm{mod}(q).
\begin{align*}

Alice can calculate $K$, by using Bob's public key in the following way,

\begin{align*}
    K = B_1^{A_0} \; \textrm{mod}(q).
\begin{align*}

1234