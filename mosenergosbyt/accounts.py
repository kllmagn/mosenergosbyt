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
        accs = [item for item in self.__list if getattr(item, 'nn_ls') == nn_ls]
        return None if len(accs) == 0 else accs[0]
