import validators


class Email(str):
    """ Email type str object """

    def __init__(self, email):
        if validators.email(email) is False:
            raise ValueError('Invalid email address')
