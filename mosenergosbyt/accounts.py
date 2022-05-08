from mosenergosbyt.account import Account


class AccountException(BaseException):
    pass


class Accounts:
    def __init__(self, session):
        self.session = session
        self.__list = []

    def load(self,
             account="",
             with_counters=False,
             with_balance=False,
             with_payments=False,
             period=0) -> None:
        """
        Получение счетов клиента с портала с дополнительной информацией.
        :param account: номер лицевого счета. Возможно указвать только первые несколько знаков, либо пустую строку.
                        Если номер счета не указан, будут загружены все счета для указанного пользователя
        :param with_counters: если True то будет загружена информация по всем имеющимся счетчикам
        :param with_balance: если True то загружается информация по текущему балансу
        :param with_payments: еслм True то загружается инофрмация по последним платежам
        :param period: количество месяцев назад, за которое надо выводить информацию по платежам
        :return:
        """
        self.__list = []
        data = self.session.call('LSList')
        for item in data:
            if item['nn_ls'].startswith(account):
                obj = Account.parse(session=self.session, **item)
                if with_counters:
                    obj.get_counters()

                if with_balance:
                    obj.get_balance()

                if with_payments:
                    obj.get_payments(period=period)

                self.__list.append(obj)

    def get_list(self):
        return self.__list

    def get_account(self, nn_ls):
        """
        Возвращает лцевой счет по номеру счета
        :param nn_ls: номер лицевого счета
        :return:
        """
        accs = [item for item in self.__list if getattr(item, 'nn_ls') == nn_ls]
        return None if len(accs) == 0 else accs[0]
