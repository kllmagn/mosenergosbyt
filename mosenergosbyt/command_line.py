
from mosenergosbyt import Session, Accounts
import argparse
from datetime import datetime
import json


def converter(obj):
    if isinstance(obj, Session):
        return None
    if isinstance(obj, datetime):
        return obj.__str__()
    else:
        return obj.__dict__


def toJson(obj):
    return json.dumps(obj, default=lambda o: converter(o), sort_keys=True, indent=4, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(description='Укажите параметры ввода')

    parser.add_argument('-i', '--info', action='store_true',
                        help='Получение информации')
    parser.add_argument('-l', '--login', required=True, type=str,
                        help='Имя пользователя')
    parser.add_argument('-p', '--password', required=True, type=str,
                        help='Пароль')
    parser.add_argument('-a', '--account', required=False, type=str, default="",
                        help='Номер лицевого счета (обязательно для upload)')
    parser.add_argument('-e', '--with_counters', action='store_true',
                        help='Показывать информацию о счетчиках')
    parser.add_argument('-b', '--with_balance', action='store_true',
                        help='Показывать информацию о балансе')
    parser.add_argument('-y', '--with_payments', action='store_true',
                        help='Показывать информацию о платежах')
    parser.add_argument('-o', '--period', required=False, type=int, default=3,
                        help='Показывать информацию за последние N месяцев')

    parser.add_argument('-u', '--upload', action='store_true',
                        help='Передача показаний')
    parser.add_argument('-c', '--counter', type=str,
                        help='Номер счетчика для передачи (обязательно для upload)')
    parser.add_argument('-r', '--counter_reading', type=float,
                        help='Показания счетчика для передачи (обязательно для upload)')

    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Печатать отладочную информацию')

    args = parser.parse_args()
    try:
        session = Session(login=args.login, password=args.password)
        session.logger.setLevel('DEBUG' if args.verbose else 'INFO')

        accounts = Accounts(session)
        accounts.load(account=args.account,
                      with_counters=True if args.upload else args.with_counters,
                      with_balance=False if args.upload else args.with_balance,
                      with_payments=False if args.upload else args.with_payments,
                      period=args.period)

        if args.info:
            session.logger.info(toJson(accounts.get_list()))
            exit(0)

        elif args.upload:
            account = accounts.get_account(args.account)
            if not account:
                session.logger.error(f'Информация о счете <{args.account}> не найдена')
                exit(1)

            res = account.upload_reading(args.counter, args.counter_reading)

            if res:
                session.logger.error(res)
                exit(1)
            else:
                session.logger.info("Показания переданы для аккаунта/счетчика %s / %s: %f" %
                      (args.account, args.counter, args.counter_reading))

    except SystemExit:
        pass
    except BaseException as e:
        print(e)
        exit(1)


if __name__ == "__main__":
    main()
