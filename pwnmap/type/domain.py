import validators


class Domain(str):
    """ Domain type str object """

    def __init__(self, domain):
        if validators.domain(domain) is False:
            raise ValueError('Invalid domain name')
