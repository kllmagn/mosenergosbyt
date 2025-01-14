import logging
import sys

from requests import session
from requests.exceptions import Timeout, RequestException
from mosenergosbyt.exceptions import *
import json


class Session:
    __session = None

    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.token = None
        self.id_profile = None
        self.logger = logging.getLogger(__name__)
        formatter = logging.Formatter(logging.BASIC_FORMAT)
        st = logging.StreamHandler(sys.stdout)
        st.setFormatter(formatter)
        self.logger.addHandler(st)

    def __establish(self) -> None:
        self.__session = session()

        resp = self.call(
            query='login', action='auth',
            data={
                'login': self.login,
                'psw': self.password,
                'vl_device_info': json.dumps(
                    {"appver": "1.28.1", "type": "browser",
                     "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4; rv:99.0) " +
                                  "Gecko/20100101 Firefox/99.0"
                     }
                )
            }
        )
        data = self.check_auth_response(resp)

        self.token = data['session']
        self.id_profile = data['id_profile']

        self.call(query='Init')

    def call(self, query, action='sql', data=None, **kwargs) -> dict:
        """
        адаптер вызова портала
        :param query: наименование операции
        :type query: str
        :param action: тип операции (по умлочанию sql)
        :type action: str
        :param data: дополнительные данные для передачи в теле post
        :type data: dict
        :return:
        """

        self.logger.debug(f'query={query},action={action},data={data}')

        if not self.__session:
            self.__establish()

        try:
            resp = self.__session.post(
                'https://my.mosenergosbyt.ru/gate_lkcomu',
                headers={
                    'Sec-Fetch-Dest': 'empty',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Site': 'same-origin'
                },
                params={
                    'action': action,
                    'query': query,
                    'session': self.token
                },
                data=data,
                timeout=kwargs.get('timeout', None)
            )
        except RequestException as e:
            if isinstance(e, Timeout):
                raise SessionTimeout(e)
            else:
                raise SessionException(e)

        try:
            return self.check_response(resp)
        except InvalidSession as e:
            if kwargs.get('retry', False):
                raise e

            self.logger.info(f'сессия не валидна, нужно сделать переподключение ({e})')
            self.__session = None
            return self.call(query=query, action=action, data=data, retry=True)

    @staticmethod
    def check_auth_response(resp):
        if not resp:
            raise SessionException(
                'не корректный ответ'
            )

        data = resp[0]
        if data['kd_result']:
            raise SessionException(
                'ошибка авторизации (%s): %s' % (data['kd_result'], data['nm_result'])
            )

        return data

    def check_response(self, resp):
        if resp.status_code != 200:
            raise SessionException(
                'получен не корректный ответ от портала %s' % resp.status_code
            )

        j = resp.json()
        self.logger.debug(j)
        if not j['success']:
            if j['err_code'] == 201:
                raise InvalidSession(
                    j['err_text']
                )
            raise SessionException(
                'ошибка авторизации: %s' % j['err_text']
            )

        if 'data' not in j:
            raise SessionException(
                'не корректный ответ'
            )

        return j['data']
