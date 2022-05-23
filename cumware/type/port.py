class Port(int):
    """ Port type int object """

    def __init__(self, port):
        try:
            port = int(port)

            if not 1 <= port <= 65535:
                raise Exception()

        except Exception:
            raise ValueError('Invalid port number')
