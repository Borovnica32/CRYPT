import re
from core.colors import color

regexSpecial = re.compile(r'[@_!#$%^&*()<>?/\|}{~:]')
regexNumber = re.compile(r'\d')

def validate_password(password: str) -> tuple[bool, str]:
    if len(password) < 8:
        return False, "color.BOLD + color.ORANGE + Password must be at least 8 characters." + color.END

    if not regexNumber.search(password):
        return False, color.BOLD + color.ORANGE + "Password must contain at least one number." + color.END

    if not regexSpecial.search(password):
        return False, color.BOLD + color.ORANGE + "Password must contain at least one special character." + color.END

    return True, "OK"