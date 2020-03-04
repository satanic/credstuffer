import logging
from credstuffer.proxy import Proxy
from credstuffer.exceptions import ProxyMaxRequestError, ProxyBadConnectionError


class Stuffer:
    """ Base class Stuffer to provide basic methods for the stuffing algorithm

    USAGE:
            stuffer = Stuffer(account=account, timeout_ms=50)

    """
    def __init__(self, account, timeout_ms=50):
        self.logger = logging.getLogger('credstuffer')
        self.logger.info('create class Stuffer')

        self.account = account

        self.proxy = Proxy(timeout_ms=timeout_ms)
        self.http_str = 'http://'
        self.https_str = 'https://'

    def set_account_proxy(self):
        """ sets a proxy for the given account

        :param account: account instance
        """

        proxy_alive = False
        while not proxy_alive:
            proxy = self.__get_proxy_dict()
            if self.account.is_proxy_alive(proxy=proxy):
                self.account.set_proxy(proxy=proxy)
                proxy_alive = True

    def account_login(self, password):
        """ executes the account login with given password

        """
        try:
            self.account.login(password)
        except (ProxyMaxRequestError, ProxyBadConnectionError) as e:
            self.set_account_proxy()
            self.account_login(password=password)

    def __get_proxy_dict(self):
        """ get proxy dictionary

        :return: dict with 'http' proxy
        """
        proxy = self.proxy.get()
        http_proxy = self.http_str + proxy

        return {'http': http_proxy}