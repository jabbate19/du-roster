from sys import stderr

class User:
    def __init__(self, email):
        self.email = email

    def __str__(self):
        return '<email {}>'.format(self.email)

    def __repr__(self):
        return self.__str__

    def get_id(self):
        return self.email

    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False