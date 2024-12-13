class UserSession:
    logged_in_username = None

    @staticmethod
    def set_logged_in_username(Username):
        UserSession.logged_in_username = Username

    @staticmethod
    def get_logged_in_username():
        return UserSession.logged_in_username

    @staticmethod
    def clear():
        UserSession.logged_in_username = None
