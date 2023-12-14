from operator import itemgetter
import re

from SchedulingApp.models import MyUser, Course, Section


def func_MyUserCreator(email, password, passwordconfirm, first, last, phone, street, city, state, zip, role):
    if not func_ValidateEmail(email):
        return "Invalid email. Must be a UWM email."
    if MyUser.objects.filter(email=email).exists():
        return "Non-unique email. Please try again."
    if not func_ValidatePassword(password, passwordconfirm):
        return ("Passwords must match and contain one lowercase letter, one uppercase letter,"
                " a digit, and a special character. Please try again.")
    if not func_ValidateFirstName(first):
        return "Invalid first name. Must be capitalized and have only contain letters."
    if not func_ValidateLastName(last):
        return "Invalid last name. Must be capitalized and have only contain letters."
    if not func_ValidatePhoneNumber(phone):
        return "Invalid phone number. Format is 123-456-7890"
    if not func_ValidateStreetAddress(street):
        return "Invalid street address."
    if not func_ValidateCity(city):
        return "Invalid city. Must be capitalized."
    if not func_ValidateState(state):
        return "Invalid state. Two letter state code only."
    if not func_ValidateZipCode(zip):
        return "Invalid zipcode. Must be 5 digits long"
    if not func_ValidateRole(role):
        return "Invalid role. Can only be Admin, Instructor, or TA."

    user = MyUser.objects.create(email=email, password=password,
                                 firstName=first, lastName=last,
                                 phoneNumber=phone, streetAddress=street,
                                 city=city, state=state,
                                 zipcode=zip, role=role)
    user.save()
    return "User created successfully!"


def func_EditFirstName(firstname, email):
    try:
        changeUser = MyUser.objects.get(email=email)
    except:
        return "User does not exist!"
    if func_ValidateFirstName(firstname):
        changeUser.firstName = firstname
        changeUser.save()
        return "First name changed successfully!"
    else:
        return "Invalid first name. Must be capitalized and have only contain letters."


def func_EditLastName(lastname, email):
    try:
        changeUser = MyUser.objects.get(email=email)
    except:
        return "User does not exist!"
    if func_ValidateLastName(lastname):
        changeUser.lastName = lastname
        changeUser.save()
        return "Last name changed successfully!"
    else:
        return "Invalid last name. Must be capitalized and have only contain letters."

def func_EditPhoneNumber(phonenumber, email):
    try:
        changeUser = MyUser.objects.get(email=email)
    except:
        return "User does not exist!"
    if func_ValidatePhoneNumber(phonenumber):
        changeUser.phoneNumber = phonenumber
        changeUser.save()
        return "Phone number changed successfully!"
    else:
            return "Invalid phone number. Format is 123-456-7890"

def func_EditStreetAddress(streetaddress, email):
    try:
        changeUser = MyUser.objects.get(email=email)
    except:
        return "User does not exist!"
    if func_ValidateStreetAddress(streetaddress):
        changeUser.streetAddress = streetaddress
        changeUser.save()
        return "Street address changed successfully!"
    else:
        return "Invalid street address."

def func_EditCity(city, email):
    try:
        changeUser = MyUser.objects.get(email=email)
    except:
        return "User does not exist!"
    if func_ValidateCity(city):
        changeUser.city = city
        changeUser.save()
        return "City changed successfully!"
    else:
        return "Invalid city. Must be capitalized."

def func_EditState(state, email):
    try:
        changeUser = MyUser.objects.get(email=email)
    except:
        return "User does not exist!"
    if func_ValidateState(state):
        changeUser.state = state
        changeUser.save()
        return "State changed successfully!"
    else:
        return "Invalid state. Two letter state code only."

def func_EditZipcode(zipcode, email):
    try:
        changeUser = MyUser.objects.get(email=email)
    except:
        return "User does not exist!"
    if func_ValidateZipCode(zipcode):
        changeUser.zipcode = zipcode
        changeUser.save()
        return "Zipcode changed successfully!"
    else:
        return "Invalid zipcode. Must be 5 digits long."

def func_EditRole(role, email):
    try:
        changeUser = MyUser.objects.get(email=email)
    except:
        return "User does not exist!"
    if func_ValidateRole(role):
        changeUser.role = role
        changeUser.save()
        return "Role changed successfully!"
    else:
        return "Invalid role. Can only be Admin, Instructor, or TA."

def func_MyUserDeleter(email):
    try:
        user = MyUser.objects.get(email=email)
    except:
        return "User does not exist!"
    user.delete()
    return "User deleted successfully"


"""
Input: string - an email
Output: True if it is a UWM email. False otherwise.
"""

def func_ValidateEmail(email):
    return bool(re.fullmatch(r"[^@\s.]{1,12}@uwm\.edu", email))

"""
Input: string, string - two matching passwords
Output: True if passwords match and have one lowercase letter, one uppercase letter,
one digit, one special character, and at least 8 chars long. False otherwise
"""

def func_ValidatePassword(password, confirmPassword):

    if password != confirmPassword:
        return False
    if len(password) < 8 or len(password) > 20:
        return False

    special = ["@", "#", "$", "%",
               "^", "&", "*", "`",
               "(", ")", "-", "_",
               "+", "=", "{", "}",
               "|", "~", "/", "",
               "<", ">", ",", ".",
               ";", ":", "'", "?",
               "!"]

    if not any(char in special for char in password):
        return False

    if not any(char.isupper() for char in password):
        return False

    if not any(char.islower() for char in password):
        return False

    if not any(char.isdigit() for char in password):
        return False

    return True

"""
Input: string - a name.
Output: True if it is capatalized, has no spaces, and only contains letters. False otherwise.
"""

def func_ValidateFirstName(firstName):
    if not isinstance(firstName, str):
        return False
    if len(firstName) > 20:
        return False
    if firstName == '':
        return False
    if (all(c.isalpha() and not c.isspace() for c in firstName)):
        if firstName[0].islower():
            return False
        else:
            return True
    else:
        return False

"""
Input: string - a name.
Output: True if it is capatalized, has no spaces, and only contains letters. False otherwise.
"""

def func_ValidateLastName(lastName):
    if not isinstance(lastName, str):
        return False
    if len(lastName) > 20:
        return False
    if lastName == '':
        return False
    if (all(c.isalpha() and not c.isspace() for c in lastName)):
        if lastName[0].islower():
            return False
        else:
            return True
    else:
        return False

"""
Input: string - a phone number.
Output: True if in the format 123-456-7890. False otherwise.
"""

def func_ValidatePhoneNumber(phoneNumber):
    pattern1 = re.compile(r'^\(\d{3}\)\d{3}-\d{4}$')
    pattern2 = re.compile(r'^\d{3}-\d{3}-\d{4}$')
    pattern3 = re.compile(r'^\d{10}$')
    pattern4 = re.compile(r'^\(\d{3}\)\d{7}$')

    match1 = pattern1.match(phoneNumber)
    match2 = pattern2.match(phoneNumber)
    match3 = pattern3.match(phoneNumber)
    match4 = pattern4.match(phoneNumber)

    return bool(match1) or bool(match2) or bool(match3) or bool(match4)

"""
Input: string - an address.
Output: True if at least three words. First Word must contain numbers False otherwise.
"""

def func_ValidateStreetAddress(streetAddress):
    if streetAddress == '' or streetAddress.isspace():
        return False
    if any(not char.isalnum() and not char.isspace() for char in streetAddress):
        return False
    s = streetAddress.split()
    if any(char.isdigit() for char in s[0]):
        if len(s) < 3 or len(streetAddress) > 100:
            return False
        else:
            return True

"""
Input: string - a city.
Output: True if capitalized and only contains letters and spaces. False otherwise.
"""

def func_ValidateCity(city):
    if city == '' or city.isspace():
        return False
    if not city[0].isupper():
        return False
    pattern = re.compile(r'^[a-zA-Z\s]{2,20}$')
    match = pattern.match(city)
    return bool(match)

"""
Input: string - a state.
Output: True if one of the state postal codes. False otherwise.
"""

def func_ValidateState(state):
    valid_state = ["AL", "AK", "AZ", "AR",
                   "CA", "CO", "CT", "DC",
                   "DE", "FL", "GA", "HI",
                   "ID", "IL", "IN", "IA",
                   "KS", "KY", "LA", "ME",
                   "MD", "MA", "MI", "MN",
                   "MS", "MO", "MT", "NE",
                   "NV", "NH", "NJ", "NM",
                   "NY", "NC", "ND", "OH",
                   "OK", "OR", "PA", "RI",
                   "SC", "SD", "TN", "TX",
                   "UT", "VT", "VA", "WA",
                   "WV", "WI", "WY"]

    return state in valid_state

"""
Input: int - a zipcode.
Output: True if 5 digits long. False otherwise.
"""

def func_ValidateZipCode(zip):
    if not isinstance(zip, str):
        return False
    if len(zip) != 5:
        return False
    if any(not char.isdigit() for char in zip):
        return False
    return True

"""
Input: string - a role.
Output: True 'admin', 'instructor', or 'ta'. False otherwise.
"""

def func_ValidateRole(role):
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("instructor", "Instructor"),
        ("ta", "TA")
    ]
    return any(role in choice for choice in ROLE_CHOICES)

def func_SaveBio(email, bio):
    user = MyUser.objects.filter(email=email).first()
    user.bio = func_RemoveExcessNewLine(bio)
    user.save()

def func_RemoveExcessNewLine(string):
    lines = string.split('\r\n')
    formatted_string =''
    for line in lines:
        if line != '':
            formatted_string += line
            formatted_string += '\r\n'
    return formatted_string


