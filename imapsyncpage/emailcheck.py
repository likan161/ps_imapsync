from validate_email import validate_email

def emailcheck(email):
    is_valid = validate_email(email) 
    return(is_valid)
