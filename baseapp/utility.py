import re
from rest_framework.exceptions import ValidationError


email_regex =  re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
phone_regex = re.compile(r'^(\+998)?[ -]?\d{2}[ -]?\d{3}[ -]?\d{4}$')
username_regex = re.compile(r'^[a-zA-Z0-9.+-]*$')

def email_or_phone(email_phone_number):
    if re.fullmatch(email_regex , email_phone_number):
        data = 'email'
    elif re.fullmatch(phone_regex , email_phone_number):
        data = 'phone'
    else:
        data ={
            'success' : 'False',
            'message' : 'Siz telefon raqam yoki email ni xato kiritdingiz'
        }

        raise ValidationError(data)
    return data

def check_userinputtype(userinput):
    if re.fullmatch(email_regex , userinput):
        data = 'email'
    elif re.fullmatch(phone_regex , userinput):
        data = 'phone'
    elif re.fullmatch(username_regex , userinput):
        data = 'username'
    else:
        data ={
            'success' : 'False',
            'message' : 'Telefon raqam , email , username , xato kiritilgan bolishi mumkin'
        }
        raise ValidationError(data)
    return data
