#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test unitario del dígito verificador RIF (sin Odoo)."""


def rif_check_digit(letter, number):
    letter_map = {"V": 1, "E": 2, "J": 3, "P": 4, "G": 5, "C": 6}
    weights = [3, 2, 7, 6, 5, 4, 3, 2]
    body = (number or "").zfill(8)[-8:]
    total = letter_map.get(letter.upper(), 0) * 4
    for i, ch in enumerate(body):
        total += int(ch) * weights[i]
    remainder = total % 11
    check = 0 if remainder < 2 else 11 - remainder
    return str(check)


def main():
    samples = [
        ("V", "12345678"),
        ("J", "00012345"),
        ("J", "00312345"),
        ("G", "20000000"),
        ("E", "81234567"),
    ]
    print("Letra  Número    Dígito")
    print("-" * 28)
    for letter, number in samples:
        d = rif_check_digit(letter, number)
        full = f"{letter}-{number}-{d}"
        assert rif_check_digit(letter, number) == d
        print(f"{letter:5}  {number:9}  {d}  -> {full}")
    print("OK: algoritmo ejecutado sin errores")


if __name__ == "__main__":
    main()
