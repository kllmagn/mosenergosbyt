# API для работы с порталом Мосэнергосбыт

## Использование из командной строки:
```
> mosenergosbyt -h
usage: mosenergosbyt [-h] [-i] -l LOGIN -p PASSWORD [-u] [-m METER] [-d DAY] [-n NIGHT] [-e EVENING]

Укажите параметры ввода

optional arguments:
  -h, --help            show this help message and exit
  -i, --info            Получение информации
  -l LOGIN, --login LOGIN
                        логин
  -p PASSWORD, --password PASSWORD
                        пароль
  -u, --upload          Передача показаний

```

Загрузка данных с портала
```
> mosenergosbyt -i -l **** -p *****
```
Получение данных в виде json либо сообщение об ошибке (при этом выполнение приложения завершается с статусом 1)

Загрукза данных на портал
```
> mosenergosbyt -u -l ***** -p **** -m *****-***-** -d * -n *
```
