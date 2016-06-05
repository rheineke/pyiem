
import requests


class Session:
    base_url = 'https://iem.uiowa.edu/iem/'
    trader_url = base_url + 'trader/'

    def __init__(self, username=None, password=None):
        self._username = username
        self._password = password
        self._logger = None
        # Start session
        self._session = requests.Session()

    def build_url(self, path):
        return '{}{}'.format(self.trader_url, path)

    def authenticate(self):
        # Send login request to IEM
        data = {
            'forceLogin': False,  # Required
            'username': self._username,
            'password': self._password,
            'loginSubmit': 'Sign in',  # Required
            '_sourcePage': '',  # Required
        }

        login_url = sess.build_url('TraderLogin.action')
        return self._session.post(url=login_url, data=data)

    def _log(self, message):
        if self._logger:
            self._logger.write(message)

    def logout(self):
        logout_url = self.build_url('TraderLogin.action?logout=')
        return self._session.get(url=logout_url)


