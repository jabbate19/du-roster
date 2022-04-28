class User:
    def __init__(self, email):
        self.email = email

    def __repr__(self):
        return '<id {}>'.format(self.email)

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