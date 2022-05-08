from datetime import datetime
from time import strftime
from mosenergosbyt.exceptions import *
from dateutil.relativedelta import relativedelta


class Account:
    def __init__(self, **kwargs):
        self.session = kwargs['session']
        self.nn_ls = kwargs['nn_ls']
        self.__vl_provider = kwargs['vl_provider']
        self.id_service = kwargs.get('id_service', None)
        self.nm_ls_group_full = kwargs.get('nm_ls_group_full', None)
        self.nm_provider = kwargs.get('nm_provider', None)
        self.nn_days = None
        self.balance = {}
        self.counters = []
        self.payments = []
        self.proxy = "smorodinaTransProxy"

    @property
    def vl_provider(self):
        if not self.__vl_provider:
            raise AccountException(
                'для получения списка переданных показаний нужно получить информацию о лицевом счете'
            )
        return self.__vl_provider

    @classmethod
    def parse(cls, **kwargs):
        return cls(**kwargs)

    def get_counters(self, with_measure=False) -> list:
        """
        Получение списка счетчиков
        :return:
        """

        try:
            data = self.__post_proxy_query(proxyquery="AbonentEquipment")
        except SessionTimeout:
            self.session.logger.warning('произошел таймаут обращения к порталу при получении списка счетчиков')
            return []

        self.counters = data
        return self.counters

    def get_balance(self) -> dict:
        try:
            data = self.__post_proxy_query(proxyquery='AbonentCurrentBalance')
        except SessionTimeout:
            self.session.logger.warning('произошел таймаут обращения к порталу при получении баланса')
            return {}
        self.balance = data[0]
        return self.balance

    def get_payments(self, period=0) -> list:
        """
        Получение списка платежей
        :param period: количество месяцев назад, начиная от текущей даты, за которое ноужно вывести список платежей
        :return:
        """
        try:
            last_date = datetime.now()
            n_months_ago = datetime.today() - relativedelta(months=period)

            querydata = {'dt_st': self.__format_date(n_months_ago),
                         'dt_en': self.__format_date(last_date)}

            data = self.__post_proxy_query(proxyquery='AbonentPays', proxyquerydata=querydata)
        except SessionTimeout:
            self.session.logger.warning('произошел таймаут обращения к порталу при получении списка оплат')
            return []

        self.payments = data

        return self.payments

    def upload_reading(self, nm_counter, reading) -> str:
        """
        Передача показаний
        :param nm_counter: номер счета
        :param reading: показания
        :return:
        """

        cns = [item for item in self.counters if item['nm_counter'] == nm_counter]

        if len(cns) == 0:
            return "Счетчик %s не найден для лицевого счета %s" % (nm_counter, self.nn_ls)

        counter = cns[0]

        return ""

    def __post_proxy_query(self, proxyquery, proxyquerydata=None) -> dict:
        """
        Запрос к порталу для получения списка оплат/переданных показаний
        :param proxyquery: тип запроса
        :param proxyquerydata: дополнительные параметры для запроса
        :return:
        """

        if proxyquerydata is None:
            proxyquerydata = {}

        proxyquerydata.update({
            'plugin': self.proxy,
            'proxyquery': proxyquery,
            'vl_provider': self.vl_provider
        })

        return self.session.call(self.proxy, data=proxyquerydata, timeout=5.0)

    @staticmethod
    def __format_date(d):
        return "%s%s" % (d.strftime('%Y-%m-%dT%H:%M:%S'), strftime("%z"))
