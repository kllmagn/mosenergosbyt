# API для работы с порталом Мосэнергосбыт

## Установка

```
pip3 install git+https://gitflic.ru/project/alexbratchik/mosenergosbyt.git
```

ВНИМАНИЕ! Данная версия библиотеки mosenergosbyt является экспериментальной, и может
существенно меняться от версии к версии. Она также существенно отличается от оригинальной
версии автора @kkuryshev.

## Использование из командной строки:
```
> mosenergosbyt -h
uusage: mosenergosbyt [-h] [-i] -l LOGIN -p PASSWORD [-a ACCOUNT] [-e] [-b] [-y] [-o PERIOD] [-u] [-c COUNTER] [-v COUNTER_READING]

  -i, --info            Получение информации
  -l LOGIN, --login LOGIN
                        Имя пользователя
  -p PASSWORD, --password PASSWORD
                        Пароль
  -a ACCOUNT, --account ACCOUNT
                        Номер лицевого счета
  -e, --with_counters   Показывать информацию о счетчиках
  -b, --with_balance    Показывать информацию о балансе
  -y, --with_payments   Показывать информацию о платежах
  -o PERIOD, --period PERIOD
                        Показывать информацию за последние N месяцев
  -u, --upload          Передача показаний
  -c COUNTER, --counter COUNTER
                        Номер счетчика для передачи (обязательно для upload)
  -v COUNTER_READING, --counter_reading COUNTER_READING
                        Показания счетчика для передачи (обязательно для upload)
```

Загрузка данных с портала
```
> mosenergosbyt -i -l <имя пользователя> -p <пароль>
```
Получение данных в виде json либо сообщение об ошибке (при этом выполнение приложения завершается с статусом 1)

Загрузка данных на портал
```
> mosenergosbyt -u -l <имя пользователя> -p <пароль> -a <номер л/с> -c <номер счетчика> -v <показание>
```
