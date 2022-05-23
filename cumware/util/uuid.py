import uuid


class UUIDUtil:

    @staticmethod
    def validate(_id, version=4):
        try:
            uuid.UUID(_id, version=version)
            return True
        except:
            return False

    @classmethod
    def remove_hyphen(cls, uid, version=4):
        if not cls.validate(uid, version):
            raise ValueError('Invalid UUID: ' + uid)

        return uuid.UUID(uid, version=version).hex

    @classmethod
    def add_hyphen(cls, uid, version=4):
        if not cls.validate(uid, version):
            raise ValueError('Invalid UUID: ' + uid)

        return str(uuid.UUID(uid, version=4))
