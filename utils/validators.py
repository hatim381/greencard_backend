import re

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
IBAN_REGEX = re.compile(r"^[A-Z]{2}[0-9A-Z]{13,32}$")
BIC_REGEX = re.compile(r"^[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?$")


def is_valid_email(email: str) -> bool:
    return bool(email and EMAIL_REGEX.match(email))


def is_valid_iban(iban: str) -> bool:
    return bool(iban and IBAN_REGEX.match(iban.replace(' ', '').upper()))


def is_valid_bic(bic: str) -> bool:
    return bool(bic and BIC_REGEX.match(bic.upper()))
