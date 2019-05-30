def has_numeric_and_alpha(password: str) -> bool:
    return (not password.isnumeric()) and (not password.isalpha())


def has_upper_and_lower_letters(password: str) -> bool:
    return has_upper_letters(password) and has_lower_letters(password)


def has_upper_letters(password: str) -> bool:
    for character in set(password):
        if character.isupper():
            return True
    return False


def has_lower_letters(password: str) -> bool:
    for character in set(password):
        if character.islower():
            return True
    return False
