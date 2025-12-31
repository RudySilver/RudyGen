#!/usr/bin/env python3

import secrets
import string
import math

BAR_FULL = "█"
BAR_EMPTY = "░"

HUMAN_WORDS = [
    "Falcon", "Raven", "Nova", "Cipher", "Shadow",
    "Iron", "Pixel", "Storm", "Echo", "Lunar"
]

def human_password():
    return (
        secrets.choice(HUMAN_WORDS)
        + secrets.token_hex(2)
        + secrets.choice("!@#$_")
        + secrets.choice(HUMAN_WORDS).lower()
    )

def random_password(length=16):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(chars) for _ in range(length)), len(chars)

def entropy_bits(length, charset):
    return round(length * math.log2(charset), 2)

def strength_score(entropy):
    score = min(10, int(entropy / 12))
    label = (
        "Very Weak" if score <= 2 else
        "Weak" if score <= 4 else
        "Okay" if score <= 6 else
        "Strong" if score <= 8 else
        "Very Strong"
    )
    return score, label

def crack_time(entropy):
    guesses_per_sec = 1e10
    seconds = (2 ** entropy) / guesses_per_sec

    units = [
        ("years", 60 * 60 * 24 * 365),
        ("days", 60 * 60 * 24),
        ("hours", 60 * 60),
        ("minutes", 60),
    ]

    for name, div in units:
        value = seconds / div
        if value >= 1:
            return f"~ {int(value)} {name}"

    return "~ instantly"

def bar(score):
    return BAR_FULL * score + BAR_EMPTY * (10 - score)

def main():
    print("\nRudyGen ⚡ Secure. Fast. Human.\n")

    if secrets.randbelow(100) < 30:
        password = human_password()
        charset = 52
    else:
        password, charset = random_password()

    entropy = entropy_bits(len(password), charset)
    score, label = strength_score(entropy)
    crack = crack_time(entropy)

    print(f"Password : {password}")
    print(f"Strength : {bar(score)} {score}/10 ({label})")
    print(f"Entropy  : {entropy} bits")
    print(f"Crack    : {crack} (offline attack)\n")

    print("Generated locally. Nothing is saved. Nothing is sent.")
    print("Your password lives only on this machine.\n")

if __name__ == "__main__":
    main()
